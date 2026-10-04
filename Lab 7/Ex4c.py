def checkPurchases(recentPurchases, budget):
    totalSpent = 0


    for purchase in recentPurchases:
        totalSpent += purchase
        if totalSpent > budget:
            print(f"this purchase {purchase} is over budget!")
            break
        else:
            print(f"this purchase {purchase} is within budget")


recentPurchases = [36.13, 23.87, 183.35, 22.93, 11.62]
budget = 250
checkPurchases(recentPurchases, budget)
