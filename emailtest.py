from django.core.mail import EmailMessage

email = EmailMessage(
    'Hello',
    'Body goes here',
    'registration@arhamcollections.com',
    ['findsarfaraz@gmail.com', 'to2@arhamcollections.com'],
    
    reply_to=['newtest@arhamcollections.com'],
    headers={'Message-ID': 'foo'},
)