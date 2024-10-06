from urllib.parse import quote

from social_core.utils import (
    partial_pipeline_data,
    sanitize_redirect,
    setting_url,
    user_is_active,
    user_is_authenticated,
)

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from social_django.utils import psa
from social_django.views import NAMESPACE, _do_login
from django.contrib.auth import REDIRECT_FIELD_NAME

from applications.users.services import generate_jwt_token


def do_complete(backend, login, user=None, redirect_name="next", *args, **kwargs):
    data = backend.strategy.request_data()

    is_authenticated = user_is_authenticated(user)
    user = user if is_authenticated else None

    partial = partial_pipeline_data(backend, user, *args, **kwargs)
    if partial:
        user = backend.continue_pipeline(partial)
        # clean partial data after usage
        backend.strategy.clean_partial_pipeline(partial.token)
    else:
        user = backend.complete(user=user, *args, **kwargs)

    # pop redirect value before the session is trashed on login(), but after
    # the pipeline so that the pipeline can change the redirect if needed
    redirect_value = backend.strategy.session_get(redirect_name, "") or data.get(
        redirect_name, ""
    )

    # check if the output value is something else than a user and just
    # return it to the client
    user_model = backend.strategy.storage.user.user_model()
    if user and not isinstance(user, user_model):
        return user

    if is_authenticated:
        if not user:
            url = setting_url(backend, redirect_value, "LOGIN_REDIRECT_URL")
        else:
            url = setting_url(
                backend,
                redirect_value,
                "NEW_ASSOCIATION_REDIRECT_URL",
                "LOGIN_REDIRECT_URL",
            )
    elif user:
        if user_is_active(user):
            # catch is_new/social_user in case login() resets the instance
            is_new = getattr(user, "is_new", False)
            social_user = user.social_user
            login(backend, user, social_user)
            # store last login backend name in session
            backend.strategy.session_set(
                "social_auth_last_login_backend", social_user.provider
            )

            if is_new:
                url = setting_url(
                    backend,
                    "NEW_USER_REDIRECT_URL",
                    redirect_value,
                    "LOGIN_REDIRECT_URL",
                )
            else:
                url = setting_url(backend, redirect_value, "LOGIN_REDIRECT_URL")
        else:
            if backend.setting("INACTIVE_USER_LOGIN", False):
                social_user = user.social_user
                login(backend, user, social_user)
            url = setting_url(
                backend, "INACTIVE_USER_URL", "LOGIN_ERROR_URL", "LOGIN_URL"
            )
    else:
        url = setting_url(backend, "LOGIN_ERROR_URL", "LOGIN_URL")

    if redirect_value and redirect_value != url:
        redirect_value = quote(redirect_value)
        url += ("&" if "?" in url else "?") + f"{redirect_name}={redirect_value}"

    if backend.setting("SANITIZE_REDIRECTS", True):
        allowed_hosts = backend.setting("ALLOWED_REDIRECT_HOSTS", []) + [
            backend.strategy.request_host()
        ]
        url = sanitize_redirect(allowed_hosts, url) or backend.setting(
            "LOGIN_REDIRECT_URL"
        )

    # add auth data to url for FE
    if user:
        # generate access token and return it to user
        request = kwargs.get("request", None)

        if request:
            auth_data = generate_jwt_token(request, user)

            if auth_data:
                url += ("&" if "?" in url else "?") + "&".join([f"{k}={v}" for k, v in auth_data.items()])

    return backend.strategy.redirect(url)


@never_cache
@csrf_exempt
@psa(f"{NAMESPACE}:complete")
def complete(request, backend, *args, **kwargs):
    """Authentication complete view"""
    return do_complete(
        request.backend,
        _do_login,
        user=request.user,
        redirect_name=REDIRECT_FIELD_NAME,
        request=request,
        *args,
        **kwargs,
    )
