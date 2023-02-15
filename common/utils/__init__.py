# Standard Library
from urllib.parse import quote, unquote
from datetime import datetime, timedelta
import base64
import re


# App Constants
HEX_PATTERN_HASH = re.compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
HEX_PATTERN_NO_HASH = re.compile("^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
DOT_CODE = "%2E"
EXPIRE_MINS = 30


def getClientIp(metadata):
    """
        Get Client Ip from MetaData

        Parameters:
            metadata (dict): which holds the metadata sent through client request

        Return:
            str: client ip address
    """
    x_forwarded_for = metadata.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = metadata.get("REMOTE_ADDR")
    return ip


def isHexColor(color: str, noHash: bool):
    """
        Check the color value is a valid HEX color code with pattern (RRGGBB or RGB)

        Parameters:
            color (str): value to be verified as a HEX color
            noHash (bool): decides whether to include or exclude leading "#" in HEX color

        Return:
            a bool value represents the color value is HEX color code
    """
    if color is None or color == "":
        return False
    elif noHash:
        return re.match(HEX_PATTERN_NO_HASH, color) is not None
    return re.match(HEX_PATTERN_HASH, color) is not None


def hexToDec(color: str):
    """
        Hex color to decimal

        Parameters:
            color (str): hex color code (RRGGBB or RGB) without leading "#"

        Return:
            int: decimal value of hex code for RRGGBB
    """
    if len(color) == 3:
        fullcode = ""
        for c in color:
            fullcode += c*2
        color = fullcode
    return int(color, 16)


def strToBase64(pid: str):
    """
        Convert a string of text to base64 string

        Parameters:
            pid (str): string to be converted

        Return:
            str: converted base64 string
    """
    pid = encodeURIComponent(decodeURIComponent(pid))
    return base64.b64encode(pid.encode()).decode()


def encodeURIComponent(uri: str):
    """ 
        Encodes a text string as a valid component of a Uniform Resource Identifier (URI).

        Parameters:
            uri (str): A value representing an unencoded URI component.

        Return:
            str: encoded URI component
    """
    return quote(uri, safe="").replace(".", DOT_CODE)


def decodeURIComponent(encodedUri: str):
    """
        Gets the unencoded version of an encoded component of a Uniform Resource Identifier (URI).

        Parameters:
            encodedUri (str): A value representing an encoded URI component.

        Return:
            str: unencoded URI component
    """
    return unquote(encodedUri).replace(DOT_CODE, ".")


def calcExpiryTime(mins=EXPIRE_MINS, tillMidnight=False):
    """ 
        Calculates the expiry time from the current time

        Parameters:
            [mins] (int): time duration in terms of minutes
            [tillMidnight] (bool): if True the expire time is calculated for today's midnight

        Returns:
            float: expiration time in decimals
    """
    now = datetime.now()
    if tillMidnight:
        return datetime(now.year, now.month, now.day, 23, 59, 59).timestamp()
    try:
        mins = int(mins)
        if mins < 1:
            mins = EXPIRE_MINS
    except:
        mins = EXPIRE_MINS
    return (now + timedelta(minutes=mins)).timestamp()


def isExpired(timestamp) -> bool:
    """ Check passed in timestamp expired by comparing with current timestamp

        Parameters:
            timestamp (float): timestamp to be compared with

        Return:
            bool: True represents the timestamp is expired 
    """
    return timestamp < datetime.now().timestamp()
