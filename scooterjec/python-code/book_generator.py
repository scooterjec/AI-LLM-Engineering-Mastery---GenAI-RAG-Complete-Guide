
class Book:
    """ A class to model a book """
    title = "book title"
    author="JEC"
    genre="fiction"
    
    def __init__(self, title, author, genre):
        print("running init")
        self.title = title
        self.author = author
        self.genre = genre
        self.num_pages = 230
    
    def __str__(self) -> str:
        return f"Book object: {self.title} - {self.author} - {self.genre}"
        
    def describe_book(self):
        print("Describing a book...")
        print(f"{self.title}, {self.author}, {self.genre}")
        
    def update_num_pages(self, new_num_pages):
        self.num_pages = new_num_pages
        
    def get_num_pages(self):
        print(f"The book '{self.title}' has {self.num_pages} pages")
        
    def read_book(self):
        print(f"Reading (phisical) {self.title} by {self.author}")
        
class EBook(Book):
    def __init__(self, title, author, genre, filesize, format):
        super().__init__(title, author, genre)
        self.filesize=filesize
        self.format=format
    
    def download_book(self):
        print(f"Downloading {self.title} in {self.format} format with size {self.filesize} KB")
        
    def describe_book(self):
        super().describe_book()
        print(f"File Size: {self.filesize} KB")
        
    def read_book(self):
        print(f"Reading (electronic) {self.title} by {self.author}")

# book = Book("titulo", "autor", "genero")
# print(book)
# book.describe_book()
# book.read_book()
# book.get_num_pages()
# book.update_num_pages (340)
# book.get_num_pages()

# ebook = EBook("Don Quijote", "Cervantes", "Historico", "1234", "PDF")
# ebook.describe_book()
# ebook.download_book()
# ebook.read_book()