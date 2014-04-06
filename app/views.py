import logging

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, loader
from django.contrib import auth
from app.models import UserInfo,SkillType,SkillInstance
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

    template = loader.get_template('app/profile.html')
    ui = UserInfo.objects.get(authuser_id=current_user)
    user_skills = SkillInstance.objects.filter(user_id=ui).all()

    context = RequestContext(request, {
        'current_user': str(current_user),
        "page": "profile",
        "username": current_user.username,
        "user_skills": user_skills,
    })
    logger.debug("User: " + str(current_user))
    return HttpResponse(template.render(context))


def registration(request):
    logger.debug("REGISTRATION")
    if request.user.is_active:
        return HttpResponse("Already registered")
    else:
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        skill1 = request.POST.get('skill1', '')
        skill2 = request.POST.get('skill2', '')
        skill3 = request.POST.get('skill3', '')
        skill1info = request.POST.get('skill1info', '')
        skill2info = request.POST.get('skill2info', '')
        skill3info = request.POST.get('skill3info', '')
        logger.debug("reg user:" + email)
        logger.debug("reg pw:" + password)
        if email:
            try:
                u = User.objects.create_user(username=str(username), email=email, password=str(password))
                u.set_password(password)
                u.save()
            except Exception:
                return HttpResponse("This username is taken.")
            user = auth.authenticate(username=str(username), password=str(password))
            ui = UserInfo(message="{}::{}::{}".format(skill1, skill2, skill3), authuser_id_id=u.id)
            ui.save()

            if skill1:
                try:
                    s = SkillType.objects.get(name=skill1)
                except Exception:
                    s = None
                if s:
                    si = SkillInstance(user_id=ui, skill_type_id=s, instance_type="Offer",snippet=skill1info)
                    si.save()

            if skill2:
                try:
                    s = SkillType.objects.get(name=skill2)
                except Exception:
                    s = None
                if s:
                    si = SkillInstance(user_id=ui, skill_type_id=s, instance_type="Offer",snippet=skill2info)
                    si.save()

            if skill3:
                try:
                   s = SkillType.objects.get(name=skill3)
                except Exception:
                    s = None
                if s:
                    si = SkillInstance(user_id=ui, skill_type_id=s, instance_type="Offer",snippet=skill3info)
                    si.save()

            
            auth.login(request, user)
            return redirect("/")

        template = loader.get_template('app/registration.html')
        context = RequestContext(request, {
            'current_user': str(request.user),
            "page": "registration",
        })
        logger.debug("Data: " + str(email) + " " + str(password) + " " + str(skill1))

        return HttpResponse(template.render(context))
