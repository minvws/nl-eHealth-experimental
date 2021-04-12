// jshint esversion:6
function setFhirFocus(fhir_id) {
    "use strict";
    const elemById = document.getElementById(fhir_id);
    if (null !== elemById) {
        elemById.focus();
    }
}
