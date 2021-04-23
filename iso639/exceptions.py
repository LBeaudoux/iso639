class InvalidLanguageValue(Exception):
    """Exception raised when the arguments and keyword arguments passed to
    the Lang constructor are not a valid combination of:
    - ISO 639 language name
    - ISO 639-1 language code
    - ISO 639-2B language code
    - ISO 639-2T language code
    - ISO 639-3 language code
    - ISO 639-5 language code
    """

    def __init__(self, *args, **kwargs):

        arg_str = ", ".join(list(args) + ["=".join(x) for x in kwargs.items()])
        self.msg = f"'{arg_str}' not supported by ISO 639"

        super().__init__(self.msg)


class DeprecatedLanguageValue(Exception):
    """Exception raised when the arguments and keyword arguments passed to the
    Lang constructor point to a deprecated ISO 639-3 language code
    """

    def __init__(self, *args, **kwargs):

        reasons = {
            "C": "change",
            "D": "duplicate",
            "N": "non-existent",
            "S": "split",
            "M": "merge",
        }
        reason = reasons.get(kwargs.get("ret_reason"))
        if kwargs.get("ret_remedy"):
            remedy = "{ret_remedy}.".format(**kwargs)
        elif kwargs.get("change_to"):
            remedy = "Use [{change_to}] instead.".format(**kwargs)
        else:
            remedy = ""
        pt = (
            "As of {effective}, [{id}] for {ref_name} is deprecated "
            "due to {0}. {1}"
        )

        self.msg = pt.format(reason, remedy, **kwargs)
        self.name = kwargs.get("ref_name", "")
        self.change_to = kwargs.get("change_to", "")

        super().__init__(self.msg)
