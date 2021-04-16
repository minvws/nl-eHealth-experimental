from disclosure_level import DisclosureLevel


class UvciReader:
    def __init__(self, value: str):
        self.__value = value

    def is_valid(self):
        delimiter_count = self.__value.count("/") - 2
        if delimiter_count < 0 or delimiter_count > 2:
            raise ValueError("Invalid UVCI option.")

        # TODO checksum validation

    def get_option(self):
        delimiter_count = self.__value.count("/") - 2
        if delimiter_count < 0 or delimiter_count > 2:
            raise ValueError("Invalid UVCI option.")

        if delimiter_count == 2:
            return 1
        if delimiter_count == 0:
            return 2
        if delimiter_count == 1:
            return 3

    def get_identifer(self, disclosure_level: DisclosureLevel):
        if disclosure_level == DisclosureLevel.PrivateVenue:
            return self.get_issuing_country()
        return self.__value

    def get_issuing_country(self):
        start = self.__value.find("/", 2) + 1  # skip the 01 prefix
        end = self.__value.find("/", start)
        return self.__value[start:end]

    def get_schema_version(self):
        return self.__value[0:2]

    def get_issuing_authority(self):
        if self.get_option() == 2:
            return None

        start = self.__value.find("/", 3) + 1  # skip the 01/ prefix
        end = self.__value.find("/", start)
        return self.__value[start:end]
