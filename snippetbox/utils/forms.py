from re import fullmatch

from dataclasses import dataclass, field


@dataclass
class Form:
    # We now make a distinction between errors belonging to a specific
    # field (e.g., password too short) and general form errors such as
    # bad credentials.
    field_errors: dict[str, str] = field(init=False, default_factory=dict)
    non_field_errors: list[str] = field(init=False, default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.field_errors) == 0

    def add_field_error(self, key: str, msg: str) -> None:
        self.field_errors[key] = msg

    def add_non_field_error(self, msg: str) -> None:
        self.non_field_errors.append(msg)

    def check_field(self, ok: bool, key: str, msg: str) -> None:
        if not ok:
            self.add_field_error(key, msg)


class Field:
    @staticmethod
    def not_blank(value: str) -> bool:
        return value.strip() != ""

    @staticmethod
    def max_chars(value: str, max: int) -> bool:
        return len(value) <= max

    @staticmethod
    def min_chars(value: str, min: int) -> bool:
        return len(value) >= min

    @staticmethod
    def is_valid_email(value: str) -> bool:
        # This pattern is the one currently recommended by the W3C
        # and Web Hypertext Application Technology Working Group for
        # validating email addresses.
        pattern = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
        return fullmatch(pattern, value) is not None

    @staticmethod
    def permitted_value(value: object, permitted_values: list[object]) -> bool:
        return value in permitted_values
