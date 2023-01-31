from password_validator import PasswordValidator

schema = PasswordValidator()
schema.min(8).max(30).has().uppercase().has().lowercase().has().digits().has().no().spaces()

