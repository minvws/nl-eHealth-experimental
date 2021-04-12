from cryptography import x509
from DisclosureCertificate import DisclosureCertificateBuilder
from DisclosureLevel import DisclosureLevel


class DisclosureCertificateDirectDictMapper:
    @staticmethod
    def build(cert : x509.Certificate, disclosureLevel : DisclosureLevel):
        # TODO Which is Issuer, which is Issuing Authority
        # TODO cert.extensions.get_extension_for_oid()
        result = {}
        result["ia"] = DisclosureCertificateBuilder.findIssuingAuthority(cert, disclosureLevel)
        result["is"] = cert.issuer.rfc4514_string() #TODO Correct format?
        result["st"] = cert.not_valid_before.isoformat() #TODO is missing the Z?
        result["en"] = cert.not_valid_after.isoformat() #TODO is missing the Z?
        result["vr"] = DisclosureCertificateBuilder.findVersion(cert)
        if disclosureLevel != DisclosureLevel.PrivateVenue:
            result["id"] = DisclosureCertificateBuilder.findId(cert) #TODO Correct format?
        return result