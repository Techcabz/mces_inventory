import re


class Validation:
    def is_valid_name(name):
        name_pattern = r"^[A-Za-z]+$"
        return bool(re.match(name_pattern, name))

    def has_no_repeated_characters(name):
        return not bool(re.search(r"(.)\1{2,}", name))
