from brf.settings_base import *

STAGE = True

DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': 'brf',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',  # Or an IP Address that your DB is hosted on
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

# STRIPE_LIVE_PUBLIC_KEY = ''  # os.environ.get("STRIPE_LIVE_PUBLIC_KEY", "<your publishable key>")
# STRIPE_LIVE_SECRET_KEY = ''  # os.environ.get("STRIPE_LIVE_SECRET_KEY", "<your secret key>")
# STRIPE_TEST_PUBLIC_KEY = 'pk_test_51HiftwIlMtWWDUzA2gSajpvxNaXgDFVJwl97UbOtJAgWIVDshUzGO9sF2GUuSHyLR97noZC8YGI9K6due2FH8Lo300fGz1hCTW'  # os.environ.get("STRIPE_TEST_PUBLIC_KEY", "<your publishable key>")
# STRIPE_TEST_SECRET_KEY = 'sk_test_51HiftwIlMtWWDUzAXCb8gzTg8vN0XamDyKIUqMIKye1LUKJ5xLtvFfwZOooof7cv7BNpTSAZGa2nQMCbafhf4DHe00dps4qw0z'  # os.environ.get("STRIPE_TEST_SECRET_KEY", "<your secret key>")
# STRIPE_LIVE_MODE = False  # Change to True in production
# DJSTRIPE_WEBHOOK_SECRET = "whsec_xxx"  # Get it from the section in the Stripe dashboard where you added the webhook endpoint
# DJSTRIPE_FOREIGN_KEY_TO_FIELD='djstripe_id'
# UNITPAY_PUBLIC = "15bb80b0e1d4f4aca55a5445466c5f5b"
# UNITPAY_PUBLIC_KEY = "347601-2d399"
# UNITPAY_SECRET = "A0B06DF16D4-89ADCAB337C-0D3C5A82DA"
# UNITPAY_SECRET_TEST = "D94ACBA64AC-AEACFBBFBFB-1D43C55AD2"
#
# COINBASE_API_KEY = "8f9a85bd-fe5a-41f1-8593-8098748ad483"
# COINBASE_WEBHOOK_SHARED = "7f3f9c1d-922e-4958-9035-623ecdbbef43"
#
# PAYPAL_CLIENT_ID = "AQ7KcDn2x7sFom7D3M9HDux56JWL_wAEjSfhGYYsb54wDOYyXFp7_FycFUNiDu3wr_vWt0UJ5ppq0asH"
# PAYPAL_CLIENT_SECRET = "EJwOwEB7zl5LJwGyhX1_o0Z7IFP-J-NdF2bgYQ3S1tbJ9u3d6r5udQJeVQuXOQSP_pkaRDBUputPwsfE"

DEBUG = True
