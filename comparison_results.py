import os
import csv

# ======================
# Algo optimisé (sac à dos dynamique)
# ======================
def load_stocks(file_path):
    """Charge les actions depuis un fichier CSV"""
    stocks = []
    try:
        with open(file_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    name = row['name']
                    price = float(row['price'])
                    profit = float(row['profit'])
                    if price > 0 and profit > 0:
                        stocks.append((name, price, profit))
                except (KeyError, ValueError):
                    continue
    except FileNotFoundError:
        print(f"❌ Fichier {file_path} introuvable !")
        return []
    except Exception as e:
        print(f"❌ Erreur lors du chargement de {file_path}: {e}")
        return []
    return stocks

def knapsack(stocks, max_budget=500):
    """Algorithme du sac à dos pour optimiser les investissements"""
    if not stocks:
        return [], 0, 0
        
    n = len(stocks)
    W = int(max_budget * 100)  # Éviter les flottants → centimes
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    # Remplissage de la matrice DP
    for i in range(1, n + 1):
        name, cost, profit = stocks[i - 1]
        cost = int(cost * 100)
        for w in range(W + 1):
            if cost <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - cost] + profit)
            else:
                dp[i][w] = dp[i - 1][w]

    # Reconstruction des choix optimaux
    w = W
    chosen = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            name, cost, profit = stocks[i - 1]
            chosen.append((name, cost, profit))
            w -= int(cost * 100)

    total_cost = sum(x[1] for x in chosen)
    total_profit = sum(x[2] for x in chosen)
    return chosen[::-1], total_cost, total_profit

# ======================
# Création de données de test
# ======================
def create_test_data():
    """Crée des fichiers CSV de test si ils n'existent pas"""
    # Dataset 1 : Une seule action très chère
    dataset1_data = [
        {"name": "Share-GRUT", "price": "498.76", "profit": "196.61"},
        {"name": "Share-TEST", "price": "100.00", "profit": "50.00"},
        {"name": "Share-DEMO", "price": "200.00", "profit": "80.00"},
    ]
    
    with open("dataset1_Python+P7.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "price", "profit"])
        writer.writeheader()
        writer.writerows(dataset1_data)
    
    # Dataset 2 : Plusieurs actions plus petites
    dataset2_data = [
        {"name": "Share-ECAQ", "price": "25.50", "profit": "10.20"},
        {"name": "Share-IXCI", "price": "30.75", "profit": "12.30"},
        {"name": "Share-FWBE", "price": "45.20", "profit": "18.08"},
        {"name": "Share-ZOFA", "price": "22.10", "profit": "8.84"},
        {"name": "Share-PLLK", "price": "38.90", "profit": "15.56"},
        {"name": "Share-YFVZ", "price": "41.25", "profit": "16.50"},
        {"name": "Share-ANFX", "price": "28.60", "profit": "11.44"},
        {"name": "Share-PATS", "price": "33.80", "profit": "13.52"},
        {"name": "Share-NDKR", "price": "27.45", "profit": "10.98"},
        {"name": "Share-ALIY", "price": "35.15", "profit": "14.06"},
        {"name": "Share-JWGF", "price": "24.30", "profit": "9.72"},
        {"name": "Share-JGTW", "price": "31.95", "profit": "12.78"},
        {"name": "Share-FAPS", "price": "26.85", "profit": "10.74"},
        {"name": "Share-VCAX", "price": "29.70", "profit": "11.88"},
        {"name": "Share-LFXB", "price": "32.40", "profit": "12.96"},
        {"name": "Share-DWSK", "price": "23.55", "profit": "9.42"},
        {"name": "Share-XQII", "price": "36.20", "profit": "14.48"},
        {"name": "Share-ROOM", "price": "40.15", "profit": "16.06"},
    ]
    
    with open("dataset2_Python+P7.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "price", "profit"])
        writer.writeheader()
        writer.writerows(dataset2_data)
    
    print("✅ Fichiers de test créés !")

# ======================
# Comparaison Algo vs Sienna
# ======================
def compare_results(dataset_name, file_path, sienna_cost, sienna_profit, sienna_actions):
    """Compare les résultats de l'algorithme optimisé avec ceux de Sienna"""
    stocks = load_stocks(file_path)
    
    if not stocks:
        print(f"❌ Impossible de charger les données pour {dataset_name}")
        return None
    
    chosen, cost, profit = knapsack(stocks)

    print(f"\n{'='*50}")
    print(f"📊 COMPARAISON - {dataset_name}")
    print(f"{'='*50}")
    
    print(f"🤖 Algo Optimisé :")
    print(f"   💰 Coût total   : {cost:.2f} €")
    print(f"   📈 Profit total : {profit:.2f} €")
    print(f"   🎯 ROI          : {(profit/cost*100):.1f}%")
    print(f"   📋 Actions      : {len(chosen)} action(s)")
    
    print(f"\n👤 Sienna :")
    print(f"   💰 Coût total   : {sienna_cost:.2f} €")
    print(f"   📈 Profit total : {sienna_profit:.2f} €")
    print(f"   🎯 ROI          : {(sienna_profit/sienna_cost*100):.1f}%")
    print(f"   📋 Actions      : {len(sienna_actions)} action(s)")
    
    # Calcul des différences
    diff_cost = cost - sienna_cost
    diff_profit = profit - sienna_profit
    
    print(f"\n🔍 DIFFÉRENCES :")
    print(f"   💰 Coût    : {diff_cost:+.2f} € ({'+' if diff_cost > 0 else ''}{'plus cher' if diff_cost > 0 else 'moins cher' if diff_cost < 0 else 'identique'})")
    print(f"   📈 Profit  : {diff_profit:+.2f} € ({'+' if diff_profit > 0 else ''}{'meilleur' if diff_profit > 0 else 'moins bon' if diff_profit < 0 else 'identique'})")
    
    if diff_profit > 0:
        print(f"   🏆 L'algorithme optimisé est MEILLEUR de {diff_profit:.2f} € !")
    elif diff_profit < 0:
        print(f"   🤔 Sienna est meilleure de {abs(diff_profit):.2f} € (inattendu)")
    else:
        print(f"   ⚖️  Résultats identiques")

    print(f"\n📋 DÉTAIL DES ACTIONS :")
    print(f"🤖 Algo : {[x[0] for x in chosen]}")
    print(f"👤 Sienna : {sienna_actions}")
    
    print(f"\n{'='*50}")

    return {
        "dataset": dataset_name,
        "algo_cost": cost,
        "algo_profit": profit,
        "algo_actions": [x[0] for x in chosen],
        "sienna_cost": sienna_cost,
        "sienna_profit": sienna_profit,
        "sienna_actions": sienna_actions,
    }

# ======================
# MAIN - Exécution du programme
# ======================
if __name__ == "__main__":
    print("🚀 COMPARAISON ALGORITHME OPTIMISÉ vs SIENNA")
    print("=" * 60)
    
    # Créer les fichiers de test si ils n'existent pas
    if not os.path.exists("dataset1_Python+P7.csv") or not os.path.exists("dataset2_Python+P7.csv"):
        print("📁 Création des fichiers de test...")
        create_test_data()
    
    results = []

    # Dataset 1 - Comparaison
    sienna1 = {
        "cost": 498.76,
        "profit": 196.61,
        "actions": ["Share-GRUT"]
    }
    result1 = compare_results("Dataset 1", "dataset1_Python+P7.csv",
                             sienna1["cost"], sienna1["profit"], sienna1["actions"])
    if result1:
        results.append(result1)

    # Dataset 2 - Comparaison
    sienna2 = {
        "cost": 489.24,
        "profit": 193.78,
        "actions": ["Share-ECAQ", "Share-IXCI", "Share-FWBE", "Share-ZOFA", "Share-PLLK",
                    "Share-YFVZ", "Share-ANFX", "Share-PATS", "Share-NDKR", "Share-ALIY",
                    "Share-JWGF", "Share-JGTW", "Share-FAPS", "Share-VCAX", "Share-LFXB",
                    "Share-DWSK", "Share-XQII", "Share-ROOM"]
    }
    result2 = compare_results("Dataset 2", "dataset2_Python+P7.csv",
                             sienna2["cost"], sienna2["profit"], sienna2["actions"])
    if result2:
        results.append(result2)

    # Résumé final
    if results:
        print(f"\n🎯 RÉSUMÉ FINAL")
        print("=" * 30)
        for r in results:
            algo_better = r["algo_profit"] > r["sienna_profit"]
            status = "🏆 GAGNANT" if algo_better else "🤔 À VÉRIFIER" if r["algo_profit"] < r["sienna_profit"] else "⚖️ ÉGALITÉ"
            print(f"{r['dataset']} : {status}")
        print("\n✅ Comparaison terminée !")
    else:
        print("❌ Aucun dataset n'a pu être traité")
  