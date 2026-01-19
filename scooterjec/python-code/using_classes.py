from  book_generator import Book, EBook

book=Book("Titulo","Autor","Genero")
ebook=EBook("Tit","Aut","Gen","1234","EPub")

print(book.describe_book())
print(ebook.describe_book())