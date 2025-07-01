from os import getcwd, path


# It's good practice to define your configuration class in a separate
# file. Eventually, we might want to differentiate between development,
# testing, and production configuration.
class Config:
    DATABASE_PATH = path.join(getcwd(), "instance", "db.sqlite")
