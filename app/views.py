import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, loader
from django.contrib import auth

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
        template = loader.get_template('app/registration.html')
        context = RequestContext(request, {'current_user': str(request.user)})
        logger.debug("User: " + str(request.user))
        return HttpResponse(template.render(context))
