# Standard Library
from io import BytesIO
from datetime import datetime

# Django
from django.shortcuts import render
from django.http.response import FileResponse, JsonResponse

# local Django
from common.utils.dBase import addorUpdateData
from common.utils import encodeURIComponent, decodeURIComponent
from .utils import (getCountbyType, applyStyle,
                    calcBadgeWidth, getHexColor, getFGColor,
                    getType, getLabel, getStyle)


def index(request):
    """ View for rendering Generate-Badge-Page """

    current_year = datetime.now().year
    return render(request, "index.html", {"current_year": current_year})


def badge(request):
    """ View for rendering views Badge, as per user request """

    if page_id := request.GET.get("pageId"):
        view_count = getCountbyType(
            addorUpdateData(page_id, request),  # Record Views/Visits
            request.GET.get("type")
        )  # View
        label = applyStyle(text=request.GET.get("label"),
                           style=request.GET.get("style"))  # label
        label = decodeURIComponent(label)
        badge_width = calcBadgeWidth(label, view_count)
        left_bg = getHexColor(request.GET.get("leftColor"), True, True)
        right_bg = getHexColor(request.GET.get("rightColor"), True, False)

        # Rendering Svg with user data
        response = render(request, "badge.svg", {
            "left_bg": left_bg,
            "right_bg": right_bg,
            "count": view_count,
            "label": label,
            "badge_width": badge_width,
            "left_fg": getFGColor(left_bg),
            "right_fg": getFGColor(right_bg),
        })
        file = BytesIO(response.content)
        filename = "badge.svg"
    else:
        with open("Static/Icons/error-badge.png", "rb") as f:
            file = BytesIO(f.read())
        filename = "error.png"

    # Image file as response
    return FileResponse(file, filename=filename, headers={
        "Cache-Control": "no-cache,max-age=0",
        "Expires": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    })


def generateBadgeUrl(request):
    """ View to generate Badge urls, as per user request """

    if page_id := request.POST.get("pageId"):
        page_id = encodeURIComponent(page_id)
        left_color = getHexColor(request.POST.get("leftColor"), False, True)
        right_color = getHexColor(request.POST.get("rightColor"), False, False)
        bType = getType(request.POST.get("type"), True)
        label = encodeURIComponent(getLabel(request.POST.get("label")))
        style = getStyle(request.POST.get("style"))

        # Root Url
        absolute_path = request.build_absolute_uri()
        rooturl = absolute_path.split(request.path)[0]

        # Generate url with validated values
        url = f"{rooturl}/badge?pageId={page_id}&leftColor={left_color}&rightColor={right_color}&type={bType}&label={label}&style={style}"
        return JsonResponse({
            "info": "Success",
            "urls": {
                "markdown": f"![Views Counter]({url})",
                "html": f'<img src="{url}" alt="Views Counter">',
                "url": f"{url}"
            }
        })
    else:
        return JsonResponse({"info": "empty"})
