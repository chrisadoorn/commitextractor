const dialogEle = document.getElementById("dialogEle");
const launchBtn = document.getElementById("launchDialog");
const formResult = document.getElementById("formResult");
if(dialogEle && launchBtn && formResult) {
    dialogEle.addEventListener("close", () => {
        formResult.textContent = dialogEle.returnValue;
    });
}


function newSrc(newSrc,project_name) {
    dialogEle.showModal()
    document.getElementById("MyFrame").src = newSrc;
    document.getElementById("aantekeningen").innerHTML = project_name;
}
