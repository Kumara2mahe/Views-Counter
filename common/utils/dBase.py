# Standard Library
from datetime import datetime

# local django
from common.envcast import toStr
from common.utils import strToBase64, getClientIp, calcExpiryTime, isExpired
from viewsBadge.utils import BADGE_TYPES, TODAY_K, COUNT_K

# 3rd Party
from dotenv import load_dotenv
from firebase_admin import credentials, db
import firebase_admin

load_dotenv()
cred = credentials.Certificate(toStr("SERVICE_KEY_PATH"))

# Firebase Admin SDK
firebase_admin.initialize_app(cred, {
    "databaseURL": toStr("DATABASE_URL"),
    "databaseAuthVariableOverride": {
        "uid": toStr("ADMIN_SDK_ID")
    }
})

# References
USERS_REF = db.reference("users")
VIEWS_REF = db.reference("views")
VISITS_REF = db.reference("unique-visitors")

# Keys
MODIFY_K = "modifiedOn"
EXPIRE_K = "expiresOn"
VISITORS = "visitors"


def addorUpdateData(id: str, request):
    """
        Create or Update the specific user's view count

        Parameters:
            id (str): unique id of existing/for new user
            request (HttpRequest): which contains all data sent through client request as object

        Return:
            dict: new views object with values of views count
    """
    key = strToBase64(id)  # convert id to base64
    client_ip = strToBase64(getClientIp(request.META))  # ip to base64
    user_ref = USERS_REF.child(key)
    view_ref = VIEWS_REF.child(key)

    # Calculating unique ip expire mins
    sExpire = calcExpiryTime(request.GET.get("sessionExpire"))
    if user_ref.get() is None:
        new_data = addNewData(user_ref, view_ref, client_ip, sExpire)
    else:
        new_data = updateData(user_ref, view_ref, client_ip, sExpire)
    return new_data


def addNewData(u_ref, v_ref, ip: str, sExpire: float):
    """
        Add new user data

        Parameters:
            u_ref (Reference): new firebase reference to the user object
            v_ref (Reference): new firebase reference to the view object
            ip (str): client's public ip address as base64 encoded
            sExpire (float): unique visit count expire duration as timestamp

        Return:
            dict: value of new view object
    """
    now = datetime.now().isoformat()
    u_ref.set({
        "createdOn": now,
        MODIFY_K: now,
        VISITORS: {
            ip: sExpire
        }
    })
    newData = {BADGE_TYPES[0]: 1,
               TODAY_K: defaultTodayValue(), BADGE_TYPES[2]: 1}
    v_ref.set(newData)
    return newData


def defaultTodayValue():
    """ Default values for Today key in views object """
    return {
        COUNT_K: 1,
        EXPIRE_K: calcExpiryTime(tillMidnight=True)
    }


def updateData(u_ref, v_ref, ip: str, sExpire: float):
    """
        Update existing user data and dumping expired unique ips

        Parameters:
            u_ref (Reference): existing firebase reference to the user object
            v_ref (Reference): existing firebase reference to the view object
            ip (str): client's public ip address as base64 encoded
            sExpire (float): unique visit count expire duration as timestamp

        Return:
            dict: value of updated view object
    """
    u_ref.update({MODIFY_K: datetime.now().isoformat()})
    view_obj = v_ref.get()
    visitors_ref = u_ref.child(VISITORS)

    # Dumping all expired visits
    if visitors := visitors_ref.get():
        for k in visitors:
            if isExpired(visitors[k]):
                visitors_ref.child(k).delete()

    # Collect new data
    new_data = {
        BADGE_TYPES[0]: getTotalView(view_obj),
        TODAY_K: getTodayView(view_obj),
        BADGE_TYPES[2]: getUniqueVisit(
            obj=view_obj,
            visit_ref=visitors_ref.child(ip),
            sExpire=sExpire
        )
    }
    v_ref.update(new_data)
    return new_data


def getTotalView(obj: dict):
    """ Increment Total view count by 1 

        Parameters:
            obj (dict): value of view object

        Return:
            int: increased count for value of Total key in view object
    """
    return obj[BADGE_TYPES[0]] + 1


def getTodayView(obj: dict):
    """
        Increment Today view count by 1, resets the today views when it passed expires time

        Parameters:
            obj (dict): value of view object

        Return:
            dict: new value for Today key in view object
    """
    today = obj[TODAY_K]
    today[COUNT_K] += 1
    if isExpired(today[EXPIRE_K]):
        today = defaultTodayValue()
    return today


def getUniqueVisit(obj: dict, visit_ref, sExpire: float):
    """
        Update existing user data

        Parameters:
            obj (dict): value of view object
            visit_ref (Reference): existing firebase reference to the user/visitors/{user_ip}
            sExpire (float): unique visit count expire duration as timestamp
    """
    unique = obj[BADGE_TYPES[2]]
    v_obj = visit_ref.get()
    if v_obj is None or isExpired(v_obj):
        visit_ref.set(sExpire)
        unique += 1
    return unique
