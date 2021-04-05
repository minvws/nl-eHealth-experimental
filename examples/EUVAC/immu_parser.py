from min_data_set import MinDataSet, MinDataSetFactory
from fhir_query import FhirQueryImmunization
from pprint import PrettyPrinter
from typing import Optional


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

    pp = PrettyPrinter(indent=2)

    @staticmethod
    def extract_entry(qry_entry: dict, disclosure_level: MinDataSetFactory.DisclosureLevel) -> Optional[MinDataSet]:
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
                    min_data_set: MinDataSet = ImmuEntryParser.__get_min_data_set(
                        resource=resource,
                        patient=patient,
                        disclosure_level=disclosure_level,
                    )
                    return min_data_set
        return None

    @staticmethod
    def __get_min_data_set(
        resource: dict,
        patient: dict,
        disclosure_level: MinDataSetFactory.DisclosureLevel,
    ) -> MinDataSet:
        """
        :param resource: a (nested) dict structure representing one item of { entry.resource }
        :type resource: dict
        :param patient: the resolved FHIR reference to patient
        :type entry: dict
        :param disclosure_level: controls the amount of data generated in the output JSON
        :type disclosure_level: :class: DisclosureLevel
        :return: MinDataSet derived class corresponding to the disclosure level
        :rtype: MinDataSet 
        :exception: ValueError if resourceType is not "Immunization"
        """
        if resource["resourceType"] != "Immunization":
            raise ValueError(
                f'resource["resourceType"] expected to be "Immunization", is: {resource["resourceType"]}'
            )

        min_data_set: MinDataSet = MinDataSetFactory.create(
            disclosure_level=disclosure_level
        )

        # TODO: populate min_data_set
        if (
            "protocolApplied" in resource
            and "targetDisease" in resource["protocolApplied"]
        ):
            dat = resource["protocolApplied"]["targetDisease"]
        else:
            dat = "Unknown"

        if (
            disclosure_level == MinDataSetFactory.DisclosureLevel.PV
            or disclosure_level == MinDataSetFactory.DisclosureLevel.BC
            or disclosure_level == MinDataSetFactory.DisclosureLevel.MD
        ):
            pv: dict = min_data_set.pv
            # no validation checking for the following lines accessing "patient", allow exceptions to propagate
            # e.g. it is _expected_ that "name" is present in patient, if not it is an error
            # it is also expected that the name parts "given" and "family" are at least 1 character, etc
            patient_name: dict = patient["name"]
            pv["legalName"] = f'{patient_name["given"][0][0]}.{patient_name["family"][0]}.'
            pv["diseaseOrAgentTargeted"] = dat
            pv["startDateOfValidity"] = "YYYY-MM-DD"

        if (
            disclosure_level == MinDataSetFactory.DisclosureLevel.BC
            or disclosure_level == MinDataSetFactory.DisclosureLevel.MD
        ):
            min_data_set.certificate.UVCI = "Unknown"  # Need this from an IIS

        if disclosure_level == MinDataSetFactory.DisclosureLevel.MD:
            md: dict = min_data_set.md
            # patient
            md["personId"] = patient["identifier"]
            md["gender"] = patient["gender"]
            md["dateOfBirth"] = patient["birthDate"]
            # TODO: vaccine
            md["marketingAuthorizationHolder"] = ""
            md["vaccineCode"] = resource["vaccineCode"]["coding"]
            md["vaccineMedicinalProduct"] = ""
            md["batchLotNumber"] = ""
            md["dateOfVaccination"] = ""
            md["administeringCentre"] = ""
            md["healthProfessionalId"] = ""
            md["countryOfVaccination"] = ""
            md["numberInSeries"] = ""
            md["nextVaccinationDate"] = ""

        # vaccine cert
        # # TODO: this is the more difficult one: no standardized IIS interface for the information
        min_data_set.certificate.issuer = ""

        return min_data_set
