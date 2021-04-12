import json
import pytest
from cryptography import x509

from DisclosureLevel import DisclosureLevel
from min_data_set import MinDataSet, MinDataSetFactory
from pathlib import Path
from typing import List


class TestMinDataSetPV:
    # factory tested separately, no need to re-test here
    def test_dict(self):
        with open(Path(Path(__file__).parent.resolve(), "test_min_data_set.json"), "r") as f:
            qry_res: dict = json.load(f)
            min_data_set: MinDataSet = MinDataSetFactory.create(DisclosureLevel.PrivateVenue)
            cert = TestMinDataSetPV.readCertificate()
            min_data_set.parse(qry_res, cert)
            min_data: List[dict] = min_data_set.as_dict_array()
            assert min_data is not None
            # TODO: validate fields in min_data

    def test_json(self):
        pass

    def test_jsonld(self):
        with open(Path(Path(__file__).parent.resolve(), "test_min_data_set.json"), "r") as f:
            qry_res: dict = json.load(f)
            min_data_set: MinDataSet = MinDataSetFactory.create(DisclosureLevel.PrivateVenue)
            cert = TestMinDataSetPV.readCertificate()
            min_data_set.parse(qry_res, cert)
            min_data: dict = min_data_set.as_jsonld()
            assert min_data is not None

    @staticmethod
    def readCertificate():
        with open("dsc-worker.pem", "rb") as file:
            pem = file.read()
        cert = x509.load_pem_x509_certificate(pem)
        return cert

@pytest.mark.skip(reason="changing data member fields")
class TestMinDataSetBC:
    # factory tested separately, no need to re-test here
    # pv tested separately, no need to re-test here
    def test_fields_bc(self):
        uvci_expected = "12NL12327JFEGE"
        min_data_set: MinDataSet = MinDataSetFactory.create(DisclosureLevel.BC)
        # min_data_set.certificate.UVCI = uvci_expected   # we should be able to set default None to a valid value
        # assert uvci_expected == min_data_set.certificate.UVCI


@pytest.mark.skip(reason="changing data member fields")
class TestMinDataSetMD:
    # factory tested separately, no need to re-test here
    # pv tested separately, no need to re-test here
    # bc tested separately, no need to re-test here
    def test_fields_md(self):
        min_data_set: MinDataSet = MinDataSetFactory.create(DisclosureLevel.MD)
        # assert min_data_set.md is not None
        # assert isinstance(min_data_set.md, dict)
        # # all md fields should initially be empty, also should be readable
        # md: dict = min_data_set.md
        # assert not md["dateOfBirth"]
        # assert not md["marketingAuthorizationHolder"]
        # assert not md["vaccineCode"]
        # assert not md["vaccineMedicinalProduct"]
        # assert not md["batchLotNumber"]
        # assert not md["numberInSeries"]
        # assert not md["dateOfVaccination"]
        # assert not md["administeringCentre"]
        # assert not md["healthProfessionalId"]
        # assert not md["countryOfVaccination"]
        # assert not md["personId"]
        # assert not md["nextVaccinationDate"]
        # # with the exception of gender, which should be set to "O" by default
        # assert md["gender"] == "O"
        # # although .md itself is a read-only prop, we should be able to write to its fields:
        # md["personId"] = "ABC"
