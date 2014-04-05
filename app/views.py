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
    
    if logout:
        logger.debug("Logging out!")
        auth.logout(request)
    else:
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)

    template = loader.get_template('app/index.html')
    context = RequestContext(request, {'current_user': str(request.user)})
    logger.debug("User: " + str(request.user))
    return HttpResponse(template.render(context))

def registration(request):
    logger.debug("REGISTRATION")
    if request.user.is_active:
        return HttpResponse("Already registered")
    else:
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        message = request.POST.get('message', '')

        if email:
            u = User.objects.create_user(username=email, email=email, password=password)
            u.save()
            user = auth.authenticate(username=email, password=password)
            ui = UserInfo(message=message)
            ui.save()
            auth.login(request, user)
            return redirect("/")

        template = loader.get_template('app/registration.html')
        context = RequestContext(request, {'current_user': str(request.user)})
        logger.debug("Data: " + str(email) + " " + str(password) + " " + str(message))

        return HttpResponse(template.render(context))
