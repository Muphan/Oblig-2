


reuels_books = ["The Hobbit",
                "Farmer Giles of Ham",
                "The Fellowship of the Ring",
                "The Two Towers",
                "The Return of the King",
                "The Adventures of Tom Bombadil",
                "Tree and Leaf"]

line = "="*20
# 1.
def deloppgave1():
    there_and_back_again = reuels_books[:2]+reuels_books[-2:]

    print(f"{line}\nDeloppgave 1:\n{line}")
    for book in there_and_back_again:
        print(book)
    print(line)

deloppgave1()

#2
def deloppgave2():
    posthumous = ["The Silmarillion", "Unfinished Tales"]
    global reuels_books #er vel ikke akkurat beste praksis å drive å forandre globale variabler fra inni funksjoner x)
    reuels_books = reuels_books+posthumous

deloppgave2()
#print(reuels_books[-1])

#3
def deloppgave3():
    lotr = "Lord of the Rings: "
    books_in_lotr = ["The Fellowship of the Ring",
                     "The Two Towers",
                     "The Return of the King"]
    for book in books_in_lotr:
        i = reuels_books.index(book)
        full_title = lotr+reuels_books.pop(i)
        reuels_books.insert(i, full_title)
    return reuels_books


reuels_books = deloppgave3() #dette er vel den mer korrekte måten å forande den globale variabelen på :3

#4
reuels_books.sort() #var ikke nevnt hvordan de skulle sorteres så kjørte bare alfabetisk, selv om det blir tragisk hultertilbulter

print(f"{line}\nDeloppgave 4.:\n{line}")
for book in reuels_books:
    print(book)
print(line)


"""
================================================
Kjøreeksempel:
================================================
====================
Deloppgave 1:
====================
The Hobbit
Farmer Giles of Ham
The Adventures of Tom Bombadil
Tree and Leaf
====================
====================
Deloppgave 4.:
====================
Farmer Giles of Ham
Lord of the Rings: The Fellowship of the Ring
Lord of the Rings: The Return of the King
Lord of the Rings: The Two Towers
The Adventures of Tom Bombadil
The Hobbit
The Silmarillion
Tree and Leaf
Unfinished Tales
====================

Process finished with exit code 0
================================================
"""





