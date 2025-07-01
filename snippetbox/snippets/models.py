from dataclasses import dataclass
from datetime import datetime, timedelta

from snippetbox.utils.db import Model


@dataclass
class Snippet:
    id: int
    title: str
    content: str
    created: datetime
    expires: datetime


class SnippetModel(Model):
    def insert(self, title: str, content: str, days_valid: int) -> int:
        now = datetime.now()
        expires = now + timedelta(days=days_valid)
        cursor = self.db.execute(
            """
            INSERT INTO Snippets (title, content, created, expires)
                VALUES (?, ?, ?, ?)
            """,
            (title, content, now, expires),
        )
        self.db.commit()

        id = cursor.lastrowid
        if not id:
            raise RuntimeError("insert failed: no lastrowid")

        return id

    def get(self, id: int) -> Snippet:
        id, title, content, created, expires = self.db.execute(
            """
            SELECT id, title, content, created, expires
            FROM Snippets
            WHERE expires > CURRENT_TIMESTAMP
                AND id = ?
            """,
            (id,),
        ).fetchone()
        return Snippet(id, title, content, created, expires)

    def latest(self) -> list[Snippet]:
        rows = self.db.execute(
            """
            SELECT id, title, content, created, expires
            FROM Snippets
            WHERE expires > CURRENT_TIMESTAMP
            ORDER BY id
            LIMIT 10
            """
        ).fetchall()
        print(rows)
        return [Snippet(*row) for row in rows]
