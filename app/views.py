import logging

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, loader
from django.contrib import auth
from app.models import UserInfo
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)
fh = logging.FileHandler('debug.log')
msg = "%(asctime)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(msg)
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)

def index(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    logout = request.POST.get('action', '')
    current_user = request.user

    if logout:
        logger.debug("Logging out!")
        auth.logout(request)
        return redirect("/")
    else:
        user = auth.authenticate(username=str(username), password=str(password))
        logger.debug("authed user:" + str(user))
        logger.debug("Username: " + username + ", Password: " + password)
        if user is not None and user.is_active:
            auth.login(request, user)
            current_user = user

    template = loader.get_template('app/index.html')
    context = RequestContext(request, {
        'current_user': str(current_user),
        "page": "home",
    })
    logger.debug("User: " + str(current_user))
    return HttpResponse(template.render(context))


def profile(request):
    logout = request.POST.get('action', '')
    current_user = request.user

    if logout:
        logger.debug("Logging out!")
        auth.logout(request)
        return redirect("/")

    template = loader.get_template('app/profile.html')
    context = RequestContext(request, {
        'current_user': str(current_user),
        "page": "profile",
    })
    logger.debug("User: " + str(current_user))
    return HttpResponse(template.render(context))


def registration(request):
    logger.debug("REGISTRATION")
    if request.user.is_active:
        return HttpResponse("Already registered")
    else:
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        message = request.POST.get('message', '')
        logger.debug("reg user:" + email)
        logger.debug("reg pw:" + password)
        if email:
            u = User.objects.create_user(username=str(email), password=str(password))
            u.set_password(password)
            u.save()
            user = auth.authenticate(username=str(email), password=str(password))
            ui = UserInfo(message=message, authuser_id_id=user.id)
            ui.save()
            auth.login(request, user)
            return redirect("/")

        template = loader.get_template('app/registration.html')
        context = RequestContext(request, {'current_user': str(request.user)})
        logger.debug("Data: " + str(email) + " " + str(password) + " " + str(message))

        return HttpResponse(template.render(context))
