let log = console.log;


let annotationServiceURL = "https://annotations.mustafatulun.com/annotations/"
let chCountForPrefixSuffix = 20;
let minChCountToAnnotateText = 20;
let maxChCountToAnnotateText = 100;
let selection = null
let allAnnotations = []

function onFormAddBtnClick(event) {
    event.stopPropagation();

    let inputMessage = document.getElementById("annotation-form-input-message");

    let isValid = validateInputs(inputMessage)
    if (!isValid) {
        return
    }

    let selectedText = getSelectedText()
    log("selected text:" + selectedText)

    let articleContent = document.getElementById("colearn-article").innerHTML.toString();
    // let articleContent = document.documentElement.outerHTML;

    log("article:" + articleContent)

    let prefix = findPrefix(selectedText, articleContent);
    let suffix = findSuffix(selectedText, articleContent);

    let payload = {
        "@context": "http://www.w3.org/ns/anno.jsonld",
        "type": "Annotation",
        "body": {
            "type": "TextualBody",
            "value": inputMessage.value,
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

function storeAnnotation(payload, selectedText) {
    let xhr = insertAnnotation(payload)

    xhr.onload = () => {
        log('insertAnnotation status:' + xhr.status)
    }

    xhr.onreadystatechange = () => {
        if (xhr.readyState === 4) {
            log('insertAnnotation response:' + xhr.responseText);
            let responseJson = JSON.parse(xhr.responseText)
            highlightSelectedText(selectedText, responseJson["id"])
        }
    }

    xhr.onerror = () => {
        console.error('insertAnnotation request failed')
    }

    return xhr
}

function insertAnnotation(payload) {
    let xhr = new XMLHttpRequest()

    xhr.open("POST", annotationServiceURL)
    xhr.setRequestHeader('Content-Type', 'application/ld+json; profile="http://www.w3.org/ns/anno.jsonld"')
    xhr.send(JSON.stringify(payload))

    return xhr
}

function deleteAnnotation(url) {
    let xhr = new XMLHttpRequest()

    xhr.open("DELETE", url)
    xhr.send()

    return xhr
}

function fetchAnnotations(page) {
    let xhr = new XMLHttpRequest()

    let target = encodeURIComponent(window.location.href.toString())

    log('target:' + target)

    xhr.open("GET", annotationServiceURL + "?page=" + page + "&target=" + target)
    xhr.setRequestHeader('Content-Type', 'application/ld+json; profile="http://www.w3.org/ns/anno.jsonld"')
    xhr.send()

    return xhr
}

function validateInputs(inputMessage) {
    if (inputMessage.value.length === 0) {
        inputMessage.classList.add("annotation-form-input-warning")
        return false
    }
    return true
}

function highlightSelectedText(message, id) {
    let selectedText = selection.extractContents();
    let span = document.createElement("span");

    let spanId = createSpanId(id)
    span.classList.add("annotated-text")
    span.setAttribute("id", spanId)
    span.setAttribute("data-bs-toggle", "tooltip")
    span.setAttribute("data-bs-placement", "top")
    span.setAttribute("title", message)
    span.appendChild(selectedText);

    let button = document.createElement("button")
    button.classList.add("btn")
    button.classList.add("btn-danger")
    button.classList.add("bi")
    button.classList.add("bi-trash")
    button.classList.add("annotation-delete")
    button.setAttribute("id", id)
    button.setAttribute("style", "display: none;")
    selection.insertNode(button);
    selection.insertNode(span);

    enableTooltip()

    let ids = {
        "spanId": spanId,
        "buttonId": id
    }
    addMouseOverListenerToAnnotation(ids)
    addMouseOutListenerToAnnotation(ids)
}

function createSpanId(id) {
    return id + "-span"
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

    let inputMessage = document.getElementById("annotation-form-input-message");
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

function loadAndDisplayAnnotations(page) {

    let xhr = fetchAnnotations(page)

    xhr.onreadystatechange = () => {
        if (xhr.readyState === 4) {
            log('fetchAnnotations response:' + xhr.responseText);
            let responseJson = JSON.parse(xhr.responseText)

            responseJson["items"].forEach((item) => {
                displayAnnotation(item)
            })

            let annotatedTexts = document.getElementsByClassName("annotated-text")
            for (let i = 0; i < annotatedTexts.length; i++) {
                let element = annotatedTexts[i];
                element.addEventListener("mouseover", () => onMouseOverAnnotation(element))
                element.addEventListener("mouseout", () => onMouseOutAnnotation(element))
            }

            enableTooltip()

            if (responseJson["next"]) {
                log("fetching " + (page + 1))
                loadAndDisplayAnnotations(page + 1)
            } else {
                allAnnotations.forEach((ids) => {
                    addMouseOverListenerToAnnotation(ids)
                    addMouseOutListenerToAnnotation(ids)
                })
                allAnnotations = []
            }
        }
    }
}

function addMouseOverListenerToAnnotation(ids) {
    let span = document.getElementById(ids["spanId"])
    span.addEventListener("mouseover", () => {
        log("over")
        let button = document.getElementById(ids["buttonId"])
        button.setAttribute("style", "display: auto")
        button.addEventListener("click", () => {
            onAnnotationDeleteButtonPressed(ids)
        })
    })
}

function addMouseOutListenerToAnnotation(ids) {
    let span = document.getElementById(ids["spanId"])
    span.addEventListener("mouseout", () => {
        log("out")
        setTimeout(() => {
            hideButton(ids["buttonId"])
        }, 5000)
    })
}

function hideButton(buttonId) {
    let button = document.getElementById(buttonId)
    button.setAttribute("style", "display: none")
}

function onAnnotationDeleteButtonPressed(ids) {
    let xhr = deleteAnnotation(ids["buttonId"])

    xhr.onload = () => {
        log('deleteAnnotation status:' + xhr.status)
        if (xhr.status === 204) {
            let span = document.getElementById(ids["spanId"])
            span.classList.remove("annotated-text")
            span.removeAttribute("id")
            span.removeAttribute("data-bs-toggle")
            span.removeAttribute("data-bs-placement")
            span.removeAttribute("title")
            span.removeAttribute("aria-label")
            span.removeAttribute("data-bs-original-title")
            recreateNode(span)
            hideButton(ids["buttonId"])
        }
    }

    xhr.onerror = () => {
        console.error('deleteAnnotation request failed')
    }
}

function onMouseOverAnnotation(element) {
    element.classList.add("mouse-over-annotated-text")
}

function onMouseOutAnnotation(element) {
    element.classList.remove("mouse-over-annotated-text")
}

function displayAnnotation(annotation) {
    let prefix = annotation["target"]["selector"]["prefix"]
    let suffix = annotation["target"]["selector"]["suffix"]
    let exact = annotation["target"]["selector"]["exact"]
    let message = annotation["body"]["value"]
    let id = annotation["id"]
    highlight(exact, message, id, prefix, suffix)
}

function highlight(target, message, id, prefix, suffix) {
    let article = document.getElementById("colearn-article");
    let innerHTML = article.innerHTML;

    let index = innerHTML.indexOf(target);
    if (index >= 0) {
        let spanId = createSpanId(id)
        innerHTML = innerHTML.substring(0, index) +
            "<span " +
            " id='" + spanId + "'" +
            " class='annotated-text' " +
            "      data-bs-toggle='tooltip' " +
            "      data-bs-placement='top' " +
            "      aria-label='" + message + "' " +
            "      title='" + message + "'>" +
            innerHTML.substring(index, index + target.length) +
            "</span>" +
            "<button " +
            " id='" + id + "'" +
            " style='display: none;'" +
            " class='btn btn-danger bi bi-trash annotation-delete'></button> " +
            innerHTML.substring(index + target.length);
        article.innerHTML = innerHTML;
        allAnnotations.push({
            "spanId": spanId,
            "buttonId": id
        })
    } else {
        if (prefix === null || suffix === null) {
            return
        }
        highlight(prefix + target + suffix, message, id, null, null)
    }
}

function recreateNode(el, withChildren) {
    if (withChildren) {
        el.parentNode.replaceChild(el.cloneNode(true), el);
    } else {
        let newEl = el.cloneNode(false);
        while (el.hasChildNodes()) newEl.appendChild(el.firstChild);
        el.parentNode.replaceChild(newEl, el);
    }
}

document.addEventListener("mouseup", checkSelection);
document.addEventListener("keyup", checkSelection);

loadAndDisplayAnnotations(0)

// enable tooltip
function enableTooltip() {
    let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        if (bootstrap) {
            return new bootstrap.Tooltip(tooltipTriggerEl)
        }
    });
}

enableTooltip()


