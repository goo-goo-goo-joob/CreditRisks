function error_handler(jqXHR, exception) {
    if (jqXHR.status === 400) {
        alert(jqXHR.statusText + " " + jqXHR.responseText);
    } else {
        alert(jqXHR.statusText + " " + jqXHR.status);
    }
    console.log(jqXHR.statusText + " " + jqXHR.status + "\n" + jqXHR.responseText);
}