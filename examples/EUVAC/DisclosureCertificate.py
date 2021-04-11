from typing import Optional


class DisclosureCertificate:
    """
    Simple POD data struct for certificate fields
    """
    def __init__(self):
        self.Is = "" # TODO should be 'is'
        self.id = "" # TODO str = Optional[None]  # NOT completed for DisclosureLevel PV
        self.st = ""
        self.en = ""
        self.vr = ""
        self.ia = ""
