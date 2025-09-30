#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AlgoInvest&Trade - Brute-force optimizer
----------------------------------------
Lit un CSV d'actions et énumère *toutes* les combinaisons respectant :
- budget <= 500 €
- 1 action au plus une fois
- pas de fraction d'action (0 ou 1 de chaque)

Puis renvoie la combinaison qui maximise le profit total après 2 ans.

Usage:
    python bruteforce.py
"""

import csv
import sys
from pathlib import Path
from typing import List, Dict, Tuple

BUDGET_EUR = 500.0

def parse_float(value: str) -> float:
    """Convertit une chaîne en float en gérant €, %, espaces, et virgule décimale."""
    if value is None:
        raise ValueError("Valeur manquante")
    s = str(value).strip()
    s = s.replace("€", "").replace("%", "").replace(" ", "").replace("\u00A0", "")
    s = s.replace(",", ".")
    if s == "":
        raise ValueError("Valeur vide")
    return float(s)

def load_stocks(csv_path: Path) -> List[Dict]:
    """Charge et nettoie les données d'actions depuis un CSV."""
    stocks: List[Dict] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        def key_like(targets: List[str]) -> str:
            for k in reader.fieldnames or []:
                kl = k.lower().strip()
                for t in targets:
                    if t in kl:
                        return k
            raise KeyError(f"Colonne manquante: {targets} parmi {reader.fieldnames}")

        try:
            name_key = key_like(["action", "titre", "name"])
            cost_key = key_like(["coût", "cout", "price", "prix"])
            benefit_key = key_like(["bénéfice", "benefice", "profit", "return"])
        except KeyError as e:
            raise SystemExit(f"Erreur d'en-têtes CSV: {e}")

        for row in reader:
            try:
                name = str(row[name_key]).strip()
                cost = parse_float(row[cost_key])
                percent = parse_float(row[benefit_key])
                if cost <= 0:
                    continue
                profit = cost * (percent / 100.0)
                if profit <= 0:
                    continue
                stocks.append({
                    "name": name,
                    "cost": round(cost, 2),
                    "percent": percent,
                    "profit": round(profit, 2),
                })
            except Exception:
                continue
    return stocks

def brute_force_optimize(stocks: List[Dict], budget: float=BUDGET_EUR) -> Tuple[List[Dict], float, float, int]:
    """Teste toutes les combinaisons et retourne (sélection, coût_total, profit_total, nb_combos_testées)."""
    n = len(stocks)
    best_profit = 0.0
    best_cost = 0.0
    best_subset_indices: List[int] = []
    combos_tested = 0

    for mask in range(1, 1 << n):
        combos_tested += 1
        total_cost = 0.0
        total_profit = 0.0
        for i in range(n):
            if mask & (1 << i):
                c = stocks[i]["cost"]
                p = stocks[i]["profit"]
                total_cost += c
                if total_cost > budget:
                    total_profit = -1.0
                    break
                total_profit += p
        if total_profit >= 0 and total_profit > best_profit:
            best_profit = total_profit
            best_cost = total_cost
            best_subset_indices = [i for i in range(n) if mask & (1 << i)]

    best_selection = [stocks[i] for i in best_subset_indices]
    return best_selection, round(best_cost, 2), round(best_profit, 2), combos_tested

def main(argv: List[str]) -> int:
    # Utilisation du chemin passé en argument ou chemin par défaut
    if len(argv) > 1:
        csv_path = Path(argv[1])
    else:
        csv_path = Path(r"C:\Users\sylva\Documents\School 2\Liste+d'actions+-+P7+Python+-+Feuille+1.csv")

    if not csv_path.exists():
        print(f"Fichier introuvable: {csv_path}")
        return 2

    stocks = load_stocks(csv_path)
    if not stocks:
        print("Aucune action valide trouvée après nettoyage.")
        return 1

    selection, total_cost, total_profit, combos = brute_force_optimize(stocks, BUDGET_EUR)

    print("=== Résultat optimal (force brute) ===")
    print(f"Budget maximal      : {BUDGET_EUR:.2f} €")
    print(f"Combinaisons testées: {combos:,}".replace(",", " "))
    print(f"Nombre d'actions    : {len(selection)} / {len(stocks)}")
    print(f"Coût total          : {total_cost:.2f} €")
    print(f"Profit total (2 ans): {total_profit:.2f} €")
    print(f"Valeur finale (coût + profit): {total_cost + total_profit:.2f} €")
    print("\nDétail de la sélection:")
    print(f"{'Action':<12} {'Coût (€)':>10} {'Bénéf.(%)':>10} {'Profit (€)':>12}")
    print("-" * 48)
    for s in selection:
        print(f"{s['name']:<12} {s['cost']:>10.2f} {s['percent']:>10.2f} {s['profit']:>12.2f}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
