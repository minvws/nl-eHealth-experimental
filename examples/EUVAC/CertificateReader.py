from binascii import hexlify
from cryptography import x509
from cryptography.hazmat.primitives.hashes import SHA256
# noinspection PyProtectedMember
from cryptography.x509 import NameOID, Certificate
from DisclosureLevel import DisclosureLevel

# TODO specify private or private key expected?
class CertificateLoader:

    # "dsc-worker.pem"
    @staticmethod
    def load(filename: str) -> Certificate:
        with open(filename, "rb") as file:
            pem = file.read()
        cert = x509.load_pem_x509_certificate(pem)
        return cert


class CertificateReader:
    # TODO admin 1 sheet says UVCI but this is a dupe of issuing authority?
    # TODO same for UVCI bytes? Beginning or end?
    @staticmethod
    def find_id(cert: x509.Certificate) -> str:
        return hexlify(cert.fingerprint(SHA256())).decode('ascii')

    # TODO this is V1 or V3 - dont believe this is the required value? Setting?
    @staticmethod
    def find_version(cert: x509.Certificate):
        return cert.version.name

    # TODO CHECK! PV = -only 2-digit country code from UVCI; BC, MD - Full UVCI
    @staticmethod
    def find_issuing_authority(cert: x509.Certificate, disclosure_level: DisclosureLevel):
        if disclosure_level == DisclosureLevel.PrivateVenue:
            return cert.issuer.rfc4514_string()

        # TODO assume single result
        return cert.issuer.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value
