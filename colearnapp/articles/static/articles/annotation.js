let log = console.log;

// enable tooltip
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
tooltipTriggerList.map(function (tooltipTriggerEl) {
    if (bootstrap) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    }
});

let annotationServiceURL = "https://annotations.mustafatulun.com/"
let chCountForPrefixSuffix = 20;
let minChCountToAnnotateText = 20;
let maxChCountToAnnotateText = 100;
let selection = null

function onFormAddBtnClick(event) {
    event.stopPropagation();

    let inputTitle = document.getElementById("annotation-form-input-title");
    let inputMessage = document.getElementById("annotation-form-input-message");

    let isValid = validateInputs(inputTitle, inputMessage)
    if (!isValid) {
        return
    }

    let selectedText = getSelectedText()
    log("selected text:" + selectedText)
    highlightSelectedText()

    let articleContent = document.getElementById("colearn-article").innerText.toString();

    log("article:" + articleContent)

    let prefix = findPrefix(selectedText, articleContent);
    let suffix = findSuffix(selectedText, articleContent);

    let value = {
        "title": inputTitle.value,
        "message": inputMessage.value
    }

    let payload = {
        "@context": "http://www.w3.org/ns/anno.jsonld",
        "type": "Annotation",
        "body": {
            "type": "TextualBody",
            "value": JSON.stringify(value),
            "format": "application/json",
            "language": "en"
        },
        "target": {
            "source": window.location.href,
            "selector": {
                "type": "TextQuoteSelector",
                "exact": selectedText,
                "prefix": prefix,
                "suffix": suffix
            }
        }
    }

    log("payload:" + JSON.stringify(payload))
    storeAnnotation(payload)
}

function storeAnnotation(payload) {
    let xhr = new XMLHttpRequest()
    let url = annotationServiceURL + extractURLPath() + "/"

    log('storeAnnotation url:' + url)

    xhr.open("POST", url)
    xhr.setRequestHeader('Content-Type', 'application/ld+json; profile="http://www.w3.org/ns/anno.jsonld"')
    xhr.send(JSON.stringify(payload))

    xhr.onload = () => {
        log('storeAnnotation status:' + xhr.status)
    }

    xhr.onreadystatechange = () => {
        if (xhr.readyState === 4) {
            log('storeAnnotation response:' + xhr.responseText);
        }
    }

    xhr.onerror = () => {
        console.error('storeAnnotation request failed')
    }
}

function extractURLPath() {
    let url = window.location.href.toString()
    let index = getPosition(url, "/", 3)
    let path = url.slice(index + 1, url.length)
    return path.replaceAll("/", "-")
}

function getPosition(string, subString, index) {
    return string.split(subString, index).join(subString).length;
}

function validateInputs(inputTitle, inputMessage) {
    let valid = true
    if (inputTitle.value.length === 0) {
        inputTitle.classList.add("annotation-form-input-warning")
        valid = false
    }
    if (inputMessage.value.length === 0) {
        inputMessage.classList.add("annotation-form-input-warning")
        valid = false
    }

    return valid
}

function highlightSelectedText() {
    let selectedText = selection.extractContents();
    let span = document.createElement("span");
    span.classList.add("annotated-text")
    span.appendChild(selectedText);
    selection.insertNode(span);
}


function findPrefix(target, content) {
    let targetIndex = content.search(target)
    let prefixIndex = targetIndex - chCountForPrefixSuffix
    if (prefixIndex < 0) {
        prefixIndex = 0
    }
    log('prefix index:' + prefixIndex)
    let prefix = content.slice(prefixIndex, targetIndex);
    log('prefix:' + prefix)
    return prefix
}

function findSuffix(target, content) {
    let targetIndex = content.search(target)

    let suffixStartIndex = (targetIndex + target.length)
    let suffixIndex = suffixStartIndex + chCountForPrefixSuffix
    if (suffixIndex > content.length) {
        suffixIndex = content.length - suffixStartIndex
    }
    log('suffix index:' + suffixIndex)
    let suffix = content.slice(suffixStartIndex, suffixIndex);
    log('suffix:' + suffix)
    return suffix
}

function getSelectedText() {
    let text = "";
    if (selection) {
        text = selection.toString();
    } else if (document.selection && document.selection.type !== "Control") {
        text = document.selection.createRange().text;
    }
    return text;
}

function onAddAnnotationBtnClick(event) {
    event.stopPropagation();
    removeButton()
    displayAnnotationForm(event.clientX, event.clientY)
    selection = window.getSelection().getRangeAt(0);
}

function displayAnnotationForm(x, y) {
    let annotationForm = document.getElementById("annotation-form");
    if (annotationForm.style.display === 'none' || annotationForm.style.display === '') {
        annotationForm.style.left = x + 'px';
        annotationForm.style.top = -180 + y + 'px';
        annotationForm.style.display = 'block';

        let closeBtn = document.getElementById("annotation-form-close-btn");
        closeBtn.addEventListener("click", removeAnnotationForm);

        let addBtn = document.getElementById("annotation-form-add-btn");
        addBtn.addEventListener("click", onFormAddBtnClick);
    }
}

function displayButton(x, y) {
    let floatingBtn = document.getElementById("floating-btn")
    if (floatingBtn.style.display === 'none' || floatingBtn.style.display === '') {
        floatingBtn.style.left = x + 'px';
        floatingBtn.style.top = y + 'px';
        floatingBtn.style.display = 'flex';
        floatingBtn.addEventListener("click", onAddAnnotationBtnClick)
    }
}

function removeButton() {
    let floatingBtn = document.getElementById("floating-btn")
    floatingBtn.style.display = 'none'
}

function removeAnnotationForm(event) {
    event.stopPropagation();
    let annotationForm = document.getElementById("annotation-form")
    annotationForm.style.display = 'none'

    let inputTitle = document.getElementById("annotation-form-input-title");
    let inputMessage = document.getElementById("annotation-form-input-message");
    inputTitle.classList.remove("annotation-form-input-warning")
    inputMessage.classList.remove("annotation-form-input-warning")
}

function checkSelection(event) {
    let selection = document.getSelection();
    let range = selection.rangeCount && selection.getRangeAt(0);

    if (range) {
        let selectionText = selection.toString();
        if (selectionText &&
            selectionText.length >= minChCountToAnnotateText &&
            selectionText.length < maxChCountToAnnotateText) {
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

