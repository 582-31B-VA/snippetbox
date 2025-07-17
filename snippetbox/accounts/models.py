from dataclasses import dataclass

from werkzeug.security import generate_password_hash, check_password_hash

from snippetbox.utils.db import Model
from snippetbox.snippets.models import Snippet, SnippetModel


@dataclass
class Account:
    id: int
    email: str
    password: str
    snippets: list[Snippet]


class InvalidCredentialsError(Exception): ...


class AccountModel(Model):
    def insert(self, email: str, password: str) -> int:
        cursor = self.db.execute(
            """
            INSERT INTO Accounts (email, password)
                VALUES (?, ?)
            """,
            # If your database is ever compromised by an attacker, it's
            # hugely important that it doesn't contain the plain-text
            # versions of your users' passwords. It's essential to
            # store a one-way hash of the password.
            (email, generate_password_hash(password)),
        )
        self.db.commit()

        id = cursor.lastrowid
        if not id:
            raise RuntimeError("insert failed: no lastrowid")

        return id

    def get(self, id: int) -> Account:
        email, password = self.db.execute(
            "SELECT email, password FROM Accounts WHERE id = ?", (id,)
        ).fetchone()
        snippets = SnippetModel(self.db)
        return Account(id, email, password, snippets.account_snippets(id))

    def authenticate(self, email: str, password: str) -> Account:
        account = self.db.execute(
            "SELECT id, email, password FROM Accounts WHERE email = ?",
            (email,),
        ).fetchone()

        if account is None or not check_password_hash(account[2], password):
            raise InvalidCredentialsError()

        id, email, password = account
        snippets = SnippetModel(self.db)
        return Account(id, email, password, snippets.account_snippets(id))

    def email_exists(self, email: str) -> bool:
        account = self.db.execute(
            "SELECT * FROM Accounts WHERE email = ?", (email,)
        ).fetchone()
        return account is not None
