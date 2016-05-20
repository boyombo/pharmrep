from datetime import datetime


def last_activity(func):
    def inner(request, *args, **kwargs):
        ret = func(request, *args, **kwargs)
        rep = request.user.rep
        rep.last_activity = datetime.now()
        rep.save()
        return ret
    return inner
