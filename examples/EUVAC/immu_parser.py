import json
from enum import auto, Enum


class ImmuEntryParser:

    """ImmuEntryParser

    An "entry" corresponds to an instance of the FHIR Immunization model v4.x given at
     https://www.hl7.org/fhir/immunization.html

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

    foreach entry:
        1. check it is a resource
        2. check its resourceType (must be Immunization given the FHIR query, if not then something strange...)
        3. pick up the fields required as per Annex 1 spec (eHN) wrt desired level of disclosure
    """

    class DisclosureLevel(Enum):
        """Enum for disclosure level. The disclosure level is representative
        of the intended use of the vaccination certificate and governs in accordance
        with the EU eHealthNetwork Annex 1 Minimum Dataset Specification for
        Vaccination Certificates
        """

        PV = auto()  # private venue, level 0
        BC = auto()  # border control, level 1
        MD = auto()  # medical, level 2

    @staticmethod
    def json(entry: dict, patient: dict, disclosure_level: DisclosureLevel) -> str:
        """
        :param entry: a (nested) dict structure (usually created via json module from JSON str)
        :type entry: dict
        :param patient: the resolved FHIR reference to patient
        :type entry: dict
        :param disclosure_level: controls the amount of data generated in the output JSON
        :type disclosure_level: :class: DisclosureLevel
        :return: JSON containing a much reduced version of the input entry,
        as a function of disclosure_level
        :rtype: str
        """

        # always present:
        disclosure_entry = {
            "LegalName": patient["name"],
            "DiseaseOrAgentTargeted": entry["protocolApplied"]["targetDisease"],
        }

        # patient
        if disclosure_level == ImmuEntryParser.DisclosureLevel.MD:
            disclosure_entry["PersonID"] = patient["identifier"]
            disclosure_entry["AdministrativeGender"] = patient["gender"]
            disclosure_entry["DateOfBirth"] = patient["birthDate"]

        # vaccine
        if disclosure_level == ImmuEntryParser.DisclosureLevel.MD:
            disclosure_entry["VaccineProphylaxis"] = entry["vaccineCode"]
            # ...

        # vaccine cert
        # TODO: this is the more difficult one: no standardized IIS interface for the information

        return json.dumps(disclosure_entry)
