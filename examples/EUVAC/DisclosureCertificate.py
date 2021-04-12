from binascii import hexlify
# TODO reinstate - from typing import Optional
from cryptography import x509
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.x509 import NameOID
from DisclosureLevel import DisclosureLevel

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

class DisclosureCertificateDictMapper:
    @staticmethod
    def build(cert : DisclosureCertificate, disclosureLevel : DisclosureLevel):
        result = {}
        result["ia"] = cert.ia
        result["is"] = cert.Is
        result["st"] = cert.st
        result["en"] = cert.en
        result["vr"] = cert.vr
        if disclosureLevel != DisclosureLevel.PrivateVenue:
            result["id"] = cert.id
        return result

class DisclosureCertificateFriendlyDictMapper:
    @staticmethod
    def build(cert : DisclosureCertificate, disclosureLevel : DisclosureLevel):
        result = {}
        result["issuingAuthority"] = cert.ia
        result["issuer"] = cert.Is
        result["validStart"] = cert.st
        result["validEnd"] = cert.en
        result["version"] = cert.vr
        if disclosureLevel != DisclosureLevel.PrivateVenue:
            result["identifier"] = cert.id
        return result

class DisclosureCertificateBuilder:
    @staticmethod
    def build(cert : x509.Certificate, disclosureLevel : DisclosureLevel):
        # TODO Which is Issuer, which is Issuing Authority
        # TODO cert.extensions.get_extension_for_oid()
        result = DisclosureCertificate()
        result.Is = cert.issuer.rfc4514_string() #TODO Correct format?
        result.id = DisclosureCertificateBuilder.findId(cert) #TODO Correct format?
        result.st = cert.not_valid_before.isoformat() #TODO is missing the Z?
        result.en = cert.not_valid_after.isoformat() #TODO is missing the Z?
        result.vr = DisclosureCertificateBuilder.findVersion(cert)
        result.ia = DisclosureCertificateBuilder.findIssuingAuthority(cert, disclosureLevel)
        return result

    # TODO admin 1 sheet says UVCI but this is a dupe of issuing authority?
    @staticmethod
    def findId(cert: x509.Certificate):
        return hexlify(cert.fingerprint(SHA256())).decode('ascii')

    # TODO this is V1 or V3 - dont believe this is the required value? Setting?
    @staticmethod
    def findVersion(cert: x509.Certificate):
        return cert.version.name

    # TODO CHECK! PV = -only 2-digit country code from UVCI; BC, MD - Full UVCI
    @staticmethod
    def findIssuingAuthority(cert, disclosureLevel : DisclosureLevel):
        if disclosureLevel == DisclosureLevel.PrivateVenue:
            return cert.issuer.rfc4514_string()

        # TODO assume single result
        return cert.issuer.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value


