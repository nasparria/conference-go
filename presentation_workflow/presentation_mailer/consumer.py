import json
import pika
import django
import os
import sys
from django.core.mail import send_mail

sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presentation_mailer.settings")
django.setup()


def process_approval(ch, method, properties, body):
    info = json.loads(body)
    to_email = info["presenter_email"]
    from_email = "admin@conference.go"
    subject = "Your presentation has been accepted"
    title = info["title"]
    name = info["presenter_name"]
    body = f"{name}, we're happy to tell you that your presentation {title} has been accepted"
    send_mail(
        subject=subject,
        message=body,
        from_email=from_email,
        recipient_list=[to_email],
        fail_silently=False,
    )


def process_rejection(ch, method, properties, body):
    info = json.loads(body)
    to_email = info["presenter_email"]
    from_email = "admin@conference.go"
    subject = "Your presentation has been rejected"
    title = info["title"]
    name = info["presenter_name"]
    body = f"{name}, we're sorry to tell you that your presentation {title} has been rejected"
    send_mail(
        subject=subject,
        message=body,
        from_email=from_email,
        recipient_list=[to_email],
        fail_silently=False,
    )


parameters = pika.ConnectionParameters(host="rabbitmq")
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue="presentation_approvals")
channel.basic_consume(
    queue="presentation_approvals",
    on_message_callback=process_approval,
    auto_ack=True,
)
channel.queue_declare(queue="presentation_rejections")
channel.basic_consume(
    queue="presentation_rejections",
    on_message_callback=process_rejection,
    auto_ack=True,
)
channel.start_consuming()
