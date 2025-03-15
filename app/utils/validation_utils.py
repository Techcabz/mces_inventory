import re

class Validation:
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


    @staticmethod
    def is_valid_name(name):
        """Check if the name contains only alphabetic characters."""
        name_pattern = r"^[A-Za-z\s]+$"  # Allow spaces
        return bool(re.match(name_pattern, name))

    @staticmethod
    def has_repeated_characters(name, threshold=3):
        """Check if the name has three or more consecutive repeated characters."""
        return bool(re.search(r"(.)\1{" + str(threshold - 1) + r",}", name))

    @staticmethod
    def is_valid_number(value):
        """Check if the value is a positive integer."""
        return value.isdigit() and int(value) > 0
    @staticmethod
    def allowed_file(filename):
        """Check if the file extension is allowed."""
        return "." in filename and filename.rsplit(".", 1)[1].lower() in Validation.ALLOWED_EXTENSIONS
    
    @staticmethod
    def is_valid_password(password):
        if len(password) < 8:
            return "Password must be at least 8 characters long."
        if not any(char.isdigit() for char in password):
            return "Password must contain at least one number."
        if not any(char.isupper() for char in password):
            return "Password must contain at least one uppercase letter."
        if not any(char in "!@#$%^&*()-_=+{}[]|;:'\",.<>?/`~" for char in password):
            return "Password must contain at least one special character."
        return None  # Password is valid

