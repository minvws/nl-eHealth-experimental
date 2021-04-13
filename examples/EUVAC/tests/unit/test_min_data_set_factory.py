from disclosure_level import DisclosureLevel
from min_data_set import MinDataSet, MinDataSetPV, MinDataSetBC, MinDataSetMD, MinDataSetFactory


class TestMinDataSetFactory:
    def test_inheritance_hierarchy(self):
        assert issubclass(MinDataSetPV, MinDataSet)
        assert issubclass(MinDataSetBC, MinDataSet)
        assert issubclass(MinDataSetMD, MinDataSet)

    def test_create_pv(self):
        min_data_set: MinDataSet = MinDataSetFactory.create(DisclosureLevel.PrivateVenue)
        assert min_data_set is not None
        assert isinstance(min_data_set, MinDataSet)
        assert isinstance(min_data_set, MinDataSetPV)
        assert not isinstance(min_data_set, MinDataSetBC)
        assert not isinstance(min_data_set, MinDataSetMD)

    def test_create_bc(self):
        min_data_set: MinDataSet = MinDataSetFactory.create(DisclosureLevel.BorderControl)
        assert min_data_set is not None
        assert isinstance(min_data_set, MinDataSet)
        assert not isinstance(min_data_set, MinDataSetPV)
        assert isinstance(min_data_set, MinDataSetBC)
        assert not isinstance(min_data_set, MinDataSetMD)

    def test_create_md(self):
        min_data_set: MinDataSet = MinDataSetFactory.create(DisclosureLevel.Medical)
        assert min_data_set is not None
        assert isinstance(min_data_set, MinDataSet)
        assert not isinstance(min_data_set, MinDataSetPV)
        assert not isinstance(min_data_set, MinDataSetBC)
        assert isinstance(min_data_set, MinDataSetMD)

