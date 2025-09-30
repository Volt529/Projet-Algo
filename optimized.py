import csv
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import time
import argparse

DEFAULT_BUDGET_EUR = 500.0

def parse_float(value: str) -> float:
    s = str(value).strip()
    s = s.replace("€", "").replace("%", "").replace("\u00A0", "").replace(" ", "")
    s = s.replace(",", ".")
    if s == "":
        raise ValueError("empty")
    return float(s)

def load_stocks(csv_path: Path) -> List[Dict]:
    stocks = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        def find_key(poss):
            for k in fieldnames:
                if k is None: continue
                kl = k.lower()
                for p in poss:
                    if p in kl:
                        return k
            raise KeyError(f"no header among {poss} found in {fieldnames}")
        name_k = find_key(["action", "titre", "name"])
        cost_k = find_key(["coût", "cout", "price", "prix"])
        profit_k = find_key(["bénéfice", "benefice", "profit", "return"])
        for row in reader:
            try:
                name = str(row[name_k]).strip()
                cost = parse_float(row[cost_k])
                percent = parse_float(row[profit_k])
                if cost <= 0: continue
                profit = cost * (percent / 100.0)
                if profit <= 0: continue
                stocks.append({
                    "name": name,
                    "cost_eur": round(cost, 2),
                    "cost_cents": int(round(cost * 100)),
                    "percent": percent,
                    "profit_eur": round(profit, 2),
                    "profit_cents": int(round(profit * 100)),
                })
            except Exception:
                
                continue
    return stocks

def best_single(stocks: List[Dict], budget_cents: int):
    best = None
    for s in stocks:
        if s["cost_cents"] <= budget_cents:
            if best is None or s["profit_cents"] > best["profit_cents"]:
                best = s
    return best

def knapsack_dp(stocks: List[Dict], budget_cents: int) -> Tuple[List[Dict], int, int, int]:
    
    dp = [0] * (budget_cents + 1)
    parents_updates = []  

    for idx, s in enumerate(stocks):
        c = s["cost_cents"]
        p = s["profit_cents"]
        updates = {}
       
        for w in range(budget_cents, c - 1, -1):
            candidate = dp[w - c] + p
            if candidate > dp[w]:
                dp[w] = candidate
                updates[w] = w - c
        parents_updates.append(updates)

    
    best_w = max(range(budget_cents + 1), key=lambda w: dp[w])
    best_profit_cents = dp[best_w]

    
    w = best_w
    selected_indices = []
    for idx in range(len(stocks) - 1, -1, -1):
        updates = parents_updates[idx]
        if w in updates:
            prev_w = updates[w]
            selected_indices.append(idx)
            w = prev_w
    selected_indices.reverse()
    selection = [stocks[i] for i in selected_indices]
    total_cost_cents = sum(s["cost_cents"] for s in selection)
    total_profit_cents = sum(s["profit_cents"] for s in selection)
    return selection, total_cost_cents, total_profit_cents, best_profit_cents

def format_eur_cents(cents: int) -> str:
    return f"{cents/100:.2f} €"

def main(argv=None):
    parser = argparse.ArgumentParser(description="Optimized portfolio selector (0/1 knapsack DP)")
    parser.add_argument("--input", "-i", type=str, default="Liste+d'actions+-+P7+Python+-+Feuille+1.csv", help="CSV input file path")
    parser.add_argument("--budget", "-b", type=float, default=DEFAULT_BUDGET_EUR, help="Budget in euros")
    parser.add_argument("--mode", "-m", choices=["combo", "single"], default="combo", help="combo = best subset, single = best single action")
    args = parser.parse_args(argv)

    csv_path = Path(args.input)
    if not csv_path.exists():
        print(f"File not found: {csv_path}")
        return 2
    start = time.time()
    stocks = load_stocks(csv_path)
    if not stocks:
        print("No valid stocks after parsing.")
        return 1
    budget_cents = int(round(args.budget * 100))

    if args.mode == "single":
        best = best_single(stocks, budget_cents)
        if best is None:
            print("No single action fits the budget.")
        else:
            print("--- Best single action ---")
            print(f"Name: {best['name']}")
            print(f"Cost: {best['cost_eur']:.2f} € | Profit: {best['profit_eur']:.2f} € ({best['percent']:.2f} %)")
    else:
        selection, cost_cents, profit_cents, dp_best = knapsack_dp(stocks, budget_cents)
        end = time.time()
        print("--- Best combination (DP) ---")
        print(f"Items available: {len(stocks)} | Budget: {args.budget:.2f} € ({budget_cents} cents)")
        print(f"Selected items: {len(selection)}")
        print(f"Total cost: {format_eur_cents(cost_cents)}")
        print(f"Total profit: {format_eur_cents(profit_cents)}")
        print(f"Final value (cost + profit): {format_eur_cents(cost_cents + profit_cents)}")
        print(f"Time: {(end-start):.4f} s")
        print("\nSelection details:")
        for s in selection:
            print(f"- {s['name']} | Cost: {s['cost_eur']:.2f} € | Profit: {s['profit_eur']:.2f} € | {s['percent']:.2f} %")

if __name__ == '__main__':
    main()