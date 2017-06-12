from django.contrib.auth import views as auth_views
from django.utils.decorators import method_decorator

from .decorators import watch_login


class FailedLoginMiddleware(object):
    patched = False

    def __init__(self, *args, **kwargs):
        super(FailedLoginMiddleware, self).__init__(*args, **kwargs)

        # Watch the auth login.
        # Monkey-patch only once - otherwise we would be recording
        # failed attempts multiple times!
        if not FailedLoginMiddleware.patched:
            # Django 1.11 turned the `login` function view into the
            # `LoginView` class-based view
            try:
                from django.contrib.auth.views import LoginView
                watch_login_method = method_decorator(watch_login)
                LoginView.dispatch = watch_login_method(LoginView.dispatch)
            except ImportError:  # Django < 1.11
                auth_views.login = watch_login(auth_views.login)

            FailedLoginMiddleware.patched = True
