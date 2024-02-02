from src.core.api.main import *
from src.core.api.mails import thanks_mail

@csrf_exempt
def paid_booking(request):
    if request.method == "POST":
        user_id = integer(request.POST.get('user'))
        tour_id = integer(request.POST.get('tour'))
        adults = integer(request.POST.get('adults'))
        coupon_code = request.POST.get('coupon')
        pick_up = request.POST.get('pick_up')
        notes = request.POST.get('notes')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        book_date = request.POST.get('book_date')
        book_time = request.POST.get('book_time')
        paid_secret = request.POST.get('paid_secret')
        paid_currency = request.POST.get('paid_currency')
        paid_price = float(request.POST.get('paid_price'))
        paid_date = request.POST.get('paid_date')
        paid_status = bool(request.POST.get('paid_status'))
        config = product.objects.filter(id=tour_id, active=True).first()
        cp = coupon.objects.filter(code=coupon_code).first()
        price = config.new_price * adults
        discount = 0
        if cp:
            coupon_code = cp.code
            discount = price * cp.discount / 100
            price -= discount
        complete = True
        if not config: complete = False
        if not paid_status: complete = False
        if paid_currency != 'usd': complete = False
        if paid_price < price: complete = False
        if diff_date(paid_date, str(datetime.utcnow()).split('.')[0]) > 60: complete = False
        if payment.objects.filter(paid_secret=paid_secret).exists(): complete = False
        if not complete: return JsonResponse({"status": False})

        order(
            user_id=user_id, product_id=tour_id, name=name,
            email=email, phone=phone, date=get_date(), pick_up=pick_up,
            book_date=book_date, book_time=book_time, notes=notes, adults=adults,
            discount=discount, coupon=coupon_code, price=price, paid=True
        ).save()
        id = order.objects.latest('id').id
        payment(
            user_id=user_id, tour_id=tour_id, order_id=id,
            paid_price=paid_price, real_price=price, adults=adults,
            paid_secret=paid_secret, paid_date=paid_date, date=get_date()
        ).save()
        kwargs = {
            "id": id, "price": price, "email": email,
            "date": f"{book_date} {book_time}",
            "paid": True, "pick_up": pick_up
        }
        threading.Thread(target=thanks_mail, kwargs=kwargs).start()
        data = {"status": True, "id": id, "price": price, "email": email, "paid": True}
        return JsonResponse(data)
    return JsonResponse({"status": False})

@csrf_exempt
def later_booking(request):
    if request.method == "POST":
        user_id = integer(request.POST.get('user'))
        tour_id = integer(request.POST.get('tour'))
        adults = integer(request.POST.get('adults'))
        coupon_code = request.POST.get('coupon')
        pick_up = request.POST.get('pick_up')
        notes = request.POST.get('notes')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        book_date = request.POST.get('book_date')
        book_time = request.POST.get('book_time')
        config = product.objects.filter(id=tour_id, active=True).first()
        cp = coupon.objects.filter(code=coupon_code).first()
        price = config.new_price * adults
        discount = 0
        if cp:
            coupon_code = cp.code
            discount = price * cp.discount / 100
            price -= discount
        if not config: return JsonResponse({"status": False})
        order(
            user_id=user_id, product_id=tour_id, name=name,
            email=email, phone=phone, date=get_date(), pick_up=pick_up,
            book_date=book_date, book_time=book_time, notes=notes, adults=adults,
            discount=discount, coupon=coupon_code, price=price, paid=False
        ).save()
        id = order.objects.latest('id').id
        kwargs = {
            "id": id, "price": price, "email": email,
            "date": f"{book_date} {book_time}",
            "paid": False, "pick_up": pick_up
        }
        threading.Thread(target=thanks_mail, kwargs=kwargs).start()
        data = {"status": True, "id": id, "price": price, "email": email, "paid": False}
        return JsonResponse(data)
    return JsonResponse({"status": False})

@csrf_exempt
def discount(request):
    if request.method == "POST":
        code = request.POST.get('coupon')
        tour_id = integer(request.POST.get('tour'))
        tour_config = product.objects.filter(id=tour_id, active=True).first()
        coupon_config = coupon.objects.filter(code=code, active=True).first()
        if not tour_config: return JsonResponse({"status": False})
        if not coupon_config: return JsonResponse({"status": False})
        discount = tour_config.new_price * coupon_config.discount / 100
        price = round(tour_config.new_price - discount, 2)
        return JsonResponse({"status": True, 'price': price, 'coupon': code})
    return JsonResponse({"status": False})

@csrf_exempt
def bookings_data(request):
    if request.method == "POST":
        user_id = integer(request.POST.get('user'))
        data = {"bookings": bookings(user_id), **default()}
        return JsonResponse(data)
    return JsonResponse({"status": False})

@csrf_exempt
def change_status(request):
    if request.method == "POST":
        ids = parse(request.POST.get('ids'))
        status = integer(request.POST.get('status'))
        for id in ids:
            config = order.objects.filter(id=id, active=True).first()
            if not config: continue
            tour = product.objects.filter(id=config.product_id, active=True).first()
            if not tour: continue
            date = f"{config.book_date} {config.book_time or '0:0:0'}"
            if diff_date(end=date) < 86400: return JsonResponse({"status": False})
            if config.status > 2: return JsonResponse({"status": False})
            if not tour.cancellation and status == 2: return JsonResponse({"status": False})
            config.status = status
            config.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})

@csrf_exempt
def remove_booking(request):
    if request.method == "POST":
        ids = parse(request.POST.get('ids'))
        for id in ids:
            config = order.objects.filter(id=id, active=True).first()
            if not config: continue
            if config.status < 3: return JsonResponse({"status": False})
            config.removed = True
            config.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})
