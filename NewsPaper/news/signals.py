import os
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import PostCategory


from dotenv import load_dotenv

load_dotenv()


@receiver(m2m_changed, sender=PostCategory)
def mail_new_post_to_subs(sender, instance, **kwargs):
    categories = instance.categories.all()
    html_content = render_to_string('mail_news_single.html', {'header': instance.header,
                                                              'text': instance.text,
                                                              'id': instance.id})
    to = []
    for category in categories:
        subscribers = category.subscribers.all()
        for subscriber in subscribers:
            to.append(subscriber.email)
    msg = EmailMultiAlternatives(
        subject=instance.header,
        body=instance.text[0:50],
        from_email=os.getenv("YANDEX_ADDRESS"),
        to=to,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
