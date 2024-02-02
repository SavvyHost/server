from src.core.api.main import *
from src.core.api.mails import recovery_mail

@csrf_exempt
def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if user.objects.filter(email=email).exists():
            return JsonResponse({"status": "exists"})
        user(
            name=name, email=email, password=password, ip=client(request, 'ip'), role=2,
            host=client(request, 'host'), city=client(request, 'location'), date=get_date(),
            contacts=True, chat=True,
        ).save()
        user_data = user_list(user.objects.latest("id").id)
        return JsonResponse({"user": user_data, **default()})
    return JsonResponse({"status": False})

@csrf_exempt
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        config = user.objects.filter(email=email, password=password, active=True, role=2).first()
        if not config: return JsonResponse({"status": False})
        return JsonResponse({"user": user_list(config.id), **default()})
    return JsonResponse({"status": False})

@csrf_exempt
def recovery(request):
    if request.method == "POST":
        email = request.POST.get('email')
        config = user.objects.filter(email=email, active=True, role=2).first()
        if not config: return JsonResponse({"status": False})
        token = f"{token_hex()}-{abs(hash(get_date()))}"
        reset_token = reset.objects.filter(user_id=config.id).first()
        if reset_token:
            reset_token.token = token
            reset_token.date = get_date()
            reset_token.save()
        else: reset(user_id=config.id, token=token, date=get_date()).save()
        threading.Thread(target=recovery_mail, kwargs={"email":config.email, "token":token}).start()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})

@csrf_exempt
def check_token(request):
    if request.method == "POST":
        token = request.POST.get('token')
        status = False
        if reset.objects.filter(token=token).exists(): status = True
        return JsonResponse({"status": status, "settings": settings()})
    return JsonResponse({"status": False})

@csrf_exempt
def change_password(request):
    if request.method == "POST":
        password = request.POST.get('password')
        token = request.POST.get('token')
        token = reset.objects.filter(token=token).first()
        if not token: return JsonResponse({"status": False})
        config = user.objects.filter(id=token.user_id, active=True, role=2).first()
        if not config: return JsonResponse({"status": False})
        config.password = password
        config.save()
        token.delete()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})
