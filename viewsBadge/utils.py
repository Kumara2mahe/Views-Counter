# local
from common.utils import isHexColor, hexToDec


# App Constants
BADGE_TYPES = ["total", "daily", "unique"]
BADGE_STYLES = ["upper", "lower"]
TODAY_K = "today"
COUNT_K = "count"
BADGE_MINLEN = 8
HALF_LEN = BADGE_MINLEN // 2
THOUSAND = 10 ** 3
MILLION = THOUSAND ** 2
BILLION = THOUSAND ** 3
TRILLION = THOUSAND ** 4
HEX_CODES = ["000", "FFF", "00F"]
MIDHEXCOLOR = hexToDec(HEX_CODES[1]) // 2


def getCountbyType(obj: dict, key: str):
    """
        Get badge count by its type

        Parameters:
            obj (dict): views object with values of views count
            key (str): represents the keys in views object

        Return:
            int: view count relavent to the key
    """
    bType = getType(key)
    if bType in BADGE_TYPES:
        count = obj[bType]
    else:
        count = obj[bType][COUNT_K]
    return assignViewMetrics(count)


def getType(val: str, useDefault=None):
    if val in BADGE_TYPES:
        return val if useDefault or val != BADGE_TYPES[1] else TODAY_K
    return BADGE_TYPES[0]


def getLabel(text: str):
    return (text if text else "Viewers").strip()


def getStyle(val: str):
    return val if val in BADGE_STYLES else "none"


def assignViewMetrics(n):
    """ 
        Abbreviate numbers with some metric symbols like million(M), billion(B) & trillion(T)

        Parameters:
            n (int): number to abbreviated with metric

        Return:
            str: abbreviated number with its relavent metric symbols(K, M, B, T)
    """
    if THOUSAND <= n < MILLION:
        n = roundCount(n / THOUSAND) + "K"
    elif MILLION <= n < BILLION:
        n = roundCount(n / MILLION) + "M"
    elif BILLION <= n < TRILLION:
        n = roundCount(n / BILLION) + "B"
    elif TRILLION <= n:
        n = roundCount(n / TRILLION) + "T"
    return str(n)


def roundCount(n, decimaldigits=2):
    """
        Round(limit) numbers with specified decimal places

        Parameters:
            n (float): number to be round of
            decimaldigits (int): no of decimal places to take or include while rounding

        Return:
            str: round offed number as text
    """
    n = str(n).split(".")
    n[1] = n[1][0:decimaldigits]
    while n[1].endswith("0"):  # remove trailing zeros after "."
        n[1] = n[1][0:-1]
    return f"{n[0]}.{n[1]}" if n[1] != "" else f"{n[0]}"


def applyStyle(text: str, style: str):
    """
        Change case to the badge label text according to the style specified

        Parameters:
            text (str): text to be displayed on the badge label
            style (str): text represents either lower or upper case

        Return:
            str: text to be displayed on the badge label
    """
    text = getLabel(text)
    if style == BADGE_STYLES[0]:
        text = text.upper()
    elif style == BADGE_STYLES[1]:
        text = text.lower()
    return text


def calcBadgeWidth(label: str, count: str):
    """
        Calculate the badge with by character length of label & count

        Parameters:
            label (str): text to be displayed on the right side of badge
            count (str): a number representing the total views count

        Return:
            str: value represents the badge width with clearance of 2px
    """
    badge_width = len(label + count)  # total char length
    diff = BADGE_MINLEN - badge_width
    if badge_width > BADGE_MINLEN:
        diff = diff * -1
        if diff <= HALF_LEN:
            badge_width = 98 + \
                (diff * (HALF_LEN + diff / 1.75) if diff > 1 else diff)
        else:
            badge_width = (badge_width * 10) + badge_width - \
                (diff * BADGE_MINLEN / 2.5)
    else:
        diff = BADGE_MINLEN - badge_width
        badge_width = 92 - diff * (HALF_LEN + diff / 2)
    return str(badge_width * 1.08)


def getHexColor(val: str, noHash: bool, label: bool):
    """
        Validate and get hex color code

        Parameters:
            val (str): hex color code to validate
            noHash (bool): represents whether to include leading "#" in hex code validation
            label (bool): used when val is empty and defines a default color as either (black or blue)

        Return:
            str: hex color code (RRGGBB or RGB) without leading "#"
    """
    if isHexColor(val, noHash):
        hexcode = val
    else:
        hexcode = HEX_CODES[0] if label else HEX_CODES[2]
    return hexcode.replace("#", "")


# Pick Foreground color opposite to background color
def getFGColor(bgcolor: str):
    return HEX_CODES[1] if hexToDec(bgcolor) < MIDHEXCOLOR else HEX_CODES[0]
