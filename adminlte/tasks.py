import time

from django.core.mail import send_mail
from celery import shared_task
from celery import group

from adminlte.models import TemplatesMailing
from user.models import User


@shared_task
def send_single_email(subject, from_email, html_content, user_email):
    send_mail(
        subject,
        '',
        from_email,
        [user_email],
        html_message=html_content
    )

@shared_task(bind=True)
def bulk_send_email_task(self, template_id, users_ids):
    template = TemplatesMailing.objects.get(id=template_id)
    with open(template.template.path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    subject = "CINEMAX ВІТАЄ!!"
    from_email = "cinemax@ukr.net"
    total = len(users_ids)

    for i, user_id in enumerate(users_ids):
        try:
            user = User.objects.get(id=user_id)
            send_mail(
                subject,
                '',
                from_email,
                [user.email],
                html_message=html_content
            )
        except Exception as e:
            pass

        self.update_state(state='PROGRESS', meta={
            'current': i + 1,
            'total': total,
            'status': f"Відправлено {i + 1} з {total}"
        })

        time.sleep(.5)

    return {'current': total, 'total': total, 'status': 'Готово'}