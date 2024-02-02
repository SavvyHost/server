from src.core.api.main import *

def recovery_mail(**keywargs):
    try:
        config_user = user.objects.filter(email=keywargs.get('email')).first()
        config_settings = settings()
        subject= f'{config_settings["name"]} - Reset Password'
        data = {
            'reset_link': f"change/{keywargs.get('token')}",
            'username': config_user.name if config_user else 'Dear',
            'year': get_date('year'),
            'host': 'http://127.0.0.1:3000',
            'img_url': 'http://127.0.0.1:8000',
            'settings': config_settings,
        }
        html_content = render_to_string('mail/recovery.html', data)
        msg = EmailMultiAlternatives(
            subject, strip_tags(html_content), config_settings['name'],
            [keywargs.get('email')]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except: ...

def thanks_mail(**keywargs):
    try:
        config_user = user.objects.filter(email=keywargs.get('email')).first()
        config_settings = settings()
        subject= f'{config_settings["name"]} - Successful Booking'
        data = {
            'username': config_user.name if config_user else 'Dear',
            'year': get_date('year'),
            'host': 'http://127.0.0.1:3000',
            'img_url': 'http://127.0.0.1:8000',
            'settings': config_settings,
            'id': keywargs.get('id'),
            'price': keywargs.get('price'),
            'paid': "Paid" if keywargs.get('paid') else "Pay Later",
            'date': keywargs.get('date'),
            'pick_up': keywargs.get('pick_up'),
        }
        html_content = render_to_string('mail/thanks.html', data)
        msg = EmailMultiAlternatives(
            subject, strip_tags(html_content), config_settings['name'],
            [keywargs.get('email')]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except: ...
