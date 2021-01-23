import immunization_pb2


def build_immunization() -> immunization_pb2.Immunization:
    immu = immunization_pb2.Immunization()
    immu.resourceType = "Immunization"
    immu.id = "example"
    immu.identifier.system = "urn:ietf:rfc:3986"
    immu.identifier.value = "urn:oid:1.3.6.1.4.1.21367.2005.3.7.1234"
    immu.status = "completed"
    immu.vaccineCode.coding.system = "urn:oid:1.2.36.1.2001.1005.17"
    immu.vaccineCode.coding.code = "FLUVAX"
    immu.vaccineCode.text = "Fluvax (Influenza)"
    immu.patient.reference = "Patient/example"
    immu.encounter.reference = "Encounter/example"
    immu.occurrenceDateTime = "2013-01-10"
    immu.primarySource = True
    immu.location.reference = "Location/1"
    immu.manufacturer.reference = "Organization/hl7"
    immu.lotNumber = "AAJN11K"
    immu.expirationDate = "2015-02-15"
    immu.site.coding.system = "http://terminology.hl7.org/CodeSystem/v3-ActSite"
    immu.site.coding.code = "LA"
    immu.site.coding.display = "left arm"
    immu.route.coding.system = "http://terminology.hl7.org/CodeSystem/v3-RouteOfAdministration"
    immu.route.coding.code = "ÏM"
    immu.route.coding.display = "Injection, intramuscular"
    immu.doseQuantity.value = 5
    immu.doseQuantity.system = "http://unitsofmeasure.org"
    immu.doseQuantity.code = "mg"
    immu.performer.function.coding.system = "http://terminology.hl7.org/CodeSystem/v2-0443"
    immu.performer.function.coding.code = "OP"
    immu.performer.actor.reference = "Practitioner/example"
    immu.performer.function.coding.system = "http://terminology.hl7.org/CodeSystem/v2-0443"
    immu.performer.function.coding.code = "AP"
    immu.performer.actor.reference = "Practitioner/example"
    immu.note.text = "Notes on adminstration of vaccine"
    immu.reasonCode.coding.system = "http://snomed.info/sct"
    immu.reasonCode.coding.code = "429060002"
    immu.isSubpotent = True
    immu.education.documentType = "253088698300010311120702"
    immu.education.publicationDate = "2012-07-02"
    immu.education.presentationDate = "2013-01-10"
    immu.programEligibility.coding.system = "http://terminology.hl7.org/CodeSystem/immunization-program-eligibility"
    immu.programEligibility.coding.code = "ineligible"
    immu.fundingSource.coding.system = "http://terminology.hl7.org/CodeSystem/immunization-funding-source"
    immu.fundingSource.coding.code = "private"
    return immu


if __name__ == "__main__":
    immu = build_immunization()
    with open("immunization.bin", "wb") as f:
        f.write(immu.SerializeToString())
