from django.conf import settings

from models import Account, AnonymousAccount


def account(request):
    if request.user.is_authenticated():
        try:
            account = Account._default_manager.get(user=request.user)
        except Account.DoesNotExist:
            account = AnonymousAccount(request)
    else:
        account = AnonymousAccount(request)
    return {
        "account": account,
        "CONTACT_EMAIL": getattr(settings, "CONTACT_EMAIL", "admin@ibookmark.me")
    }
