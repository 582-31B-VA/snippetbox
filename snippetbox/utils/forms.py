from dataclasses import dataclass, field


@dataclass
class Form:
    errors: dict[str, str] = field(init=False, default_factory=lambda: {})

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def add_error(self, key: str, msg: str) -> None:
        self.errors[key] = msg

    def check_field(self, ok: bool, key: str, msg: str) -> None:
        if not ok:
            self.add_error(key, msg)


class Field:
    @staticmethod
    def not_blank(value: str) -> bool:
        return value.strip() != ""

    @staticmethod
    def max_chars(value: str, max: int) -> bool:
        return len(value) <= max

    @staticmethod
    def permitted_value(value: object, permitted_values: list[object]) -> bool:
        return value in permitted_values
