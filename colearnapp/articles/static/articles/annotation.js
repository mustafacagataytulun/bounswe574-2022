// enable tooltip
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
tooltipTriggerList.map(function (tooltipTriggerEl) {
    if (bootstrap) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    }
});


function onClick(event) {
    console.log("click")
    removeButton()
    console.log('x:' + event.clientX)
    console.log('y:' + event.clientY)
    displayAnnotationForm(event.clientX, event.clientY)
}

function displayAnnotationForm(x, y) {
    let annotationForm = document.getElementById("annotation-form");
    if (annotationForm.style.display === 'none' || annotationForm.style.display === '') {
        annotationForm.style.left = x + 'px';
        annotationForm.style.top = y + 'px';
        annotationForm.style.display = 'block';
        let closeBtn = document.getElementById("annotation-form-close-btn");
        closeBtn.addEventListener("click", removeAnnotationForm);
    }
}

function displayButton(x, y) {
    let floatingBtn = document.getElementById("floating-btn")
    if (floatingBtn.style.display === 'none' || floatingBtn.style.display === '') {
        floatingBtn.style.left = x + 'px';
        floatingBtn.style.top = y + 'px';
        floatingBtn.style.display = 'flex';
        floatingBtn.addEventListener("click", onClick)
    }
}

function removeButton() {
    let floatingBtn = document.getElementById("floating-btn")
    floatingBtn.style.display = 'none'
}

function removeAnnotationForm() {
    let annotationForm = document.getElementById("annotation-form")
    annotationForm.style.display = 'none'
}

function checkSelection(event) {
    let selection = document.getSelection();
    let range = selection.rangeCount && selection.getRangeAt(0);

    if (range) {
        let selectionText = selection.toString();
        if (selectionText) {
            let endContainer = range.endContainer;
            console.log('node type:' + endContainer.nodeType)
            console.log("selection:" + selectionText)
            console.log('x:' + event.clientX)
            console.log('y:' + event.clientY)
            displayButton(event.clientX, event.clientY)
        } else {
            removeButton();
        }
    } else {
        removeButton();
    }
}

document.addEventListener("mouseup", checkSelection);
document.addEventListener("keyup", checkSelection);

