
// Hex to decimal
export const hexToDec = (color) => {
    return window.parseInt(color.replace("#", ""), 16)
}

// Color picker's background & foreground color changer
const MIDHEXCOLOR = Math.floor(hexToDec("FFFFFF") / 2)
export const changeBadgeBGcolor = (e) => {
    let input = (e instanceof Element) ? e : e.target
    let bgcolor = input.value
    input.parentElement.style.backgroundColor = bgcolor
    input.parentElement.style.color = hexToDec(bgcolor) < MIDHEXCOLOR ? "#FFF" : "#000"
}