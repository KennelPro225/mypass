solde = 1000
depense = int(input())
recette = int(input())
if depense > 0:
    solde = solde-depense
    print(solde)
elif recette > 0:
    solde = solde+recette
    print(solde)
