def get_params(request, name):
    return request.GET.get(name)


def post_params(request, name):
    return request.POST.get(name)


def session_params(request, name):
    return request.session.get(name)


def cookie_params(request, name):
    return request.cookie.get(name)


def convert_to_dict(obj):
    dict = {}
    dict.update(obj.__dict__)
    return dict
