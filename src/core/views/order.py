from src.core.config.main import *

@authentication
def index(request):
    data = start_data(request)
    if not data['user'].orders: return redirect('/')
    data['orders'] = order.objects.all().order_by('status')
    if request.method == "POST":
        ids = json.loads(request.POST.get("ids"))
        for id in ids: order.objects.get(id=int(id)).delete()
        return JsonResponse({"status": True})
    return render(request, 'order/list.html', data)

@authentication
def add(request):
    data = start_data(request)
    if not data['user'].orders: return redirect('/')
    data['products'] = list(reversed(product.objects.all()))
    data['users'] = list(reversed(user.objects.filter(role=2)))
    data['coupons'] = list(reversed(coupon.objects.all()))
    if request.method == "POST":
        user_id = integer(request.POST.get("user"))
        product_id = integer(request.POST.get("product"))
        coupon_id = integer(request.POST.get("coupon"))
        config_tour = product.objects.filter(id=product_id, active=True).first()
        config_coupon = coupon.objects.filter(id=coupon_id, active=True).first()
        if not config_tour: return JsonResponse({"status": False})
        coupon_name = ''
        discount = 0
        price = config_tour.new_price
        if config_coupon:
            coupon_name = config_coupon.code
            discount = config_coupon.discount * price / 100
            price -= discount
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        pick_up = request.POST.get("address")
        notes = request.POST.get("notes")
        status = int(request.POST.get("status"))
        paid = bool(request.POST.get("paid"))
        active = bool(request.POST.get("active"))
        order(
            user_id=user_id, product_id=product_id, coupon=coupon_name, discount=discount,
            price=price, date=get_date(), paid=paid, status=status, name=name,
            email=email, phone=phone, pick_up=pick_up, notes=notes, active=active
        ).save()
        return JsonResponse({"status": True})
    return render(request, 'order/add.html', data)

@authentication
def edit(request, id):
    data = start_data(request)
    if not data['user'].orders: return redirect('/')
    if not order.objects.filter(id=id).exists(): return redirect("/orders")
    data['order'] = order.objects.get(id=id)
    data['products'] = list(reversed(product.objects.all()))
    data['users'] = list(reversed(user.objects.filter(role=2)))
    data['coupons'] = list(reversed(coupon.objects.all()))
    if request.method == "POST":
        config = order.objects.get(id=id)
        config.name = request.POST.get("name")
        config.email = request.POST.get("email")
        config.phone = request.POST.get("phone")
        config.pick_up = request.POST.get("pick_up")
        config.notes = request.POST.get("notes")
        config.status = int(request.POST.get("status"))
        config.paid = bool(request.POST.get("paid"))
        config.active = bool(request.POST.get("active"))
        config.save()
        return JsonResponse({"status": True})
    return render(request, 'order/edit.html', data)
