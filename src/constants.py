import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS_CSV = os.path.join(ROOT_DIR, "input_data", "books.csv")
USERS_JSON = os.path.join(ROOT_DIR, "input_data", "users.json")
RESULT_JSON = os.path.join(ROOT_DIR, "result.json")

BOOK_FIELDS = ["Title", "Author", "Pages", "Genre"]
USER_FIELDS = ["name", "gender", "address", "age"]
