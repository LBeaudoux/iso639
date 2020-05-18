class InvalidLanguageValue(Exception):
    """Customed exception raised when the argument passed to the Lang 
    constructor is not a valid:
    - ISO 639 language name
    - ISO 639-3 language code
    - ISO 639-1 language code
    """

    def __init__(self, language):

        msg = f"{language} is not a valid ISO-639 value"

        super().__init__(msg)
