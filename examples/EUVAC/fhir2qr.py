from fhir_query import FhirQueryImmunization
from immu_parser import ImmuEntryParser
from min_data_set import MinDataSet, MinDataSetFactory
from pprint import PrettyPrinter


def __extract_entry(qry_entry: dict):
    # General approach to processing the JSON: we just skip any JSON items that are not of interest to us
    # We are looking for resourceType of Immunization but we tread carefully, checking for existence
    # of keys at each step for two reasons:
    # 1. we can quickly skip over any entries that are not of interest - the sooner the better, and
    # 2. we don't want any JSON that we are not interested in to disturb our processing by raising
    # an InvalidKey exception which would be the case if we didn't explicitly check keys at each level
    # in the JSON hierarchy
    if "resource" in qry_entry:
        resource: dict = qry_entry["resource"]
        if "resourceType" in resource:
            if resource["resourceType"] == "Immunization":
                patient = FhirQueryImmunization.resolve_patient(resource=resource)
                min_data_set: MinDataSet = ImmuEntryParser.get_min_data_set(
                    resource=resource,
                    patient=patient,
                    disclosure_level=MinDataSetFactory.DisclosureLevel.MD,
                )
                print("min_data_set.pv/bc:")
                pp.pprint(min_data_set.pv)
                print("min_data_set.md:")
                pp.pprint(min_data_set.md)


if __name__ == "__main__":
    pp = PrettyPrinter(indent=2)
    qry_res = FhirQueryImmunization.find()
    if "entry" in qry_res:
        for entry in qry_res["entry"]:
            __extract_entry(qry_entry=entry)
    if "resourceType" in qry_res:
        if qry_res["resourceType"] == "Bundle":
            total_matches = qry_res["total"]
            print(f"\n ** Total FHIR query matches found: {total_matches} **")
