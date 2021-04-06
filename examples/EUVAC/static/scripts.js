function import_url() {
    const te = document.getElementById('fhir');
    const ue = document.getElementById('url');
    const url = ue.value;

    console.log("fetching " + url);

    te.value = "...fetching";
    fetch(url)
        .then(function (reply) {
            reply.text().then(function (payload) {
                te.value = payload;
            });
            console.log("ok");
        })
        .catch(function (err) {
            console.log("fetching " + url + " failed: " + err);
        });
}

function fhir_query_res(elementId) {
    fetch("fhir_query_res.json")
        .then(response => {
            return response.text()
        })
        .then(data => {
            document.getElementById(elementId).value = data;
        });
}
