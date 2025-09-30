import csv
from pathlib import Path

BUDGET = 500.0

def parse_float(value: str) -> float:
    """Convertit un texte en float (gère €, %, virgules)."""
    s = str(value).strip()
    s = s.replace("€", "").replace("%", "").replace(" ", "").replace(",", ".")
    return float(s)

def load_stocks(file_path: Path):
    """Charge les actions en acceptant plusieurs formats d'en-têtes."""
    stocks = []
    with file_path.open(newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # Reconnaissance souple des noms de colonnes
        def find_key(possible_names):
            for key in reader.fieldnames:
                if key is None:
                    continue
                k = key.lower().strip()
                for name in possible_names:
                    if name in k:
                        return key
            raise KeyError(f"Impossible de trouver une colonne parmi {possible_names}")

        name_key = find_key(["action", "titre", "name"])
        price_key = find_key(["coût", "cout", "prix", "price"])
        profit_key = find_key(["bénéfice", "benefice", "profit", "return"])

        for row in reader:
            try:
                name = row[name_key].strip()
                cost = parse_float(row[price_key])
                percent = parse_float(row[profit_key])
                if cost <= 0:
                    continue
                profit = cost * (percent / 100)
                if profit <= 0:
                    continue
                stocks.append({
                    "name": name,
                    "cost": round(cost, 2),
                    "percent": percent,
                    "profit": round(profit, 2)
                })
            except Exception:
                continue
    return stocks

def best_single_stock(stocks, budget=BUDGET):
    """Retourne l'action unique la plus rentable (dans le budget)."""
    best = None
    for stock in stocks:
        if stock["cost"] <= budget:
            if best is None or stock["profit"] > best["profit"]:
                best = stock
    return best

if __name__ == "__main__":
    file_path = Path("C:/Users/sylva/Documents/School 2/Liste+d'actions+-+P7+Python+-+Feuille+1.csv")

    stocks = load_stocks(file_path)
    if not stocks:
        print("❌ Aucune action valide trouvée")
    else:
        best = best_single_stock(stocks)
        print("=== Action la plus rentable ===")
        print(f"Nom      : {best['name']}")
        print(f"Coût     : {best['cost']} €")
        print(f"Rendement: {best['percent']} %")
        print(f"Profit   : {best['profit']} €")