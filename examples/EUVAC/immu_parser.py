from min_data_set import Gender, MinDataSet, MinDataSetFactory


def _map_patient_gender(gender: str) -> Gender:
    # often localization specific, we'll assume US English
    ret_gender: Gender = Gender.O  # default case until we know otherwise
    if gender and len(gender) > 0:
        g = gender[0]
        if g == "F":
            ret_gender = Gender.F
        elif g == "M":
            ret_gender = Gender.M
    return ret_gender


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

    @staticmethod
    def get_min_data_set(
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
            pv["legalName"] = patient["name"]
            pv["diseaseOrAgentTargeted"] = dat
            pv["startDateOfValidity"] = "2019-12-31"

        if (
            disclosure_level == MinDataSetFactory.DisclosureLevel.BC
            or disclosure_level == MinDataSetFactory.DisclosureLevel.MD
        ):
            min_data_set.certificate.UVCI = "Unknown"  # Need this from an IIS

        if disclosure_level == MinDataSetFactory.DisclosureLevel.MD:
            md: dict = min_data_set.md
            # patient
            md["personId"] = patient["identifier"]
            md["gender"] = _map_patient_gender(gender=patient["gender"])
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
