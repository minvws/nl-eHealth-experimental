import json
import pytest

from immu_parser import ImmuEntryParser
from min_data_set import (
    Certificate,
    MinDataSet,
    MinDataSetPV,
    MinDataSetBC,
    MinDataSetMD,
    MinDataSetFactory,
)
from pathlib import Path
from typing import Optional


class TestImmuParser:
    # we expect JSON test data to be in same dir as test script
    JSON_TEST_DATA: Path = Path(
        Path(__file__).parent.resolve(), "test_immu_parser.json"
    )

    def test_load_json_pv(self):
        with open(TestImmuParser.JSON_TEST_DATA, "r") as f:
            json_data: dict = json.load(f)
            assert json_data
            # we extract the first entry only from the Bundle, as tests same for all instances
            assert "entry" in json_data
            assert "resource" in json_data["entry"][0]
            qry_entry: dict = json_data["entry"][0]
            assert qry_entry
            assert isinstance(qry_entry, dict)
            min_data_set: Optional[MinDataSet] = ImmuEntryParser.extract_entry(
                qry_entry=qry_entry,
                disclosure_level=MinDataSetFactory.DisclosureLevel.PV,
            )
            assert min_data_set is not None
            assert min_data_set != Optional[None]
            # the following isinstance etc checks are, in essence, re-checking the MinDataSetFactory.create method
            # but MinDataSetFactory.create is not visible at this level, so we re-check rather than assume
            assert isinstance(min_data_set, MinDataSet)
            assert isinstance(min_data_set, MinDataSetPV)
            assert not isinstance(min_data_set, MinDataSetBC)
            assert not isinstance(min_data_set, MinDataSetMD)
            # .md field should be unset for PV disclosure level
            with pytest.raises(RuntimeError) as ex_run:
                min_data_set.md.personId = "abc"
            assert "property md not supported for concrete type" in str(ex_run.value)
            # test data specific to disclosure level PV (JSON test data can be found in TestImmuParser.JSON_TEST_DATA)
            pv = min_data_set.pv
            assert "D.A." == pv["legalName"]

    def test_load_json_bc(self):
        pass

    def test_load_json_md(self):
        pass
