import requests
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.core.exceptions import ValidationError

from applications.users.utils import get_tokens_for_user

User = get_user_model()


def google_validate_id_token(*, id_token: str) -> bool:
    response = requests.get(
        settings.GOOGLE_ID_TOKEN_INFO_URL,
        params={'id_token': id_token}
    )
    """
    Response from Google API:
        {
            "iss": "https://accounts.google.com",
            "sub": "110169484474386276334",
            "azp": "1008719970978-hb24n2dstb40o45d4feuo2ukqmcc6381.apps.googleusercontent.com",
            "aud": "1008719970978-hb24n2dstb40o45d4feuo2ukqmcc6381.apps.googleusercontent.com",
            "iat": "1433978353",
            "exp": "1433981953"
        }
    """

    if not response.ok:
        raise ValidationError('id_token is invalid.')

    audience = response.json()['aud']

    if audience != settings.GOOGLE_OAUTH2_CLIENT_ID:
        raise ValidationError('Invalid audience.')

    return True


def generate_jwt_token(request, user):
    login(request, user)
    auth_data = get_tokens_for_user(request.user)
    return auth_data
