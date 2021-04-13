class InvalidLanguageValue(Exception):
    """Customed exception raised when the arguments and keyword
    arguments passed to the Lang constructor are not a valid combination of:
    - ISO 639 language name
    - ISO 639-1 language code
    - ISO 639-2B language code
    - ISO 639-2T language code
    - ISO 639-3 language code
    - ISO 639-5 language code
    """

    def __init__(self, *args, **kwargs):

        arg_str = ", ".join(list(args) + ["=".join(x) for x in kwargs.items()])
        msg = f"'{arg_str}' not supported by ISO 639"

        super().__init__(msg)
