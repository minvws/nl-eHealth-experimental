import pytest

from min_data_set import Certificate, MinDataSet, MinDataSetPV, MinDataSetBC, MinDataSetMD, MinDataSetFactory
from typing import Optional


class TestMinDataSetFactory:
    def test_inheritance_hierarchy(self):
        assert issubclass(MinDataSetPV, MinDataSet)
        assert issubclass(MinDataSetBC, MinDataSetPV)
        assert issubclass(MinDataSetMD, MinDataSetBC)

    def test_create_pv(self):
        min_data_set: MinDataSet = MinDataSetFactory.create(MinDataSetFactory.DisclosureLevel.PV)
        assert min_data_set is not None
        assert isinstance(min_data_set, MinDataSet)
        assert isinstance(min_data_set, MinDataSetPV)
        assert not isinstance(min_data_set, MinDataSetBC)
        assert not isinstance(min_data_set, MinDataSetMD)
        with pytest.raises(RuntimeError) as ex_run:
            min_data_set.md.personId = "abc"
        assert "property md not supported for concrete type" in str(ex_run.value)

    def test_create_bc(self):
        min_data_set: MinDataSet = MinDataSetFactory.create(MinDataSetFactory.DisclosureLevel.BC)
        assert min_data_set is not None
        assert isinstance(min_data_set, MinDataSet)
        assert isinstance(min_data_set, MinDataSetBC)
        assert not isinstance(min_data_set, MinDataSetMD)
        with pytest.raises(RuntimeError) as ex_run:
            min_data_set.md.personId = "abc"
        assert "property md not supported for concrete type" in str(ex_run.value)

    def test_create_md(self):
        min_data_set: MinDataSet = MinDataSetFactory.create(MinDataSetFactory.DisclosureLevel.MD)
        assert min_data_set is not None
        assert isinstance(min_data_set, MinDataSet)
        assert isinstance(min_data_set, MinDataSetMD)


class TestMinDataSetPV:
    # factory tested separately, no need to re-test here
    def test_fields_pv(self):
        min_data_set: MinDataSet = MinDataSetFactory.create(MinDataSetFactory.DisclosureLevel.PV)
        assert min_data_set.certificate is not None
        assert isinstance(min_data_set.certificate, Certificate)
        vacc_cert: Certificate = min_data_set.certificate
        assert vacc_cert.UVCI == Optional[None]     # NOTE: "== Optional[None]" not the same as "is not None"
        assert min_data_set.pv is not None
        pv = min_data_set.pv
        assert isinstance(pv, dict)
        assert "legalName" in pv
        assert "diseaseOrAgentTargeted" in pv
        assert "startDateOfValidity" in pv


class TestMinDataSetBC:
    # factory tested separately, no need to re-test here
    # pv tested separately, no need to re-test here
    def test_fields_bc(self):
        uvci_expected = "12NL12327JFEGE"
        min_data_set: MinDataSet = MinDataSetFactory.create(MinDataSetFactory.DisclosureLevel.BC)
        min_data_set.certificate.UVCI = uvci_expected   # we should be able to set default None to a valid value
        assert uvci_expected == min_data_set.certificate.UVCI


class TestMinDataSetMD:
    # factory tested separately, no need to re-test here
    # pv tested separately, no need to re-test here
    # bc tested separately, no need to re-test here
    def test_fields_md(self):
        min_data_set: MinDataSet = MinDataSetFactory.create(MinDataSetFactory.DisclosureLevel.MD)
        assert min_data_set.md is not None
        assert isinstance(min_data_set.md, dict)
        # all md fields should initially be empty, also should be readable
        md: dict = min_data_set.md
        assert not md["dateOfBirth"]
        assert not md["marketingAuthorizationHolder"]
        assert not md["vaccineCode"]
        assert not md["vaccineMedicinalProduct"]
        assert not md["batchLotNumber"]
        assert not md["numberInSeries"]
        assert not md["dateOfVaccination"]
        assert not md["administeringCentre"]
        assert not md["healthProfessionalId"]
        assert not md["countryOfVaccination"]
        assert not md["personId"]
        assert not md["nextVaccinationDate"]
        # with the exception of gender, which should be set to "O" by default
        assert md["gender"] == "O"
        # although .md itself is a read-only prop, we should be able to write to its fields:
        md["personId"] = "ABC"
