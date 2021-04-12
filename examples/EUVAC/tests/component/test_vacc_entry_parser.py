import json

from cryptography import x509

from DisclosureLevel import DisclosureLevel
from pathlib import Path
from vacc_entry_parser import VaccEntryParser


class TestVaccEntryParser:
    # we expect JSON test data to be in same dir as test script
    JSON_TEST_DATA: Path = Path(
        #TODO handle unicode in - Path(__file__).parent.resolve(), "test_vacc_entry_parser.json"
        Path(__file__).parent.resolve(), "test_immu_parser.json"
    )

    @staticmethod
    def readCertificate():
        with open("dsc-worker.pem", "rb") as file:
            pem = file.read()
        cert = x509.load_pem_x509_certificate(pem)
        return cert

    def test_load_json_pv(self):
        with open(TestVaccEntryParser.JSON_TEST_DATA, "r") as f:
            json_data: dict = json.load(f)
            assert json_data
            # we extract the first entry only from the Bundle, as tests same for all instances
            assert "entry" in json_data
            assert "resource" in json_data["entry"][0]
            qry_entry: dict = json_data["entry"][0]
            assert qry_entry
            assert isinstance(qry_entry, dict)
            cert = TestVaccEntryParser.readCertificate()
            entry_parser: VaccEntryParser = VaccEntryParser(json_data, cert)
            pv: dict = entry_parser.resolve_entry(
                entry=qry_entry, disclosure_level=DisclosureLevel.PrivateVenue
            )
            # TODO: check data values are as expected wrt the source data

    def test_load_json_bc(self):
        pass

    def test_load_json_md(self):
        pass
