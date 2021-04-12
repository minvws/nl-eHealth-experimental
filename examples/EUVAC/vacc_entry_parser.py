from DisclosureLevel import DisclosureLevel


class VaccEntryParser:

    """VaccEntryParser

    An "entry" corresponds to an instance of the FHIR Immunization model v4.x given at
     https://www.hl7.org/fhir/immunization.html

    ASSUMPTION: the FHIR result given here has all references included (server-side) in the response
    document via the use of _include= in the FHIR query.

    A FHIR Immumization resource query such as:
        HTTP header = "Accept": "application/fhir+json"
        GET: {https://SERVICE_ROOT_URL}/Immunization?_summary=data&date=ge2021-01-01
    delivers a (JSON) response for Immunization results according to the following (simplified) structure:
    {
        'resourceType': 'Bundle',
        'total': '28',
        'entry': [
            'resource': {
                'resourceType': 'Immunization',
                'doseQuantity: 'nnn',
                occurrenceDateTime: '2021-03-08',
                ...
            }
        ]
    }

    You will have a total of 28 entry records. These are paged, so usually not all present in this chunk of
    response, you will need to use the standard FHIR paging link[ 'relation': 'next' ] to move to next etc.
    (You can influence the paging but that's going O.T. here - look up paging support in FHIR if interested)
    """

    def __init__(self, qry_res: dict):
        """
        :param qry_res: the result of a FHIR query contained as a dict (result of e.g.json.loads()) -
        note that this has to be whole response document as we will need to resolve references from
        within the Immunization resource to other resources contained in the document (e.g. Patient)
        but only pointed to from the Immunization resource
        :type qry_res: dict
        """
        self.__qry_res: dict = qry_res

    def resolve_entry(
        self, entry: dict, disclosure_level: DisclosureLevel
    ) -> dict:
        """
        :param entry: one specific entry in the FHIR results to be resolved
        for entry:
            1. check its resourceType => must be Immunization, ignore anything else
            2. pick up the fields required as per Annex 1 spec (eHN) wrt desired level of disclosure
        :type entry: dict
        :param disclosure_level: Disclosure Level according to EU eHealthNetwork Annex 1 Minimum Data Set
        :type disclosure_level: MinDataSetFactory.DisclosureLevel
        :return: EU eHealthNetwork Annex 1 Minimum Data Set for the given disclosure level
        :rtype: dict
        """
        is_immunization_entry = VaccEntryParser.__is_immunization_entry(entry)
        if not is_immunization_entry:
            return {}
        resolved_entry: dict = self.__extract_entry(
            entry=entry, disclosure_level=disclosure_level
        )
        return resolved_entry

    @staticmethod
    def __is_immunization_entry(entry: dict) -> bool:
        is_immu_entry: bool = (
            entry is not None
            and "resource" in entry
            and "resourceType" in entry["resource"]
            and "Immunization" == entry["resource"]["resourceType"]
        )
        return is_immu_entry

    def __extract_entry(
        self, entry: dict, disclosure_level: DisclosureLevel
    ) -> dict:
        ret = {}
        dat: str = VaccEntryParser.__get_dat(entry=entry)
        patient: dict = self.__resolve_patient(entry=entry)

        if (
            disclosure_level == DisclosureLevel.PrivateVenue
            or disclosure_level == DisclosureLevel.BorderControl
            or disclosure_level == DisclosureLevel.Medical
        ):
            # no validation checking for the following lines accessing "patient", allow exceptions to propagate
            # e.g. it is _expected_ that "name" is present in patient, if not it is an error
            # it is also expected that the name parts "given" and "family" are at least 1 character, etc
            # We take first entry for "name" as this is the "default" name if multiple present
            patient_name: dict = patient["nam"][0]
            ret.update(
                {
                    "nam": f'{patient_name["given"][0][0]}.{patient_name["family"][0]}.',
                    "dat": dat,
                    "gen": patient["gen"],
                }
            )

        if (
            disclosure_level == DisclosureLevel.BorderControl
            or disclosure_level == DisclosureLevel.Medical
        ):
            pass

        if disclosure_level == DisclosureLevel.Medical:
            pass

        # vaccine cert
        # # TODO: this is the more difficult one: no standardized IIS interface for the information
        return ret

    def __resolve_patient(self, entry: dict) -> dict:
        # patient as per https://build.fhir.org/ig/hl7-eu/dgc/StructureDefinition-Patient-dgc.html
        if VaccEntryParser.__entry_has_immu_patient_ref(entry=entry):
            patient_url: str = entry["resource"]["patient"]["reference"]
            patient: dict = VaccEntryParser.__locate_resource(
                qry_res=self.__qry_res, resource_relative_url=patient_url
            )
        else:
            patient: dict = entry["resource"]["patient"]
        return {
            "nam": patient["name"],
            "birthDate": patient["birthDate"],
            "gen": "U",  # should be patient["gender"], but currently not available from FHIR resource
            "pid": patient["identifier"],
        }

    @staticmethod
    def __get_dat(entry: dict) -> str:
        resource: dict = entry["resource"]  # allow InvalidKey exception to propagate
        if (
            "protocolApplied" in resource
            and "targetDisease" in resource["protocolApplied"]
        ):
            dat = resource["protocolApplied"]["targetDisease"]
        else:
            dat = "Unknown"
        return dat

    @staticmethod
    def __entry_has_immu_patient_ref(entry: dict) -> bool:
        return (
            "resource" in entry
            and "resourceType" in entry["resource"]
            and "patient" in entry["resource"]
            and "Immunization" == entry["resource"]["resourceType"]
            and "reference" in entry["resource"]["patient"]
        )

    @staticmethod
    def __locate_resource(qry_res: dict, resource_relative_url: str) -> dict:
        # pre-cond: qry_res already checked for containing "entry" elements
        # thus allow InvalidKey exception to propagate if needed
        for entry in qry_res["entry"]:
            if entry["fullUrl"].endswith(resource_relative_url):
                return entry["resource"]
        # data error if we cannot find the resource_relative_url *somewhere* in the
        # JSON received from FHIR with _include=*
        raise ValueError(f"Cannot find fullUrl {resource_relative_url} in FHIR response entries")
