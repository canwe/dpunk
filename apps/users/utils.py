from django.contrib.auth import login, authenticate

def auth(request, email, password):
    user = authenticate(email=email, password=password)
    login(request, user)
    return user