from os import getcwd, path


class Config:
    DATABASE_PATH = path.join(getcwd(), "instance", "db.sqlite")

    # Cookies are signed using this key. Secret keys should be as random
    # as possible. You can use "secrets.token_hex" from the standard
    # library to generate one.
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
