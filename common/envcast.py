# Standard library
import os


def toBool(key: str) -> bool:
    """
        Get and Convert the value of environment variable to a (bool)

        Parameters:
            key (str): name of the environment variable

        Return:
            bool
    """
    BOOLS = ["True", "False"]

    value = os.getenv(key)
    if (value is not None) and (value := value.capitalize()) in BOOLS:
        return eval(value)
    return False


def toInt(key: str) -> int:
    """
        Get and Convert the value of environment variable to a (int)

        Parameters:
            key (str): name of the environment variable

        Return:
            int
    """

    value = os.getenv(key)
    if (value is not None and value.isdigit()):
        return int(value)
    return 0


def toStr(key: str) -> str:
    """
        Get and Convert the value of environment variable to a (str)

        Parameters:
            key (str): name of the environment variable

        Return:
            str
    """

    value = os.getenv(key)
    return str(value)


def toTuple(key: str):
    """
        Get and Convert the value of environment variable to a (tuple)
    """
    BRACS = ["(", ")"]
    QUOTES = ["\"", "'"]

    value = os.getenv(key)
    if (value is not None and value.capitalize() != "None"):

        if value[0] != BRACS[0]:
            print(
                f"May be you forgot the '{BRACS[0]}' while setting your value for : {key}")
        elif value[-1] != BRACS[1]:
            print(
                f"May be you forgot the '{BRACS[1]}' while setting your value for : {key}")
        else:

            # Splitting the str to list
            value = value[1:-1].split(",")
            if len(value) == 2:
                for n, val in enumerate(value):

                    # Removing the whitespace
                    val = val.strip()

                    # Removing the quotes around the string
                    if (val[0] == QUOTES[0] and val[-1] == QUOTES[0]):
                        value[n] = val.removeprefix(QUOTES[0]).removesuffix(QUOTES[0])
                    elif (val[0] == QUOTES[1] and val[-1] == QUOTES[1]):
                        value[n] = val.removeprefix(QUOTES[1]).removesuffix(QUOTES[1])
                    else:
                        value[n] = val

                return tuple(value)
