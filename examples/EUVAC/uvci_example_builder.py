import uuid


class UvciExampleBuilder:
    # Med 10 vaccine code
    # Issuing entity - assuming NL for now

    VERSION = "01"
    FAKED_LUHN_MOD10_VALUE = 8  # TODO actual LUNH Mod 10 value

    @staticmethod
    def get_example(
        vaccine_code="XX123",
        country="NL",
        issuing_entity="anIssuingEntity",
    ) -> str:
        opaque_unique_string = uuid.uuid4().hex  # Opaque unique string
        return f"{UvciExampleBuilder.VERSION}/{country}/{issuing_entity}/{vaccine_code}/{opaque_unique_string}#{UvciExampleBuilder.FAKED_LUHN_MOD10_VALUE}"
