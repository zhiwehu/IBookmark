#Configuration
#
#Add social_auth to PYTHONPATH and installed applications:
#
#INSTALLED_APPS = (
#    ...
#    "social_auth"
#)
#
#Add desired authentication backends to AUTHENTICATION_BACKENDS setting:
#
from django.core.urlresolvers import reverse

AUTHENTICATION_BACKENDS = (
#    "django.contrib.auth.backends.ModelBackend",
    "account.auth_backends.AuthenticationBackend",
#    "social_auth.backends.twitter.TwitterBackend",
    "social_auth.backends.facebook.FacebookBackend",
#    "social_auth.backends.google.GoogleOAuthBackend",
#    "social_auth.backends.google.GoogleOAuth2Backend",
    "social_auth.backends.google.GoogleBackend",
#    "social_auth.backends.yahoo.YahooBackend",
#    "social_auth.backends.contrib.linkedin.LinkedinBackend",
#    "social_auth.backends.contrib.livejournal.LiveJournalBackend",
#    "social_auth.backends.contrib.orkut.OrkutBackend",
#    "social_auth.backends.contrib.foursquare.FoursquareBackend",
#    "social_auth.backends.contrib.github.GithubBackend",
#    "social_auth.backends.contrib.dropbox.DropboxBackend",
#    "social_auth.backends.contrib.flickr.FlickrBackend",
#    "social_auth.backends.OpenIDBackend",
#    "django.contrib.auth.backends.ModelBackend",
#    "sina_oauth2.backends.sina.SinaWeiboBackend",
)
#
#The application will try to import custom backends from the sources defined in:
#
SOCIAL_AUTH_IMPORT_BACKENDS = (
    "sina_oauth2.backends",
)
#
#This way it"s easier to add new providers, check the already defined ones in social_auth.backends for examples.
#
#Take into account that backends must be defined in AUTHENTICATION_BACKENDS or Django won"t pick them when trying to authenticate the user.
#
#All backends are enabled by default.
#
#Setup needed OAuth keys (see OAuth section for details):
#
#TWITTER_CONSUMER_KEY         = ""
#TWITTER_CONSUMER_SECRET      = ""
FACEBOOK_APP_ID              = '203404126401249'
FACEBOOK_API_SECRET          = 'f101067288e758e39e6854376623217a'
#SINAWEIBO_APP_ID              = '3926699931'
#SINAWEIBO_API_SECRET          = '7872e7b8dcb0a25c833b1a8adc95c43f'
#LINKEDIN_CONSUMER_KEY        = ""
#LINKEDIN_CONSUMER_SECRET     = ""
#ORKUT_CONSUMER_KEY           = ""
#ORKUT_CONSUMER_SECRET        = ""
#GOOGLE_CONSUMER_KEY          = ""
#GOOGLE_CONSUMER_SECRET       = ""
#GOOGLE_OAUTH2_CLIENT_ID      = ""
#GOOGLE_OAUTH2_CLIENT_SECRET  = ""
#FOURSQUARE_CONSUMER_KEY      = ""
#FOURSQUARE_CONSUMER_SECRET   = ""
#GITHUB_APP_ID                = ""
#GITHUB_API_SECRET            = ""
#DROPBOX_APP_ID               = ""
#DROPBOX_API_SECRET           = ""
#FLICKR_APP_ID                = ""
#FLICKR_API_SECRET            = ""
#
#Setup login URLs:
#
#LOGIN_URL          = "/login-form/"
LOGIN_REDIRECT_URL = "/account/social/"
#LOGIN_ERROR_URL    = "/login-error/"
#
#Check Django documentation at Login URL and Login redirect URL
#
#If a custom redirect URL is needed that must be different to LOGIN_URL, define the setting:
#
#SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/another-login-url/"
#
#A different URL could be defined for newly registered users:
#
#SOCIAL_AUTH_NEW_USER_REDIRECT_URL = "/new-users-redirect-url/"
#
#or for newly associated accounts:
#
#SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = "/new-association-redirect-url/"
#
#or for account disconnections:
#
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = "/account/social/"
#
#In case of authentication error, the message can be stored in session if the following setting is defined:
#
#SOCIAL_AUTH_ERROR_KEY = "social_errors"
#
#This defines the desired session key where last error message should be stored. It"s disabled by default.
#
#Configure authentication and association complete URL names to avoid possible clashes:
#
#SOCIAL_AUTH_COMPLETE_URL_NAME  = "socialauth_complete"
#SOCIAL_AUTH_ASSOCIATE_URL_NAME = "socialauth_associate_complete"
#
#Add URLs entries:
#
#urlpatterns = patterns("",
#    ...
#    url(r"", include("social_auth.urls")),
#    ...
#)
#
#All django-social-auth URLs names have socialauth_ prefix.
#
#Define context processors if needed:
#
# TEMPLATE_CONTEXT_PROCESSORS = (
#     ...
#     "social_auth.context_processors.social_auth_by_type_backends",
# )
#
#check `social_auth.context_processors`.
#
#Sync database to create needed models:
#
#./manage.py syncdb
#
#Not mandatory, but recommended:
#
#SOCIAL_AUTH_DEFAULT_USERNAME = "new_social_auth_user"
#
#or:
#
#import random
#SOCIAL_AUTH_DEFAULT_USERNAME = lambda: random.choice(["Darth Vader", "Obi-Wan Kenobi", "R2-D2", "C-3PO", "Yoda"])
#
#or:
#
#from django.template.defaultfilters import slugify
#SOCIAL_AUTH_USERNAME_FIXER = lambda u: slugify(u)
#
#in case your user layout needs to purify username on some weird way.
#
#Final user name will have a random UUID-generated suffix in case it"s already taken. The UUID token max length can be changed with the setting:
#
#SOCIAL_AUTH_UUID_LENGTH = 16
#
#Backends will store extra values from response by default, set this to False to avoid such behavior:
#
#SOCIAL_AUTH_EXTRA_DATA = False
#
#Also more extra values will be stored if defined, details about this setting are listed below on OpenId and OAuth sections.
#
#Session expiration time is an special value, it"s recommended to define:
#
#SOCIAL_AUTH_EXPIRATION = "expires"
#
#and use such setting name where expiration times are returned. View that completes login process will set session expiration time using this name if it"s present or expires by default. Expiration configuration can be disabled with setting:
#
#SOCIAL_AUTH_SESSION_EXPIRATION = False
#
#It"s possible to override the used User model if needed:
#
#SOCIAL_AUTH_USER_MODEL = "myapp.CustomUser"
#
#This class must have a custom Model Manager with a create_user method that resembles the one on auth.UserManager.
#
#Also, it"s highly recommended that this class define the following fields:
#
#username   = CharField(...)
#last_login = DateTimeField(blank=True)
#is_active  = BooleanField(...)
#
#and the method:
#
#is_authenticated():
#    ...
#
#These are needed to ensure a better django-auth integration, in other case login_required won"t be usable. A warning is displayed if any of these are missing. By default auth.User is used.
#
#Check example application for implementation details, but first, please take a look to User Profiles, it might be what you were looking for.
#
#It"s possible to disable user creations by django-social-auth with:
#
#SOCIAL_AUTH_CREATE_USERS = False
#
#It is also possible to associate multiple user accounts with a single email address as long as the rest of the user data is unique. Set value as True to enable, otherwise set as False to disable. This behavior is disabled by default (false) unless specifically set:
#
SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True
#
#You can send extra parameters on auth process by defining settings per provider, example to request Facebook to show Mobile authorization page, define:
#
#FACEBOOK_AUTH_EXTRA_ARGUMENTS = {"display": "touch"}
#
#For other providers, just define settings in the form:
#
#<uppercase backend name>_AUTH_EXTRA_ARGUMENTS = {...}
#
#By default the application doesn"t make redirects to different domains, to disable this behavior:
#
#SOCIAL_AUTH_SANITIZE_REDIRECTS = False
#
#Signals
#
#A pre_update signal is sent when user data is about to be updated with new values from authorization service provider, this apply to new users and already existent ones. This is useful to update custom user fields or User Profiles, for example, to store user gender, location, etc. Example:
#
#from social_auth.signals import pre_update
#from social_auth.backends.facebook import FacebookBackend
#
#def facebook_extra_values(sender, user, response, details, **kwargs):
#user.gender = response.get("gender")
#return True
#
#pre_update.connect(facebook_extra_values, sender=FacebookBackend)
#
#New data updating is made automatically but could be disabled and left only to signal handler if this setting value is set to True:
#
#SOCIAL_AUTH_CHANGE_SIGNAL_ONLY = False
#
#Take into account that when defining a custom User model and declaring signal handler in models.py, the imports and handler definition must be made after the custom User model is defined or circular imports issues will be raised.
#
#Also a new-user signal (socialauth_registered) is sent when new accounts are created:
#
#from social_auth.signals import socialauth_registered
#
#def new_users_handler(sender, user, response, details, **kwargs):
#user.is_new = True
#return False
#
#socialauth_registered.connect(new_users_handler, sender=None)
#
#OpenId
#
#OpenId support is simpler to implement than OAuth. Google and Yahoo providers are supported by default, others are supported by POST method providing endpoint URL.
#
#OpenId backends can store extra data in UserSocialAuth.extra_data field by defining a set of values names to retrieve from any of the used schemas, AttributeExchange and SimpleRegistration. As their keywords differ we need two settings.
#
#Settings is per backend, so we have two possible values for each one. Name is dynamically checked using uppercase backend name as prefix:
#
#<uppercase backend name>_SREG_EXTRA_DATA
#<uppercase backend name>_AX_EXTRA_DATA
#
#Example:
#
#GOOGLE_SREG_EXTRA_DATA = [(..., ...)]
#GOOGLE_AX_EXTRA_DATA = [(..., ...)]
#
#Settings must be a list of tuples mapping value name in response and value alias used to store.
#OAuth
#
#OAuth communication demands a set of keys exchange to validate the client authenticity prior to user approbation. Twitter, Facebook and Orkut facilitates these keys by application registration, Google works the same, but provides the option for unregistered applications.
#
#Check next sections for details.
#
#OAuth backends also can store extra data in UserSocialAuth.extra_data field by defining a set of values names to retrieve from service response.
#
#Settings is per backend and it"s name is dynamically checked using uppercase backend name as prefix:
#
#<uppercase backend name>_EXTRA_DATA
#
#Example:
#
#FACEBOOK_EXTRA_DATA = [(..., ...)]
#
#Settings must be a list of tuples mapping value name in response and value alias used to store.
#Twitter
#
#Twitter offers per application keys named Consumer Key and Consumer Secret. To enable Twitter these two keys are needed. Further documentation at Twitter development resources:
#
#Register a new application at Twitter App Creation,
#
#mark the "Yes, use Twitter for login" checkbox, and
#
#fill Consumer Key and Consumer Secret values:
#
#TWITTER_CONSUMER_KEY
#TWITTER_CONSUMER_SECRET
#
#You need to specify an URL callback or the application will be marked as Client type instead of the Browser. Almost any dummy value will work if you plan some test.
#
#Facebook
#
#Facebook works similar to Twitter but it"s simpler to setup and redirect URL is passed as a parameter when issuing an authorization. Further documentation at Facebook development resources:
#
#Register a new application at Facebook App Creation, and
#
#fill App Id and App Secret values in values:
#
#FACEBOOK_APP_ID
#FACEBOOK_API_SECRET
#
#also it"s possible to define extra permissions with:
#
#FACEBOOK_EXTENDED_PERMISSIONS = [...]
#
#If you define a redirect URL in Facebook setup page, be sure to not define http://127.0.0.1:8000 or http://localhost:8000 because it won"t work when testing. Instead I define http://myapp.com and setup a mapping on /etc/hosts or use dnsmasq.
#Orkut
#
#Orkut offers per application keys named Consumer Key and Consumer Secret. To enable Orkut these two keys are needed.
#
#Check Google support and Orkut API for details on getting your consumer_key and consumer_secret keys.
#
#fill Consumer Key and Consumer Secret values:
#
#ORKUT_CONSUMER_KEY
#ORKUT_CONSUMER_SECRET
#
#add any needed extra data to:
#
#ORKUT_EXTRA_DATA = ""
#
#configure extra scopes in:
#
#ORKUT_EXTRA_SCOPES = [...]
#
#Google OAuth
#
#Google provides Consumer Key and Consumer Secret keys to registered applications, but also allows unregistered application to use their authorization system with, but beware that this method will display a security banner to the user telling that the application is not trusted.
#
#Check Google OAuth and make your choice.
#
#fill Consumer Key and Consumer Secret values:
#
#GOOGLE_CONSUMER_KEY
#GOOGLE_CONSUMER_SECRET
#
#anonymous values will be used if not configured as described in their OAuth reference
#
#configure the display name to be used in the "grant permissions" dialog that Google will display to users in:
#
#GOOGLE_DISPLAY_NAME = ""
#
#shows "Social Auth" by default, but that might not suite your application.
#
#setup any needed extra scope in:
#
#GOOGLE_OAUTH_EXTRA_SCOPE = [...]
#
#Check which applications can be included in their Google Data Protocol Directory
#Google OAuth2
#
#Recently Google launched OAuth2 support following the definition at OAuth2 draft. It works in a similar way to plain OAuth mechanism, but developers must register an application and apply for a set of keys. Check Google OAuth2 document for details.
#
#Note:
#This support is experimental as Google implementation may change and OAuth2 is still a draft.
#
#To enable OAuth2 support:
#
#fill Client ID and Client Secret settings, these values can be obtained easily as described on OAuth2 Registering doc:
#
#GOOGLE_OAUTH2_CLIENT_ID = ""
#GOOGLE_OAUTH2_CLIENT_SECRET = ""
#
#previous name GOOGLE_OAUTH2_CLIENT_KEY is supported for backward compatibility.
#
#scopes are shared between OAuth mechanisms:
#
#GOOGLE_OAUTH_EXTRA_SCOPE = [...]
#
#Check which applications can be included in their Google Data Protocol Directory
#LinkedIn
#
#LinkedIn setup is similar to any other OAuth service. To request extra fields using LinkedIn fields selectors just define the setting:
#
#LINKEDIN_EXTRA_FIELD_SELECTORS = [...]
#
#with the needed fields selectors, also define LINKEDIN_EXTRA_DATA properly, that way the values will be stored in UserSocialAuth.extra_data field.
#
#By default id, first-name and last-name are requested and stored.
#GitHub
#
#GitHub works similar to Facebook (OAuth).
#
#Register a new application at GitHub Developers, and
#
#fill App Id and App Secret values in the settings:
#
#GITHUB_APP_ID = ""
#GITHUB_API_SECRET = ""
#
#also it"s possible to define extra permissions with:
#
#GITHUB_EXTENDED_PERMISSIONS = [...]
#
#Dropbox
#
#Dropbox uses OAuth v1.0 for authentication.
#
#Register a new application at Dropbox Developers, and
#
#fill App Key and App Secret values in the settings:
#
#DROPBOX_APP_ID = ""
#DROPBOX_API_SECRET = ""
#
#Flickr
#
#Flickr uses OAuth v1.0 for authentication.
#
#Register a new application at the Flickr App Garden, and
#
#fill Key and Secret values in the settings:
#
#FLICKR_APP_ID = ""
#FLICKR_API_SECRET = ""
#
#