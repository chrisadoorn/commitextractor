const dialogEle = document.getElementById("dialogEle");
const idproject = document.getElementById("idproject");
const comment = document.getElementById("comment");
const type_of_project = document.getElementById("type_of_project");
const exclude = document.getElementById("exclude");
const exclude_reason = document.getElementById("exclude_reason");
const form = document.getElementById("manual_comments_form");
const close_modal = document.getElementById("close_modal");


form.addEventListener("submit", (event) => {
    event.preventDefault();
    sendData();
});

close_modal.addEventListener("click", (event) => {
    event.preventDefault();
    closeDialog();
});

dialogEle.addEventListener("click", (event) => {
    if (!event.target.closest('div')) {
        closeDialog();
    }
});


function newSrc(project_id) {
    dialogEle.showModal()
    getRemarks(project_id)
}

function closeDialog() {
    dialogEle.close();
}

function getRemarks(project_id) {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/manual_comments/save/?mc_id=" + project_id)
    xhr.send();
    xhr.responseType = "json";
    xhr.onload = () => {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const data = xhr.response;
            idproject.value = data.idproject || ""
            comment.value = data.comment || "";
            type_of_project.value = data.type_of_project || "";
            exclude.value = data.exclude || false;
            exclude_reason.value = data.exclude_reason || "";
        } else {
            console.log(`Error: ${xhr.status}`);
        }
    };
}


function sendData() {
    const XHR = new XMLHttpRequest();


    // Bind the FormData object and the form element
    const FD = new FormData(form);




    // Define what happens on successful data submission
    XHR.addEventListener("load", (event) => {
        //alert(event.target.responseText);
        closeDialog()
    });

    // Define what happens in case of error
    XHR.addEventListener("error", (event) => {
        alert('Oops! Something went wrong.');
    });

    // Set up our request
    XHR.open("POST", "/manual_comments/save/");

    // The data sent is what the user provided in the form
    XHR.send(FD);
}

