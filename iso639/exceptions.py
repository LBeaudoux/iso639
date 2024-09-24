class InvalidLanguageValue(Exception):
    """Exception raised when the argument passed to the `Lang` constructor is
    not a valid:
    - ISO 639-1 identifier
    - ISO 639-2 English name
    - ISO 639-2/B identifier
    - ISO 639-2/T identifier
    - ISO 639-3 identifier
    - ISO 639-3 inverted name
    - ISO 639-3 printed name
    - ISO 639-3 reference name
    - ISO 639-5 identifier
    """

    def __init__(self, name_or_identifier):

        self.invalid_value = name_or_identifier
        self.msg = (
            f"'{name_or_identifier}' is not a valid "
            "ISO 639 name or identifier."
        )

        super().__init__(self.msg)


class DeprecatedLanguageValue(Exception):
    """Exception raised when the argument passed to the `Lang` constructor
    points to a deprecated ISO 639 language name or identifier.
    """

    def __init__(self, *args, **kwargs):

        reasons = {
            "C": "change",
            "D": "duplicate",
            "N": "non-existent",
            "S": "split",
            "M": "merge",
            "Add": "newly added",
            "Dep": "deprecated",
            "CC": "code change",
            "NC": "name change",
            "NA": "variant name(s) added",
        }
        reason = reasons.get(kwargs.get("reason"))
        if kwargs.get("change_to"):
            remedy = "Use [{change_to}] instead.".format(**kwargs)
        elif kwargs.get("ret_remedy"):
            remedy = kwargs["ret_remedy"]
            if not remedy.endswith("."):
                remedy += "."
        else:
            remedy = ""
        pt = (
            "As of {effective}, [{id}] for {name} is deprecated "
            "due to {0}. {1}"
        )

        self.msg = pt.format(reason, remedy, **kwargs)
        for attr_name in (
            "id",
            "name",
            "reason",
            "change_to",
            "ret_remedy",
            "effective",
        ):
            attr_value = kwargs.get(attr_name, "")
            setattr(self, attr_name, attr_value)

        super().__init__(self.msg)
