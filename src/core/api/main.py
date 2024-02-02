from app.models import *

def tour_image(id):
    files = file.objects.filter(product_id=id)
    dir = f"/static/media/product"
    images_ = [[f"{dir}/{ch.link}", ch.type] for ch in files if ch.type == "image"]
    frames_ = [[f"{dir}/{ch.link}", ch.type] for ch in files if ch.type == "iframe"]
    videos_ = [[f"{dir}/{ch.link}", ch.type] for ch in files if ch.type == "video"]
    images = frames_ + videos_ + images_
    if not images: images = [[f"{dir}/default.png", "image"]]
    if images_: image = images_[0][0]
    else: image = images[0][0]
    return images, image

def tour_list(id):
    data = product.objects.filter(id=id, active=True).first()
    if not data: return {}
    location = "Egypt"
    dest = category.objects.filter(id=data.category_id, active=True).first()
    if dest: location = dest.name
    images, image = tour_image(id)
    list_data = {
        'id': data.id, 'name': data.name, 'keys': data.keys, 'location': location,
        'new_price': data.new_price, 'old_price': data.old_price, 'images': images,
        'reviews': data.reviews, 'rate': data.rate, 'booking': data.allow_bookings, 'adults': data.adults,
        'company': data.company, 'phone': data.phone, 'times': data.times, 'overview': data.overview,
        'included': data.included, 'expect': data.expect, 'policy': data.policy, 'meeting': data.meeting,
        'additional_info': data.info, 'notes': data.notes, 'date': data.date, "image": image,
        "time": data.time, "cancellation": data.cancellation, "public": data.public,
        "pay_later": data.pay_later, "attraction": data.attraction, "description": data.description
    }
    return list_data

def user_list(id):
    data = user.objects.filter(id=id, active=True, role=2).first()
    if not data: return {}
    data = {
        'id': data.id, 'name': data.name, 'email': data.email,
        'image': f'/static/media/user/{data.image}', 'phone': data.phone,
        "city": data.city, "ip": data.ip, "host": data.host,
        "date": data.date,
    }
    return data

def recent_tours():
    data = product.objects.filter(active=True).order_by('-id')[:10]
    return [tour_list(ch.id) for ch in data]

def recommend_tours(id=0):
    data = product.objects.filter(id=id, active=True).first()
    if not data: return recent_tours()
    tours = product.objects.filter(category_id=data.category_id)
    if tours: tours = tours.exclude(id=id).order_by('-id')[:10]
    tours = [tour_list(ch.id) for ch in tours]
    if len(tours) < 10: tours += recent_tours()[:10-len(tours)]
    return tours

def tour_details(id):
    data = product.objects.filter(id=id, active=True).first()
    if not data: return {}
    data.views += 1
    data.save()
    return tour_list(id)

def destinations():
    destinations = []
    data = category.objects.filter(active=True).order_by('-id')[:9]
    for ch in data:
        tours_count = product.objects.filter(category_id=ch.id).count()
        destinations.append({
            'id': ch.id, 'name': ch.name, 'tours': tours_count,
            'description': ch.description,
            'image': f"/static/media/category/{ch.image}"
        })
    return destinations

def destination(id):
    data = category.objects.filter(id=id, active=True).first()
    if not data: return {}
    data = {
        'name': data.name, 'description': data.description,
        'image': f'/static/media/category/{data.image}',
        'tours': [tour_list(ch.id) for ch in product.objects.filter(category_id=id)]
    }
    return data

def bookings(user_id):
    if not user_id: return []
    orders = order.objects.filter(user_id=user_id, active=True, removed=False).order_by('status')
    all_orders = []
    for ch in orders:
        tour_info = tour_list(ch.product_id)
        all_orders.append({
            'id': ch.id, 'date': ch.date,
            'paid': ch.paid, 'adults': ch.adults, 'price': ch.price,
            'book_date': ch.book_date, 'book_time': ch.book_time,
            'pick_up': ch.pick_up, 'status': ch.status, 'tour': tour_info,
        })
    return all_orders

def search(query, date, filters):
    all_data = product.objects.filter(active=True)
    if query and date: data = all_data.filter(Q(name__icontains=f'{query}')|Q(date__icontains=f'{date}'))
    elif query: data = all_data.filter(Q(name__icontains=f'{query}'))
    elif date: data = all_data.filter(Q(date__icontains=f'{date}'))
    return [tour_list(ch.id) for ch in data]

def settings():
    config = setting.objects.filter(id=1).first()
    if not config: return {}
    data = {
        "name": config.name, "email": config.email, "phone": config.phone, "city": config.city,
        "facebook": config.facebook, "whatsapp": config.whatsapp, "youtube": config.youtube,
        "twetter": config.twetter, "telegram": config.telegram, "instagram": config.instagram,
        "linkedin": config.linkedin, "theme": config.theme, "contact": config.enable_contacts,
        "chat": config.enable_chat, "chat_files": config.enable_chat_files, "bookings": config.enable_orders,
        "deactive": config.deactive, "login": config.enable_login, "register": config.enable_register,
        "language": config.language, "description": config.description,
        'tours_count': product.objects.all().count(),
    }
    return data

def default(tour_id=0):
    return {
        'status': True,
        'recent_tours': recent_tours(),
        'recommend_tours': recommend_tours(tour_id),
        'destinations': destinations(),
        'settings': settings(),
    }
