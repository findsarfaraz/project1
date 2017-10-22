from project1 import settings
from django.core.mail import EmailMessage
settings.configure()

email = EmailMessage(
    'Hello',
    'Body goes here',
    from_email='registration@arhamcollections.com',
    to=['findsarfaraz@gmail.com', 'finddjango@gmail.com'],
    
    reply_to=['newtest@arhamcollections.com'],
    headers={'Message-ID': 'foo'},
)
email.send()

