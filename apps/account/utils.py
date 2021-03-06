from django.conf import settings
from django.core.urlresolvers import reverse



LOGIN_REDIRECT_URLNAME = getattr(settings, "LOGIN_REDIRECT_URLNAME", "")



def get_default_redirect(request, redirect_field_name="next",
        login_redirect_urlname=LOGIN_REDIRECT_URLNAME):
    """
    Returns the URL to be used in login procedures by looking at different
    values in the following order:

    - a REQUEST value, GET or POST, named "next" by default.
    - LOGIN_REDIRECT_URL - the URL in the setting
    - LOGIN_REDIRECT_URLNAME - the name of a URLconf entry in the settings
    """
    if login_redirect_urlname:
        default_redirect_to = reverse(login_redirect_urlname)
    else:
        default_redirect_to = settings.LOGIN_REDIRECT_URL
    redirect_to = request.REQUEST.get(redirect_field_name)
    # light security check -- make sure redirect_to isn't garabage.
    if not redirect_to or "://" in redirect_to or " " in redirect_to:
        try:
            redirect_to = request.user.get_profile().primary_group.get_absolute_url()
        except:
            redirect_to = default_redirect_to
        return redirect_to


def user_display(user):
    func = getattr(settings, "ACCOUNT_USER_DISPLAY", lambda user: user.username)
    return func(user)
