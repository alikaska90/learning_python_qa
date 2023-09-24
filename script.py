from src.constants import BOOK_FIELDS, USER_FIELDS, BOOKS_CSV, USERS_JSON, RESULT_JSON
from src.csv_handler import CSVHandler
from src.json_handlre import JSONHandler

book_list = CSVHandler(BOOKS_CSV).read_file()
user_list = JSONHandler(USERS_JSON).read_file()

num_books = len(book_list)
num_users = len(user_list)

count = 0
result = []


def dict_format(dictionary: dict, fields: list) -> dict:
    return {field.lower(): dictionary.get(field) for field in fields}


for user in user_list:
    num_books_for_user = num_books // num_users + 1 \
        if count < num_books % num_users \
        else num_books // num_users
    user_format = dict_format(user, USER_FIELDS)
    user_format["books"] = [dict_format(book_list.pop(0), BOOK_FIELDS) for i in range(num_books_for_user)]
    result.append(user_format)
    count += 1

JSONHandler(RESULT_JSON).write_file(result)
