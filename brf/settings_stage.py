from brf.settings_base import *

STAGE = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gvital',
        'USER': 'admin',
        'PASSWORD': '4_u@MdBrJ3h9hsC9',
        'HOST': 'localhost',  # Or an IP Address that your DB is hosted on
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

# AWS_SES_IAM='ses-smtp-user.20200620-232754'arn:aws:iam::735606338233:user/ses-smtp-user.20201104-005649
# AWS_SES_IAM='ses-smtp-user.20201104-005649'
# AWS_SES_REGION='us-east-1'
# AWS_SES_ACCESS_KEY_ID='AKIA2WRMN6K4464PRN6M'
# AWS_SES_SECRET_ACCESS_KEY='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'
AWS_SES_IAM='ses-smtp-user.20201202-015549'
AWS_SES_REGION='us-east-1'
AWS_SES_ACCESS_KEY_ID='AKIAYUIOYLGAOPAHTO7X'
AWS_SES_SECRET_ACCESS_KEY='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'

SENDGRID_API_KEY='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'
SENDGRID_SANDBOX_MODE_IN_DEBUG=False
# STRIPE_TEST_PUBLIC_KEY = 'pk_test_51HiftwIlMtWWDUzA2gSajpvxNaXgDFVJwl97UbOtJAgWIVDshUzGO9sF2GUuSHyLR97noZC8YGI9K6due2FH8Lo300fGz1hCTW'#os.environ.get("STRIPE_TEST_PUBLIC_KEY", "<your publishable key>")
# STRIPE_TEST_SECRET_KEY = 'sk_test_51HiftwIlMtWWDUzAXCb8gzTg8vN0XamDyKIUqMIKye1LUKJ5xLtvFfwZOooof7cv7BNpTSAZGa2nQMCbafhf4DHe00dps4qw0z'#os.environ.get("STRIPE_TEST_SECRET_KEY", "<your secret key>")
# STRIPE_LIVE_MODE = False  # Change to True in production
# STRIPE_WEBHOOK_SECRET = "whsec_BKz5AGIgUlbNeciM2p4l1PiusOVgmGhi"
STRIPE_LIVE_PUBLIC_KEY = 'pk_live_51HYjkpF7BywwUH9urrLmJG3xl24r94ZI0rkFIeXCvP0Swhzrn8CChiJrCkje1Zclpd8GnrXjw67rgS3SQmU5LdoU00Duqt3boY'#os.environ.get("STRIPE_TEST_PUBLIC_KEY", "<your publishable key>")
STRIPE_LIVE_SECRET_KEY = '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'#os.environ.get("STRIPE_TEST_SECRET_KEY", "<your secret key>")
STRIPE_LIVE_MODE = True  # Change to True in production
STRIPE_LIVE_WEBHOOK_SECRET = "whsec_0n3C0dNChZTVayjE8gmVQWreIjsiwbC0"  # Get it from the section in the Stripe dashboard where you added the webhook endpoint
DJSTRIPE_WEBHOOK_SECRET = "whsec_BKz5AGIgUlbNeciM2p4l1PiusOVgmGhi"  # Get it from the section in the Stripe dashboard where you added the webhook endpoint

#STRIPE_LIVE_MODE = False
# STRIPE_LIVE_PUBLIC_KEY = "pk_test_51HiftwIlMtWWDUzA2gSajpvxNaXgDFVJwl97UbOtJAgWIVDshUzGO9sF2GUuSHyLR97noZC8YGI9K6due2FH8Lo300fGz1hCTW"
# STRIPE_LIVE_SECRET_KEY = "sk_test_51HiftwIlMtWWDUzAXCb8gzTg8vN0XamDyKIUqMIKye1LUKJ5xLtvFfwZOooof7cv7BNpTSAZGa2nQMCbafhf4DHe00dps4qw0z"

SITE_ID = 1
PAYPAL_TEST = True

PAYPAL_CLIENT_ID = "AQ7KcDn2x7sFom7D3M9HDux56JWL_wAEjSfhGYYsb54wDOYyXFp7_FycFUNiDu3wr_vWt0UJ5ppq0asH"
PAYPAL_CLIENT_ID_SAND = "AaRV2xyY7Zb4WL-wI7YHsqz8W3W7iXmINT38fA4tT_NmMyXORHUq6FW8dZzulkzrJXXszaTlET2dY8BH"
PAYPAL_CLIENT_SECRET = "EJwOwEB7zl5LJwGyhX1_o0Z7IFP-J-NdF2bgYQ3S1tbJ9u3d6r5udQJeVQuXOQSP_pkaRDBUputPwsfE"
PAYPAL_CLIENT_SECRET_SAND = "EMULWidhu77IHz4QBXOm1thyn10XDn-Bo6DaMnqGtXF4D6Q-sLWGt1oNYGc6m6NBr7HIcTi8kDCJ4q2w"

UNITPAY_PUBLIC = "15bb80b0e1d4f4aca55a5445466c5f5b"
UNITPAY_PUBLIC_KEY = "347601-2d399"
UNITPAY_PROJECT_ID = "347601"
UNITPAY_SECRET = "A0B06DF16D4-89ADCAB337C-0D3C5A82DA"
UNITPAY_SECRET_TEST = "D94ACBA64AC-AEACFBBFBFB-1D43C55AD2"

COINBASE_API_KEY = "9c531e46-9094-4998-ae0f-73df09f81726"#"8f9a85bd-fe5a-41f1-8593-8098748ad483"
COINBASE_WEBHOOK_SHARED = "7af9080c-cf81-4a1b-bd09-09664ad66943"#"7f3f9c1d-922e-4958-9035-623ecdbbef43"
DOMAIN = 'https://buyrealfollows.com'
