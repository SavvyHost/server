from src.core.config.main import *

def set_file(request, id):
    dir = "product"
    file_num = request.POST.get("file_num") or 0
    deleted_files = request.POST.get("deleted_files") or "[]"
    for ch in range(int(file_num)):
        type = request.POST.get(f"file_{ch}_type")
        if type == "iframe":
            file_ = request.POST.get(f"file_{ch}")
            file(product_id=id, type="iframe", link=file_, date=get_date()).save()
            continue
        file_ = request.FILES.get(f"file_{ch}")
        ext = request.POST.get(f"file_{ch}_ext")
        name = request.POST.get(f"file_{ch}_name")
        size = request.POST.get(f"file_{ch}_size")
        link = upload_file(dir=dir, file=file_, ext=ext)
        file(product_id=id, name=name, type=type, size=size, link=link, date=get_date()).save()
    for ch in json.loads(deleted_files):
        if file.objects.filter(id=ch).exists():
            config = file.objects.get(id=ch)
            remove_file(f"{dir}/{config.link}")
            config.delete()

@authentication
def index(request):
    data = start_data(request)
    if not data['user'].products: return redirect('/')
    data['products'] = list(reversed(product.objects.all()))
    if request.method == "POST":
        ids = json.loads(request.POST.get("ids"))
        for id in ids:
            product.objects.filter(id=int(id)).delete()
            order.objects.filter(product_id=int(id)).delete()
            files = file.objects.filter(product_id=int(id))
            for f in files:
                remove_file(f"product/{f.link}")
                f.delete()
        return JsonResponse({"status": True})
    return render(request, 'product/list.html', data)

@authentication
def add(request):
    data = start_data(request)
    if not data['user'].products: return redirect('/')
    data['categories'] = category.objects.filter(active=True, products=True)
    if request.method == "POST":
        category_id = request.POST.get("category")
        name = request.POST.get("name")
        keys = request.POST.get("keys")
        attraction = request.POST.get("attraction")
        time = request.POST.get("time")
        phone = request.POST.get("phone")
        old_price = float(request.POST.get("old_price"))
        new_price = float(request.POST.get("new_price"))
        rate = float(request.POST.get("rate"))
        reviews = int(request.POST.get("reviews"))
        adults = int(request.POST.get("adults"))
        times = request.POST.get("times")
        included = request.POST.get("included")
        overview = request.POST.get("overview")
        description = request.POST.get("description")
        expect = request.POST.get("expect")
        policy = request.POST.get("policy")
        meeting = request.POST.get("meeting")
        info = request.POST.get("info")
        notes = request.POST.get("notes")
        active = bool(request.POST.get("active"))
        cancellation = bool(request.POST.get("cancellation"))
        public = bool(request.POST.get("public"))
        allow_bookings = bool(request.POST.get("allow_bookings"))
        product(
            name=name, notes=notes, old_price=old_price, new_price=new_price, keys=keys,
            category_id=category_id, active=active, date=get_date(), time=time,
            phone=phone, attraction=attraction, overview=overview, included=included,
            times=times, policy=policy, meeting=meeting, info=info, expect=expect,
            description=description, adults=adults, allow_bookings=allow_bookings,
            cancellation=cancellation, public=public, rate=rate, reviews=reviews
        ).save()
        id = product.objects.latest("id").id
        set_file(request, id)
        return JsonResponse({"status": True})
    return render(request, 'product/add.html', data)

@authentication
def edit(request, id):
    data = start_data(request)
    if not data['user'].products: return redirect('/')
    if not product.objects.filter(id=id).exists(): return redirect("/products")
    data['product'] = product.objects.get(id=id)
    data['categories'] = category.objects.filter(active=True, products=True)
    files = file.objects.filter(product_id=id)
    data['files'] = [[ch.id, ch.type, f"product/{ch.link}"] for ch in files]
    if request.method == "POST":
        config = product.objects.get(id=id)
        config.category_id = request.POST.get("category")
        config.name = request.POST.get("name")
        config.keys = request.POST.get("keys")
        config.attraction = request.POST.get("attraction")
        config.time = request.POST.get("time")
        config.phone = request.POST.get("phone")
        config.old_price = float(request.POST.get("old_price"))
        config.new_price = float(request.POST.get("new_price"))
        config.rate = float(request.POST.get("rate"))
        config.reviews = int(request.POST.get("reviews"))
        config.adults = int(request.POST.get("adults"))
        config.times = request.POST.get("times")
        config.included = request.POST.get("included")
        config.overview = request.POST.get("overview")
        config.description = request.POST.get("description")
        config.expect = request.POST.get("expect")
        config.policy = request.POST.get("policy")
        config.meeting = request.POST.get("meeting")
        config.info = request.POST.get("info")
        config.notes = request.POST.get("notes")
        config.allow_bookings = bool(request.POST.get("allow_bookings"))
        config.cancellation = bool(request.POST.get("cancellation"))
        config.public = bool(request.POST.get("public"))
        config.active = bool(request.POST.get("active"))
        config.save()
        set_file(request, id)
        return JsonResponse({"status": True})
    return render(request, 'product/edit.html', data)
