from django.http import JsonResponse


from portal.func.functionCommon import *

from portal.Constant import REQUEST_SUCCESS, REQUEST_ERROR, LOGIN_NEED, USER_EXISTS, PASSWORD_WRONG, NO_SUCH_USER

import hashlib

import time

import json

from portal.models import User, UserProfile


def need_login(func):
    def _need_login(request):
        if not session_params(request, "user_id"):
            return JsonResponse({
                "error_no": REQUEST_ERROR,
                "message": LOGIN_NEED
            })
        else:
            return func(request)

    return _need_login


def insert_user(request):
    user_id = get_params(request, "user_id")
    password = get_params(request, "password")
    m = hashlib.md5()
    m.update(password)
    password = str(m.hexdigest())
    email = get_params(request, "email")
    mobile = get_params(request, "mobile")
    name = get_params(request, "name")
    id_card = get_params(request, "id_card")
    age = get_params(request, "age")
    sex = get_params(request, "sex")
    exist_user = User.objects.filter(user_id=user_id)
    if len(exist_user):
        return JsonResponse({
            "error_no": REQUEST_ERROR,
            "message": USER_EXISTS
        })
    else:
        u = User(user_id=user_id, name=name, mobile=mobile, email=email, sex=sex, age=age, id_card=id_card)
        u.save()
        upf = UserProfile(user=u, password=password)
        upf.save()
    return JsonResponse({
        "error_no": REQUEST_SUCCESS
    })


@need_login
def user_info(request):
    user_id = get_params(request, "user_id")
    uc = user_cache.get_cache(user_id, time.time())
    return JsonResponse({
        "error_no": REQUEST_SUCCESS,
        "data": json.loads(uc)
    })


def login(request):
    user_id = get_params(request, "user_id")
    password = get_params(request, "password")
    m = hashlib.md5()
    m.update(password)
    password = str(m.hexdigest())
    u = User.objects.filter(user_id=user_id)
    if len(u):
        upf = UserProfile.objects.filter(user=u[0])
        if len(upf):
            if upf[0].password == password:
                request.session['id'] = u[0].id
                request.session['user_id'] = u[0].user_id
                return JsonResponse({
                    "error_no": REQUEST_SUCCESS
                })
            else:
                return JsonResponse({
                    "error_no": REQUEST_ERROR,
                    "message": PASSWORD_WRONG
                })
        else:
            return JsonResponse({
                "error_no": REQUEST_ERROR,
                "message": NO_SUCH_USER
            })
    else:
        return JsonResponse({
            "error_no": REQUEST_ERROR,
            "message": NO_SUCH_USER
        })

@need_login
def logout(request):
    request.session['id'] = ""
    request.session['user_id'] = ""
    return JsonResponse({
        "error_no": REQUEST_SUCCESS
    })
