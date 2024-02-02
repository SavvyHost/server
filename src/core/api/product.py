from src.core.api.main import *

@csrf_exempt
def all_data(request):
    if request.method == "POST": return JsonResponse(default())
    return JsonResponse({"status": False})

@csrf_exempt
def destination_data(request):
    if request.method == "POST":
        id = integer(request.POST.get("id"))
        return JsonResponse({'destination': destination(id), **default()})
    return JsonResponse({"status": False})

@csrf_exempt
def tour_data(request):
    if request.method == "POST":
        id = integer(request.POST.get("id"))
        return JsonResponse({'tour': tour_details(id), **default(id)})
    return JsonResponse({"status": False})

@csrf_exempt
def wishlist_data(request):
    if request.method == "POST":
        ids = parse(request.POST.get("ids"))
        tours = [tour_list(id) for id in ids]
        return JsonResponse({ 'tours': tours, **default()})
    return JsonResponse({"status": False})

@csrf_exempt
def search_tours(request):
    if request.method == "POST":
        query = request.POST.get("query")
        date = request.POST.get("date")
        filters = parse(request.POST.get("filters"))
        result = search(query, date, filters)
        return JsonResponse({"tours": result, **default()})
    return JsonResponse({"status": False})
