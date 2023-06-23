from django.contrib.auth.models import User, Group


users = [
    ('admin', 'secret', True),
]

for login, pw, su in users:
    user = User.objects.create_user(login, password=pw)
    user.is_superuser=su
    user.is_staff=True
    user.save()


