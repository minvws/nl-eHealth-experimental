from cryptography import x509
from CertificateReader import CertificateReader
from DisclosureLevel import DisclosureLevel


class DisclosureCertificateDirectDictMapper:
    @staticmethod
    def build(cert: x509.Certificate, disclosure_level: DisclosureLevel):
        # TODO Which is Issuer, which is Issuing Authority
        # TODO cert.extensions.get_extension_for_oid()
        result = {"ia": CertificateReader.find_issuing_authority(cert, disclosure_level),
                  "is": cert.issuer.rfc4514_string(),
                  "st": cert.not_valid_before.isoformat(),
                  "en": cert.not_valid_after.isoformat(),
                  "vr": CertificateReader.find_version(cert)
                  }
        if disclosure_level != DisclosureLevel.PrivateVenue:
            result["id"] = CertificateReader.find_id(cert)  # TODO Correct format?

        return result
