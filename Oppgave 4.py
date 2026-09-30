#synd jeg ikke skrev den forrige oppgaven som klasser, så jeg bare kunne kalt på dem her x)
lotr = []
line = "="*20
jrr_books = ["The Hobbit",
             "Farmer Giles of Ham",
             "The Fellowship of the Ring",
             "The Two Towers",
             "The Return of the King",
             "The Adventures of Tom Bombadil",
             "Tree and Leaf",
             "The Silmarillion",
             "Unfinished Tales"]

lotr_books = ["The Fellowship of the Ring",
                 "The Two Towers",
                 "The Return of the King"]

def make_list():
    for book in jrr_books:
        if book in lotr_books:
            lotr.append("Lord of the Rings: "+book)

make_list()
#print(lotr)
print(f"{line}\nEksempel 1:\n{line}")
#eksempel 1
for b in lotr:
    print(b)

print(f"{line}\nEksempel 2:\n{line}")
#eksempel 2
for i in range(len(lotr)):
    print(lotr[i])

print(f"{line}\nEksempel 3:\n{line}")
#eksempel 3
for i, b in enumerate(lotr):
    print(f"{i+1}: {b}")

"""
================================================
Kjøreeksempel:
================================================
====================
Eksempel 1:
====================
Lord of the Rings: The Fellowship of the Ring
Lord of the Rings: The Two Towers
Lord of the Rings: The Return of the King
====================
Eksempel 2:
====================
Lord of the Rings: The Fellowship of the Ring
Lord of the Rings: The Two Towers
Lord of the Rings: The Return of the King
====================
Eksempel 3:
====================
1: Lord of the Rings: The Fellowship of the Ring
2: Lord of the Rings: The Two Towers
3: Lord of the Rings: The Return of the King

Process finished with exit code 0
"""


