from pathlib import Path
import environ
import os

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
SECRETS_PATH_FILE = os.environ.get('SECRETS_PATH_FILE', None)
environ.Env.read_env(SECRETS_PATH_FILE)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_saml2_auth',
    'django_extensions',
    # Custom
    'public',
    'private',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SAML2_AUTH = {
    # Metadata is required, choose either remote url or local file path
    'METADATA_AUTO_CONF_URL': os.environ.get("SAML2_AUTH_METADATA_AUTO_CONF_URL"),

    'DEBUG': os.environ.get("SAML2_AUTH_DEBUG"),  # Send debug information to a log file
    # Optional logging configuration.
    # By default, it won't log anything.
    # The following configuration is an example of how to configure the logger,
    # which can be used together with the DEBUG option above. Please note that
    # the logger configuration follows the Python's logging configuration schema:
    # https://docs.python.org/3/library/logging.config.html#logging-config-dictschema
    'LOGGING': {
        'version': 1,
        'formatters': {
            'simple': {
                'format': '[%(asctime)s] [%(levelname)s] [%(name)s.%(funcName)s] %(message)s',
            },
        },
        'handlers': {
            'stdout': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'level': 'DEBUG',
                'formatter': 'simple',
            },
        },
        'loggers': {
            'saml2': {
                'level': 'DEBUG'
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': [
                'stdout',
            ],
        },
    },

    # Optional settings below
    'DEFAULT_NEXT_URL': os.environ.get('SAML2_AUTH_DEFAULT_NEXT_URL'),  # Custom target redirect URL after the user get logged in. Default to /admin if not set. This setting will be overwritten if you have parameter ?next= specificed in the login URL.
    'CREATE_USER': True,  # Create a new Django user when a new user logs in. Defaults to True.
    'NEW_USER_PROFILE': {
        'USER_GROUPS': [os.environ.get("SAML2_AUTH_NEW_USER_PROFILE_USER_GROUPS")],  # The default group name when a new user logs in
        'ACTIVE_STATUS': os.environ.get("SAML2_AUTH_NEW_USER_PROFILE_ACTIVE_STATUS"),  # The default active status for new users
        'STAFF_STATUS': os.environ.get("SAML2_AUTH_NEW_USER_PROFILE_STAFF_STATUS"),  # The staff status for new users
        'SUPERUSER_STATUS': os.environ.get("SAML2_AUTH_NEW_USER_PROFILE_SUPERUSER_STATUS"),  # The superuser status for new users
    },
    'ATTRIBUTES_MAP': {  # Change Email/UserName/FirstName/LastName to corresponding SAML2 userprofile attributes.
        'email': os.environ.get('SAML2_AUTH_ATTRIBUTES_MAP_email'),
        'username': os.environ.get('SAML2_AUTH_ATTRIBUTES_MAP_username'),
        'first_name': os.environ.get('SAML2_AUTH_ATTRIBUTES_MAP_first_name'),
        'last_name': os.environ.get('SAML2_AUTH_ATTRIBUTES_MAP_last_name'),
        #'token': 'Token',  # Mandatory, can be unrequired if TOKEN_REQUIRED is False
        #'groups': 'Groups',  # Optional
    },
    #'GROUPS_MAP': {  # Optionally allow mapping SAML2 Groups to Django Groups
    #    'SAML Group Name': 'Django Group Name',
    #},
    #'TRIGGER': {
    #    # Optional: needs to return a User Model instance or None
    #    'GET_USER': 'path.to.your.get.user.hook.method',
    #    'CREATE_USER': 'path.to.your.new.user.hook.method',
    #    'BEFORE_LOGIN': 'path.to.your.login.hook.method',
    #    'AFTER_LOGIN': 'path.to.your.after.login.hook.method',
    #    # Optional. This is executed right before METADATA_AUTO_CONF_URL.
    #    # For systems with many metadata files registered allows to narrow the search scope.
    #    'GET_USER_ID_FROM_SAML_RESPONSE': 'path.to.your.get.user.from.saml.hook.method',
    #    # This can override the METADATA_AUTO_CONF_URL to enumerate all existing metadata autoconf URLs
    #    'GET_METADATA_AUTO_CONF_URLS': 'path.to.your.get.metadata.conf.hook.method',
    #},
    'ASSERTION_URL': os.environ.get("SAML2_AUTH_ASSERTION_URL"),  # Custom URL to validate incoming SAML requests against
    'ENTITY_ID': os.environ.get("SAML2_AUTH_ENTITY_ID"),  # Populates the Issuer element in authn request
    'NAME_ID_FORMAT': 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name', #FormatString'',  # Sets the Format property of authn NameIDPolicy element, e.g. 'user.email'
    'USE_JWT': False,  # Set this to True if you are running a Single Page Application (SPA) with Django Rest Framework (DRF), and are using JWT authentication to authorize client users
    #'JWT_ALGORITHM': 'HS256',  # JWT algorithm to sign the message with
    #'JWT_SECRET': 'your.jwt.secret',  # JWT secret to sign the message with
    #'JWT_PRIVATE_KEY': '--- YOUR PRIVATE KEY ---',  # Private key to sign the message with. The algorithm should be set to RSA256 or a more secure alternative.
    #'JWT_PRIVATE_KEY_PASSPHRASE': 'your.passphrase',  # If your private key is encrypted, you might need to provide a passphrase for decryption
    #'JWT_PUBLIC_KEY': '--- YOUR PUBLIC KEY ---',  # Public key to decode the signed JWT token
    #'JWT_EXP': 60,  # JWT expiry time in seconds
    #'FRONTEND_URL': 'https://myfrontendclient.com',  # Redirect URL for the client if you are using JWT auth with DRF. See explanation below
    #'LOGIN_CASE_SENSITIVE': False,  # whether of not to get the user in case_sentive mode
    #'AUTHN_REQUESTS_SIGNED': True, # Require each authentication request to be signed
    #'LOGOUT_REQUESTS_SIGNED': True,  # Require each logout request to be signed
    #'WANT_ASSERTIONS_SIGNED': True,  # Require each assertion to be signed
    'WANT_RESPONSE_SIGNED': False,  # Require response to be signed
    #'ACCEPTED_TIME_DIFF': None,  # Accepted time difference between your server and the Identity Provider
    'ALLOWED_REDIRECT_HOSTS': [os.environ.get("SAML2_AUTH_ALLOWED_REDIRECT_HOSTS")], # Allowed hosts to redirect to using the ?next parameter
    'TOKEN_REQUIRED': False,  # Whether or not to require the token parameter in the SAML assertion
}