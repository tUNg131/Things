from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

html_content = get_template('collect/email_html.html').render()
text_content = 'Hello, world!'
subject = 'test1'
to = [
    'halethuy.hlt@gmail.com',
]

msg = EmailMultiAlternatives(subject=subject, body=text_content, to=to)
msg.attach_alternative(html_content, "text/html")

msg.send()
