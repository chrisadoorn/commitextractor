const form_change = document.getElementById("change_form");
const akkoord_checkbox = document.getElementById("akkoord");


form_change.addEventListener("submit", (event) => {
    event.preventDefault();
    sendChangeData();
});

akkoord_checkbox.addEventListener("click", (event) => {
    akkoord_checkbox.checked
});

function sendChangeData() {
    const XHR = new XMLHttpRequest();

    // Bind the FormData object and the form element
    const FD = new FormData(form_change);

    // Define what happens on successful data submission
    XHR.addEventListener("load", (event) => {

    });

    // Define what happens in case of error
    XHR.addEventListener("error", (event) => {
        alert('Oops! Something went wrong.');
    });

    // Set up our request
    XHR.open("POST", "/change/save/");

    // The data sent is what the user provided in the form
    XHR.send(FD);
}


