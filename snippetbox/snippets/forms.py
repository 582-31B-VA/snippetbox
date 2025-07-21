from dataclasses import dataclass

from snippetbox.utils.forms import Form


@dataclass
class SnippetCreateForm(Form):
    title: str = ""
    content: str = ""
    valid_days: int = 365
