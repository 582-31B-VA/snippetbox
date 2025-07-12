from dataclasses import dataclass

from snippetbox.utils.forms import Form


@dataclass
class SnippetCreateForm(Form):
    # We define the form's fields and their default value.
    title: str = ""
    content: str = ""
    valid_days: int = 365
