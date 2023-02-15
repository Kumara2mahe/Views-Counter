import { changeBadgeBGcolor, hexToDec } from "./utils.js"


// Classes
const COPY_C = "copied", LOAD_C = "loaded", ERR_C = "error", EMPTY_C = "empty"

// Choose Badge background colors
const form = document.querySelector("form#generate-badge")
const outputSection = document.querySelector("#output-section")
const colorpickers = form.querySelectorAll(".label-colors input[type=color]")
colorpickers.forEach((input) => {
    input.addEventListener("input", changeBadgeBGcolor)
    changeBadgeBGcolor(input)
})

// Generate Badge on Form Submission
form.addEventListener("submit", async (e) => {
    e.preventDefault()
    let sBtn = form.querySelector("input[type=submit]")
    sBtn.disabled = true
    let formData = new FormData(e.target)
    const response = await fetch("/generate-badge", {
        method: "POST",
        body: formData
    })
    try {
        const data = await response.json()
        if (data.info == "Success") {
            outputSection.classList.add("show")
            outputSection.querySelector("#markdown input").value = data.urls.markdown
            outputSection.querySelector("#html-img input").value = data.urls.html
            outputSection.querySelector("#img-url input").value = data.urls.url
            document.documentElement.scrollTop = outputSection.offsetTop

            // Rendering Badge Preview
            showBadgePreview(
                formData.get("leftColor"),
                formData.get("rightColor"),
                data.urls.url,
                data.urls.html
            )
        }
        else if (data.info == EMPTY_C) {
            let usernameInput = form.querySelector("#user-name")
            usernameInput.classList.add(EMPTY_C)
            usernameInput.focus()
            setTimeout(() => {
                usernameInput.classList.remove(EMPTY_C)
            }, 2000)
        }
        else {
            alert("Oops! Something went wrong, Try again!")
            window.location.reload()
        }
        form.reset()
        sBtn.disabled = false
    }
    catch (error) {
        console.log(error)
    }
})

// Show/Hide loading animation and badge preview
const DEFAULTCOLOR_HEX = "#BFBFBF", DEFAULTCOLOR_DEC = hexToDec(DEFAULTCOLOR_HEX)
const showBadgePreview = (lColor, rColor, url, html) => {
    let loader = outputSection.querySelector("#preview-loader") // Change loader colors
    loader.style.borderTopColor = hexToDec(lColor) > DEFAULTCOLOR_DEC ? DEFAULTCOLOR_DEC : lColor
    loader.style.borderBottomColor = hexToDec(rColor) > DEFAULTCOLOR_DEC ? DEFAULTCOLOR_DEC : rColor

    // Show Badge Preview
    let img = outputSection.querySelector("img#preview-badge")
    if (isCopyIconsActivated === false) {
        activeCopyIcons()
        img = document.createElement("img")
        loader.before(img)
    }
    img.classList.remove("loaded")
    img.id = "preview-badge"
    img.src = url
    img.alt = html.match('alt=".+"')[0].slice(5, -1) // alt text from img
    img.onload = () => img.classList.add("loaded")
}

// Copy url Icons Activator
var isCopyIconsActivated = false
const activeCopyIcons = () => {

    // Copy url on Click
    outputSection.querySelectorAll(".urls img").forEach((icon) => {
        icon.onload = () => {
            icon.classList.add(LOAD_C)
            icon.onload = null
        }
        icon.addEventListener("click", toggleCopyAnims)
    })

    // Copy url on ENTER
    outputSection.querySelectorAll(".box").forEach((box) => {
        box.addEventListener("keydown", (event) => {
            if (event.key == "Enter") {
                event.target.querySelector("img").click()
            }
        })
    })
    isCopyIconsActivated = true
}

// Toggling copying animations
const toggleCopyAnims = (event) => {
    const icon = event.target
    if (outputSection.querySelector("img." + COPY_C) == null) {
        const img = icon.src
        navigator.clipboard.writeText(icon.previousElementSibling.value) // copy url
            .then(() => {
                icon.classList.add(COPY_C)
                icon.src = "/Static/Icons/done.svg"
            })
            .catch(() => {
                icon.classList.add(ERR_C)
                icon.src = "/Static/Icons/error.svg"
            })
            .finally(() => {
                setTimeout(() => {
                    icon.src = img
                    icon.classList.remove(COPY_C)
                    icon.classList.remove(ERR_C)
                }, 1000)
            })
    }
}