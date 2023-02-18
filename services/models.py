import datetime

from bitfield import BitField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
import uuid

from vendors.models import VendorApi, Vendor


class Meta(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True)
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    active = models.BooleanField(default=False)

    class Meta:
        abstract = True


# 100 - 1.99
# 250 - 3.99
# 500 -  6.49
# 1000 - 11.99
# 2500 - 27.99
# 5000 - 49.99
# 7500 - 70.99
# 10000- 89.99

class FAQ(Meta):
    question = models.TextField(max_length=200, blank=True)
    answer = models.TextField(blank=True, null=True)
    is_general = models.BooleanField(default=True)

    def __str__(self):
        return "%s General: %s" % (self.question, self.is_general)


class Platform(Meta):
    INSTAGRAM = 'INSTAGRAM'
    TWITTER = 'TWITTER'
    YOUTUBE = 'YOUTUBE'
    SPOTIFY = 'SPOTIFY'
    SOUNDCLOUD = 'SOUNDCLOUD'
    TWITCH = 'TWITCH'
    FACEBOOK = 'FACEBOOK'
    LINKEDIN = 'LINKEDIN'
    TIKTOK = 'TIKTOK'

    PLATFORM_TYPES_CHOICES = [
        (INSTAGRAM, 'INSTAGRAM'),
        (YOUTUBE, 'YOUTUBE'),
        (TWITTER, 'TWITTER'),
        (TWITCH, 'TWITCH'),
        (SOUNDCLOUD, 'SOUNDCLOUD'),
        (SPOTIFY, 'SPOTIFY'),
        (FACEBOOK, 'FACEBOOK'),
        (LINKEDIN, 'LINKEDIN'),
        (TIKTOK, 'TIKTOK'),
    ]

    name = models.CharField(max_length=100,
                            choices=PLATFORM_TYPES_CHOICES,
                            default=INSTAGRAM, )
    order = models.IntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    slug = models.CharField(max_length=350, blank=True, null=True)
    seo_title = models.TextField(blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    seo_keywords = models.TextField(blank=True, null=True)
    content = RichTextField(blank=True, null=True)
    faqs = models.ManyToManyField(FAQ, blank=True, default=None)

    def __str__(self):
        return "%s %s %s" % (self.order, self.name, self.description)


class LocalizeService(Meta):
    CITY_CHOICES = [('MYANMAR', 'myanmar'), ('ROMANIA', 'romania'), ('BARBADOS', 'barbados'), ('MEXICO', 'mexico'),
                    ('ETHIOPIA', 'ethiopia'), ('THE-GAMBIA', 'the-gambia'), ('IRAQ', 'iraq'),
                    ('NORFOLK-ISLAND', 'norfolk-island'), ('MACAU-SAR-(PRC)', 'macau sar (prc)'),
                    ('MACAU-SAR-(PRC)', 'macau-sar-(prc)'), ('ANDORRA', 'andorra'), ('COMOROS', 'comoros'),
                    ('MACAU', 'macau'), ('BURUNDI', 'burundi'), ('QATAR', 'qatar'), ('MOROCCO', 'morocco'),
                    ('CHILE', 'chile'), ('SPAIN', 'spain'), ('SINGAPORE', 'singapore'), ('LEBANON', 'lebanon'),
                    ('NEW-CALEDONIA', 'new%20caledonia'), ('MACAU-SAR-(PRC)', 'macau%20sar%20(prc)'),
                    ('HEARD-AND-MC-DONALD-ISLANDS', 'heard-and-mc-donald-islands'), ('KAZAKHSTAN', 'kazakhstan'),
                    ('BRAZIL', 'brazil'), ('NETHERLANDS', 'netherlands'), ('AUSTRALIA', 'australia'),
                    ('MONTSERRAT', 'montserrat'), ('ITALY', 'italy'), ('MALI', 'mali'), ('NORTH-KOREA', 'north-korea'),
                    ('KOREA', 'korea'), ('GERMANY', 'germany'), ('SOMALIA', 'somalia'), ('UZBEKISTAN', 'uzbekistan'),
                    ('MACEDONIA', 'macedonia'), ('NIGER', 'niger'), ('GUATEMALA', 'guatemala'), ('NORWAY', 'norway'),
                    ('LESOTHO', 'lesotho'), ('AFGHANISTAN', 'afghanistan'), ('MARTINIQUE', 'martinique'),
                    ('LIBYAN-ARAB-JAMAHIRIYA', 'libyan-arab-jamahiriya'), ('ALGERIA', 'algeria'), ('LIBYA', 'libya'),
                    ('GUAM', 'guam'), ('SAN-MARINO', 'san-marino'), ('SAN-MARINO', 'san%20marino'),
                    ('FRENCH-GUIANA', 'french-guiana'), ('MALDIVES', 'maldives'), ('SAINT-HELENA', 'saint-helena'),
                    ('CUBA', 'cuba'), ('SYRIA', 'syria'), ('GUINEA', 'guinea'), ('LIECHTENSTEIN', 'liechtenstein'),
                    ('CANADA', 'canada'), ('BOLIVIA', 'bolivia'), ('AMERICAN-SAMOA', 'american-samoa'),
                    ('ANGOLA', 'angola'), ('FIJI', 'fiji'), ('BAHAMAS', 'bahamas'), ('LUXEMBOURG', 'luxembourg'),
                    ('GRENADA', 'grenada'), ('NEW-ZEALAND', 'new-zealand'), ('ALBANIA', 'albania'),
                    ('BELGIUM', 'belgium'), ('FAROE-ISLANDS', 'faroe-islands'),
                    ('BRITISH-VIRGIN-ISLANDS', 'british-virgin-islands'), ('VATICAN-CITY-STATE', 'vatican-city-state'),
                    ('JAPAN', 'japan'), ('POLAND', 'poland'), ('VANUATU', 'vanuatu'), ('CAMEROON', 'cameroon'),
                    ('COCOS-ISLANDS', 'cocos-islands'), ('CONGO', 'congo'), ('ARMENIA', 'armenia'),
                    ('BELIZE', 'belize'), ('PALAU', 'palau'), ('FINLAND', 'finland'), ('BAHRAIN', 'bahrain'),
                    ('WALLIS-AND-FUTUNA-ISLANDS', 'wallis-and-futuna-islands'), ('GREENLAND', 'greenland'),
                    ('ISRAEL', 'israel'), ('DENMARK', 'denmark'), ('GEORGIA', 'georgia'), ('CHAD', 'chad'),
                    ('NORTHERN-MARIANA-ISLANDS', 'northern-mariana-islands'), ('NORFORK-ISLAND', 'norfork-island'),
                    ('KENYA', 'kenya'), ('CHINA', 'china'), ('MARSHALL-ISLANDS', 'marshall-islands'),
                    ('RUSSIAN-FEDERATION', 'russian-federation'), ('PARAGUAY', 'paraguay'),
                    ('COCOS--ISLANDS', 'cocos--islands'), ('MAURITANIA', 'mauritania'),
                    ('NETHERLANDS-ANTILLES', 'netherlands-antilles'), ('REUNION', 'reunion'), ('ARUBA', 'aruba'),
                    ('MALAYSIA', 'malaysia'), ('PERU', 'peru'), ('COOK-ISLANDS', 'cook-islands'), ('OMAN', 'oman'),
                    ('KOSOVO', 'kosovo'), ('NAMIBIA', 'namibia'), ('WESTERN-SAHARA', 'western-sahara'),
                    ('COLOMBIA', 'colombia'), ('TURKEY', 'turkey'), ('IVORY-COAST', 'ivory-coast'),
                    ('GREECE', 'greece'), ('CENTRAL-AFRICAN-REPUBLIC', 'central-african-republic'),
                    ('MAYOTTE', 'mayotte'), ('AZERBAIJAN', 'azerbaijan'), ('ZAMBIA', 'zambia'),
                    ('BOTSWANA', 'botswana'), ('PORTUGAL', 'portugal'), ('BERMUDA', 'bermuda'), ('UGANDA', 'uganda'),
                    ('MICRONESIA', 'micronesia'), ('SENEGAL', 'senegal'), ('FRANCE', 'france'),
                    ('SOLOMON-ISLANDS', 'solomon-islands'), ('ANTARCTICA', 'antarctica'), ('MOZAMBIQUE', 'mozambique'),
                    ('EGYPT', 'egypt'), ('NEW-CALEDONIA', 'new-caledonia'), ('JERSEY', 'jersey'),
                    ('BANGLADESH', 'bangladesh'), ('RUSSIA', 'russia'), ('NEPAL', 'nepal'), ('HONG-KONG', 'hong-kong'),
                    ('NICARAGUA', 'nicaragua'), ('PAKISTAN', 'pakistan'), ('ECUADOR', 'ecuador'),
                    ('SAUDI-ARABIA', 'saudi-arabia'), ('UNITED-KINGDOM', 'united-kingdom'), ('TANZANIA', 'tanzania'),
                    ('MICRONESIA-', 'micronesia-'), ('KIRIBATI', 'kiribati'), ('ERITREA', 'eritrea'),
                    ('ANGUILLA', 'anguilla'), ('FRENCH-POLYNESIA', 'french-polynesia'), ('GIBRALTAR', 'gibraltar'),
                    ('TRINIDAD-AND-TOBAGO', 'trinidad-and-tobago'), ('GUINEA-BISSAU', 'guinea-bissau'),
                    ('LIBERIA', 'liberia'), ('VENEZUELA', 'venezuela'), ('PHILIPPINES', 'philippines'),
                    ('HONDURAS', 'honduras'), ('COSTA-RICA', 'costa-rica'), ('NAURU', 'nauru'), ('IRAN', 'iran'),
                    ('BHUTAN', 'bhutan'), ('TAJIKISTAN', 'tajikistan'), ('JAMAICA', 'jamaica'), ('CYPRUS', 'cyprus'),
                    ('TOGO', 'togo'), ('SYRIAN-ARAB-REPUBLIC', 'syrian-arab-republic'),
                    ('BOUVET-ISLAND', 'bouvet-island'), ('TOKELAU', 'tokelau'), ('VIETNAM', 'vietnam'),
                    ('SUDAN', 'sudan'), ('MACAU-SAR', 'macau-sar'), ('GAMBIA', 'gambia'), ('INDIA', 'india'),
                    ('CZECH-REPUBLIC', 'czech-republic'), ('CAYMAN-ISLANDS', 'cayman-islands'),
                    ('UNITED-ARAB-EMIRATES', 'united-arab-emirates'), ('MALAWI', 'malawi'), ('CROATIA', 'croatia'),
                    ('MAURITIUS', 'mauritius'), ('JORDAN', 'jordan'), ('LITHUANIA', 'lithuania'),
                    ('PUERTO-RICO', 'puerto-rico'), ('EQUATORIAL-GUINEA', 'equatorial-guinea'), ('MONACO', 'monaco'),
                    ('NIUE', 'niue'), ('SVALBARD', 'svalbard'), ('SAINT-KITTS-AND-NEVIS', 'saint-kitts-and-nevis'),
                    ('EAST-TIMOR', 'east-timor'), ('BRUNEI', 'brunei'), ('LATVIA', 'latvia'),
                    ('FRENCH-SOUTHERN-TERRITORIES', 'french-southern-territories'), ('PITCAIRN', 'pitcairn'),
                    ('UNITED-STATES-MINOR-OUTLYING-ISLANDS', 'united-states-minor-outlying-islands'),
                    ('TAIWAN', 'taiwan'), ('BENIN', 'benin'), ('GUADELOUPE', 'guadeloupe'),
                    ('MONTENEGRO', 'montenegro'), ('HAITI', 'haiti'), ('BULGARIA', 'bulgaria'), ('TUVALU', 'tuvalu'),
                    ('THAILAND', 'thailand'), ('ZIMBABWE', 'zimbabwe'), ('BELARUS', 'belarus'),
                    ('EL-SALVADOR', 'el-salvador'), ('UNITED-STATES', 'united-states'), ('GUYANA', 'guyana'),
                    ('SAINT-PIERRE-AND-MIQUELON', 'saint-pierre-and-miquelon'), ('SWEDEN', 'sweden'),
                    ('ANTIGUA-AND-BARBUDA', 'antigua-and-barbuda'), ('BRUNEI-DARUSSALAM', 'brunei-darussalam'),
                    ('ARGENTINA', 'argentina'), ('URUGUAY', 'uruguay'), ('SERBIA', 'serbia'), ('ICELAND', 'iceland'),
                    ('BRITISH-LNDIAN-OCEAN-TERRITORY', 'british-lndian-ocean-territory'), ('YEMEN', 'yemen'),
                    ('KUWAIT', 'kuwait'), ('AUSTRIA', 'austria'), ('RWANDA', 'rwanda'), ('SAMOA', 'samoa'),
                    ('TONGA', 'tonga'), ('TURKMENISTAN', 'turkmenistan'), ('MALTA', 'malta'), ('LAOS', 'laos'),
                    ('SAINT-VINCENT-AND-THE-GRENADINES', 'saint-vincent-and-the-grenadines'),
                    ('THE-BAHAMAS', 'the-bahamas'), ('TURKS-AND-CAICOS-ISLANDS', 'turks-and-caicos-islands'),
                    ('MADAGASCAR', 'madagascar'), ('GUERNSEY', 'guernsey'), ('SWAZILAND', 'swaziland'),
                    ('MONGOLIA', 'mongolia'), ('MOLDOVA', 'moldova'), ('BURKINA-FASO', 'burkina-faso'),
                    ('CHRISTMAS-ISLAND', 'christmas-island'), ('PITCAIRN-ISLANDS', 'pitcairn-islands'),
                    ('DOMINICA', 'dominica'), ('SIERRA-LEONE', 'sierra-leone'),
                    ('BOSNIA-AND-HERZEGOVINA', 'bosnia-and-herzegovina'), ('SLOVENIA', 'slovenia'),
                    ('SVALBARN-AND-JAN-MAYEN-ISLANDS', 'svalbarn-and-jan-mayen-islands'), ('GHANA', 'ghana'),
                    ('SEYCHELLES', 'seychelles'), ('INDONESIA', 'indonesia'),
                    ('SOUTH-GEORGIA-SOUTH-SANDWICH-ISLANDS', 'south-georgia-south-sandwich-islands'),
                    ('IRELAND', 'ireland'), ('CAMBODIA', 'cambodia'), ('VIRGIN-ISLANDS-', 'virgin-islands-'),
                    ('VIRGIN-ISLANDS', 'virgin-islands'),
                    ('DEMOCRATIC-REPUBLIC-OF-THE-CONGO', 'democratic-republic-of-the-congo'), ('HUNGARY', 'hungary'),
                    ('SOUTH-AFRICA', 'south-africa'), ('DOMINICAN-REPUBLIC', 'dominican-republic'),
                    ('TUNISIA', 'tunisia'), ('PANAMA', 'panama'), ('UKRAINE', 'ukraine'), ('GABON', 'gabon'),
                    ('DJIBOUTI', 'djibouti'), ('CAPE-VERDE', 'cape-verde'), ('PAPUA-NEW-GUINEA', 'papua-new-guinea'),
                    ('SOUTH-KOREA', 'south-korea'), ('SLOVAKIA', 'slovakia'), ('SRI-LANKA', 'sri-lanka'),
                    ('SAO-TOME-AND-PRINCIPE', 'sao-tome-and-principe'), ('ESTONIA', 'estonia'),
                    ('FALKLAND-ISLANDS', 'falkland-islands'), ('NIGERIA', 'nigeria'), ('ZAIRE', 'zaire'),
                    ('SWITZERLAND', 'switzerland'), ('SAINT-LUCIA', 'saint-lucia'), ('SURINAME', 'suriname'),
                    ('THE-GAMBIA', 'the%20gambia'), ('NORFOLK-ISLAND', 'norfolk%20island'),
                    ('HEARD-AND-MC-DONALD-ISLANDS', 'heard%20and%20mc%20donald%20islands'),
                    ('NORTH-KOREA', 'north%20korea'), ('LIBYAN-ARAB-JAMAHIRIYA', 'libyan%20arab%20jamahiriya'),
                    ('FRENCH-GUIANA', 'french%20guiana'), ('SAINT-HELENA', 'saint%20helena'),
                    ('AMERICAN-SAMOA', 'american%20samoa'), ('NEW-ZEALAND', 'new%20zealand'),
                    ('FAROE-ISLANDS', 'faroe%20islands'), ('BRITISH-VIRGIN-ISLANDS', 'british%20virgin%20islands'),
                    ('VATICAN-CITY-STATE', 'vatican%20city%20state'), ('COCOS-ISLANDS', 'cocos%20islands'),
                    ('WALLIS-AND-FUTUNA-ISLANDS', 'wallis%20and%20futuna%20islands'),
                    ('NORTHERN-MARIANA-ISLANDS', 'northern%20mariana%20islands'),
                    ('NORFORK-ISLAND', 'norfork%20island'), ('MARSHALL-ISLANDS', 'marshall%20islands'),
                    ('RUSSIAN-FEDERATION', 'russian%20federation'), ('COCOS--ISLANDS', 'cocos%20%20islands'),
                    ('NETHERLANDS-ANTILLES', 'netherlands%20antilles'), ('COOK-ISLANDS', 'cook%20islands'),
                    ('WESTERN-SAHARA', 'western%20sahara'), ('IVORY-COAST', 'ivory%20coast'),
                    ('CENTRAL-AFRICAN-REPUBLIC', 'central%20african%20republic'),
                    ('SOLOMON-ISLANDS', 'solomon%20islands'), ('HONG-KONG', 'hong%20kong'),
                    ('SAUDI-ARABIA', 'saudi%20arabia'), ('UNITED-KINGDOM', 'united%20kingdom'),
                    ('MICRONESIA-', 'micronesia%20'), ('FRENCH-POLYNESIA', 'french%20polynesia'),
                    ('TRINIDAD-AND-TOBAGO', 'trinidad%20and%20tobago'), ('GUINEA-BISSAU', 'guinea%20bissau'),
                    ('COSTA-RICA', 'costa%20rica'), ('SYRIAN-ARAB-REPUBLIC', 'syrian%20arab%20republic'),
                    ('BOUVET-ISLAND', 'bouvet%20island'), ('MACAU-SAR', 'macau%20sar'),
                    ('CZECH-REPUBLIC', 'czech%20republic'), ('CAYMAN-ISLANDS', 'cayman%20islands'),
                    ('UNITED-ARAB-EMIRATES', 'united%20arab%20emirates'), ('PUERTO-RICO', 'puerto%20rico'),
                    ('EQUATORIAL-GUINEA', 'equatorial%20guinea'),
                    ('SAINT-KITTS-AND-NEVIS', 'saint%20kitts%20and%20nevis'), ('EAST-TIMOR', 'east%20timor'),
                    ('FRENCH-SOUTHERN-TERRITORIES', 'french%20southern%20territories'),
                    ('UNITED-STATES-MINOR-OUTLYING-ISLANDS', 'united%20states%20minor%20outlying%20islands'),
                    ('EL-SALVADOR', 'el%20salvador'), ('UNITED-STATES', 'united%20states'),
                    ('SAINT-PIERRE-AND-MIQUELON', 'saint%20pierre%20and%20miquelon'),
                    ('ANTIGUA-AND-BARBUDA', 'antigua%20and%20barbuda'), ('BRUNEI-DARUSSALAM', 'brunei%20darussalam'),
                    ('BRITISH-LNDIAN-OCEAN-TERRITORY', 'british%20lndian%20ocean%20territory'),
                    ('SAINT-VINCENT-AND-THE-GRENADINES', 'saint%20vincent%20and%20the%20grenadines'),
                    ('THE-BAHAMAS', 'the%20bahamas'), ('TURKS-AND-CAICOS-ISLANDS', 'turks%20and%20caicos%20islands'),
                    ('BURKINA-FASO', 'burkina%20faso'), ('CHRISTMAS-ISLAND', 'christmas%20island'),
                    ('PITCAIRN-ISLANDS', 'pitcairn%20islands'), ('SIERRA-LEONE', 'sierra%20leone'),
                    ('BOSNIA-AND-HERZEGOVINA', 'bosnia%20and%20herzegovina'),
                    ('SVALBARN-AND-JAN-MAYEN-ISLANDS', 'svalbarn%20and%20jan%20mayen%20islands'),
                    ('SOUTH-GEORGIA-SOUTH-SANDWICH-ISLANDS', 'south%20georgia%20south%20sandwich%20islands'),
                    ('DEMOCRATIC-REPUBLIC-OF-THE-CONGO', 'democratic%20republic%20of%20the%20congo'),
                    ('SOUTH-AFRICA', 'south%20africa'), ('DOMINICAN-REPUBLIC', 'dominican%20republic'),
                    ('CAPE-VERDE', 'cape%20verde'), ('PAPUA-NEW-GUINEA', 'papua%20new%20guinea'),
                    ('SOUTH-KOREA', 'south%20korea'), ('SRI-LANKA', 'sri%20lanka'),
                    ('SAO-TOME-AND-PRINCIPE', 'sao%20tome%20and%20principe'),
                    ('FALKLAND-ISLANDS', 'falkland%20islands'), ('SAINT-LUCIA', 'saint%20lucia'),
                    ('VIRGIN-ISLANDS-', 'virgin%20islands%20'), ('VIRGIN-ISLANDS', 'virgin%20islands')]

    platform = models.ForeignKey(Platform, related_name='city_platform', on_delete=models.CASCADE,
                                 blank=True, null=True, default=None)
    city = models.CharField(max_length=100,
                            choices=CITY_CHOICES,
                            default="myanmar", blank=True, null=True)


class Review(Meta):
    author = models.CharField(max_length=200, blank=True)
    review = models.TextField()
    rating = models.CharField(max_length=3, blank=True)

    def __str__(self):
        return "%s %s" % (self.author, self.rating)


class Varient(Meta):
    name = models.CharField(max_length=200, blank=True)
    original_price = models.CharField(max_length=10, blank=False, default='0')
    discounted_price = models.CharField(max_length=10, blank=False, default='0')
    percent_discount = models.CharField(max_length=10, blank=False, default='0')
    currency = models.CharField(max_length=10, blank=False, default='USD')
    quantity = models.IntegerField(default=10, blank=False, null=True)

    def __str__(self):
        return "%s %s %s %s %s" % (
            self.name, self.currency, self.original_price, self.currency, self.discounted_price)


class Service(Meta):
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True, null=True)
    platform = models.ForeignKey(Platform, on_delete=models.SET_NULL, null=True, default=None)
    faqs = models.ManyToManyField(FAQ, blank=True, default=None)
    slug = models.CharField(max_length=350, blank=True, null=True)
    seo_title = models.TextField(blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    seo_keywords = models.TextField(blank=True, null=True)
    review = models.ForeignKey(Review, blank=True, null=True, on_delete=models.SET_NULL)
    varients = models.ManyToManyField(Varient)
    api_order_create = models.ForeignKey(VendorApi, related_name='api_order_create', on_delete=models.SET_NULL,
                                         blank=True, null=True, default=None)
    api_order_status = models.ForeignKey(VendorApi, related_name='api_order_status', on_delete=models.SET_NULL,
                                         blank=True, null=True, default=None)
    api_order_refill = models.ForeignKey(VendorApi, related_name='api_order_refill', on_delete=models.SET_NULL,
                                         blank=True, null=True, default=None)
    meta_message = models.TextField(max_length=250, blank=True, null=True)
    button_message = models.CharField(max_length=200, blank=True, null=True)
    real_users = models.BooleanField(default=True)
    needs_meta = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    content = RichTextField(blank=True, null=True)
    link_regex_validate = models.TextField(blank=True)
    link_placeholder = models.TextField(blank=True)

    def __str__(self):
        return "%s %s" % (self.platform, self.name)
