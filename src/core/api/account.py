from src.core.api.main import *

@csrf_exempt
def info(request):
    if request.method == "POST":
        id = integer(request.POST.get("id"))
        return JsonResponse({"user": user_list(id), **default()})
    return JsonResponse({"status": False})

@csrf_exempt
def edit(request):
    if request.method == "POST":
        id = integer(request.POST.get('id'))
        config = user.objects.filter(id=id, active=True, role=2).first()
        if not config: return JsonResponse({"status": 'none'})
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        if user.objects.filter(email=email).exists() and config.email != email:
            return JsonResponse({"status": 'email'})
        config.name = name
        config.email = email
        config.phone = phone
        config.city = city
        config.save()
        return JsonResponse({"status": True, "user": user_list(config.id)})
    return JsonResponse({"status": False})

@csrf_exempt
def reset_password(request):
    if request.method == "POST":
        id = integer(request.POST.get('id'))
        config = user.objects.filter(id=id, active=True, role=2).first()
        if not config: return JsonResponse({"status": 'none'})
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        if config.password != old_password: return JsonResponse({"status": 'password'})
        if new_password == old_password: return JsonResponse({"status": 'same'})
        config.password = new_password
        config.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})
