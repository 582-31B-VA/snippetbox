from os import getcwd, path


class Config:
    DATABASE_PATH = path.join(getcwd(), "instance", "db.sqlite")
