"""Site configuration and strings for tools/build_site.py.

strings_existing.json holds the translations extracted verbatim from the former
single-page index.html. NEW_STRINGS adds the SEO copy (titles, descriptions,
H1s, subpage texts); FIXES corrects a few existing strings. Only facts that
already appear on the site are used (plus the room count of 14).
"""
import json
from pathlib import Path

BASE_URL = "https://nakas-hotel.com"
BOOKING_URL = "https://nakas.rezervasyonal.com/"
ETSTUR_URL = "https://www.etstur.com/Nakas-Hotel"
PHONE = "+905307046893"
PHONE_DISPLAY = "+90 530 704 68 93"
EMAIL = "info@nakashotel.com"
WHATSAPP_URL = "https://wa.me/905307046893"
INSTAGRAM_URL = "https://www.instagram.com/nakas.hotel/"
FACEBOOK_URL = "https://www.facebook.com/profile.php?id=61575999142790"
BOOKING_COM_URL = "https://www.booking.com/hotel/tr/nakas.tr.html"
STREET = "Tuzla, 531. Sk. No:6"
POSTAL_CODE = "48300"
CITY = "Fethiye"
REGION = "Muğla"
LAT, LNG = 36.629224, 29.118286
NUMBER_OF_ROOMS = 14
MAPS_DIRECTIONS_URL = f"https://www.google.com/maps/dir/?api=1&destination={LAT},{LNG}"
LASTMOD = "2026-11-27"

# Turkish is served at the site root and is also the x-default.
DEFAULT_LANG = "tr"
LANGS = ["tr", "en", "de", "ru", "zh"]
LANG_META = {
    "tr": {"html": "tr", "hreflang": "tr", "og": "tr_TR", "label": "TR", "maps_hl": "tr"},
    "en": {"html": "en", "hreflang": "en", "og": "en_GB", "label": "EN", "maps_hl": "en"},
    "de": {"html": "de", "hreflang": "de", "og": "de_DE", "label": "DE", "maps_hl": "de"},
    "ru": {"html": "ru", "hreflang": "ru", "og": "ru_RU", "label": "RU", "maps_hl": "ru"},
    "zh": {"html": "zh-Hans", "hreflang": "zh-Hans", "og": "zh_CN", "label": "中文", "maps_hl": "zh-CN"},
}

PAGE_SLUGS = {
    "home": {"tr": "", "en": "", "de": "", "ru": "", "zh": ""},
    "rooms": {"tr": "odalar/", "en": "rooms/", "de": "zimmer/", "ru": "rooms/", "zh": "rooms/"},
    "location": {"tr": "konum/", "en": "location/", "de": "lage/", "ru": "location/", "zh": "location/"},
}


def lang_prefix(lang):
    return "/" if lang == DEFAULT_LANG else f"/{lang}/"


def page_path(page, lang):
    return lang_prefix(lang) + PAGE_SLUGS[page][lang]


FIXES = {
    # "Kirala" means "rent"; hotel rooms are reserved ("rezervasyon").
    "tr": {"book_now": "Rezervasyon", "rooms_all": "Rezervasyon Yap"},
    # "Book all rooms" read as booking every room at once.
    "en": {"rooms_all": "Book a Room"},
    "de": {"rooms_all": "Zimmer buchen"},
    "zh": {"rooms_all": "预订客房"},
}

NEW_STRINGS = {
    "tr": {
        "title_home": "Nakas Hotel | Fethiye Merkezde Denize Yakın Butik Otel",
        "desc_home": "Fethiye merkezde, Tuzla'da denize 100 m mesafede modern butik otel. Penthouse, Standart ve Bahçeli odalar, ücretsiz Wi-Fi, 24 saat hizmet. Direkt rezervasyonla en iyi fiyat.",
        "badge": "Nakas Hotel · Fethiye, Türkiye",
        "h1_home": "Fethiye merkezde<br><em>denize yakın butik otel</em>",
        "title_rooms": "Odalar – Penthouse, Standart ve Bahçeli Oda | Nakas Hotel Fethiye",
        "desc_rooms": "Nakas Hotel'in 14 odası: 37 m² balkonlu Penthouse Oda, Standart Oda ve özel bahçeli Bahçeli Oda. Tüm odalar klimalı, ücretsiz Wi-Fi. Fethiye merkezde, denize 100 m.",
        "h1_rooms": "Fethiye'de <em>butik otel odaları</em>",
        "title_location": "Konum ve Ulaşım – Fethiye Merkez, Denize 100 m | Nakas Hotel",
        "desc_location": "Nakas Hotel, Fethiye merkezde Tuzla, 531. Sk. No:6 adresinde: denize 100 m, Dalaman Havalimanı'na yaklaşık 45 dakika. Harita, yol tarifi ve VIP transfer.",
        "h1_location": "Fethiye'nin kalbinde,<br><em>denize 100 metre</em>",
        "nav_location": "Konum",
        "room1_name": "Penthouse Oda", "room2_name": "Standart Oda", "room3_name": "Bahçeli Oda",
        "rooms_count": "14 oda · 3 oda tipi",
        "rooms_more": "Tüm odaları inceleyin",
        "loc_more": "Konum ve ulaşım bilgileri",
        "in_all_rooms": "Tüm odalarda",
        "directions": "Yol tarifi al",
        "ct_whatsapp": "WhatsApp'tan yazın",
        "address": "Adres",
        "explore": "Fethiye'yi keşfedin",
        "crumb_home": "Ana Sayfa",
        "privacy": "Gizlilik Politikası",
        "lang_label": "Dil seçimi",
        "gallery_open": "Fotoğrafı büyüt",
        "alt_exterior": "Nakas Hotel dış görünüm, Fethiye",
        "alt_bay": "Fethiye Körfezi ve şehir manzarası",
        "alt_room_sofa": "Çift kişilik yatak ve kanepeli oda",
        "alt_bed": "Çift kişilik yatak",
        "alt_balcony": "Balkondan dağ manzarası",
        "alt_room": "Oda iç görünüm",
        "alt_bathroom": "Banyo",
        "alt_garden": "Bahçeli Oda, özel bahçe",
        "alt_washbasin": "Banyo lavabo detayı",
        "alt_bath": "Lavabolu banyo",
        "alt_oludeniz": "Ölüdeniz, Fethiye",
    },
    "en": {
        "title_home": "Nakas Hotel | Boutique Hotel in Central Fethiye, Near the Sea",
        "desc_home": "Modern boutique hotel in central Fethiye, 100 m from the sea on Tuzla Street. Penthouse, Standard and Garden rooms, free Wi-Fi, 24h service. Book direct for the best price.",
        "badge": "Nakas Hotel · Fethiye, Turkey",
        "h1_home": "Boutique hotel in central Fethiye,<br><em>100 m from the sea</em>",
        "title_rooms": "Rooms – Penthouse, Standard & Garden Room | Nakas Hotel Fethiye",
        "desc_rooms": "Nakas Hotel's 14 rooms: the 37 m² Penthouse with private balcony, the Standard Room and the Garden Room with private garden. All rooms air-conditioned, free Wi-Fi.",
        "h1_rooms": "Rooms at our <em>Fethiye boutique hotel</em>",
        "title_location": "Location – Central Fethiye, 100 m to the Sea | Nakas Hotel",
        "desc_location": "Nakas Hotel is on Tuzla Street in central Fethiye (531. Sk. No:6), 100 m from the sea and approx. 45 min from Dalaman Airport. Map, directions and VIP transfer.",
        "h1_location": "In the heart of Fethiye,<br><em>100 m from the sea</em>",
        "nav_location": "Location",
        "room1_name": "Penthouse Room", "room2_name": "Standard Room", "room3_name": "Garden Room",
        "rooms_count": "14 rooms · 3 room types",
        "rooms_more": "View all rooms",
        "loc_more": "Location & directions",
        "in_all_rooms": "In every room",
        "directions": "Get directions",
        "ct_whatsapp": "Message us on WhatsApp",
        "address": "Address",
        "explore": "Explore Fethiye",
        "crumb_home": "Home",
        "privacy": "Privacy Policy",
        "lang_label": "Language",
        "gallery_open": "Enlarge photo",
        "alt_exterior": "Nakas Hotel exterior, Fethiye",
        "alt_bay": "Fethiye Bay and town from above",
        "alt_room_sofa": "Room with double bed and sofa",
        "alt_bed": "Double bed",
        "alt_balcony": "Balcony with mountain view",
        "alt_room": "Room interior",
        "alt_bathroom": "Bathroom",
        "alt_garden": "Garden Room with private garden",
        "alt_washbasin": "Bathroom washbasin detail",
        "alt_bath": "Bathroom with washbasin",
        "alt_oludeniz": "Ölüdeniz near Fethiye",
    },
    "de": {
        "title_home": "Nakas Hotel | Boutique-Hotel in Fethiye, 100 m vom Meer",
        "desc_home": "Modernes Boutique-Hotel im Zentrum von Fethiye an der Tuzla-Straße, 100 m vom Meer. Penthouse, Standard- und Gartenzimmer, kostenloses WLAN, 24h-Service. Direkt zum besten Preis buchen.",
        "badge": "Nakas Hotel · Fethiye, Türkei",
        "h1_home": "Boutique-Hotel im Zentrum von Fethiye,<br><em>100 m vom Meer</em>",
        "title_rooms": "Zimmer – Penthouse, Standard- & Gartenzimmer | Nakas Hotel Fethiye",
        "desc_rooms": "Die 14 Zimmer des Nakas Hotel: Penthouse mit 37 m² und privatem Balkon, Standardzimmer und Gartenzimmer mit Privatgarten. Alle Zimmer klimatisiert, kostenloses WLAN.",
        "h1_rooms": "Zimmer im <em>Boutique-Hotel</em> in Fethiye",
        "title_location": "Lage & Anreise – Zentrum Fethiye, 100 m zum Meer | Nakas Hotel",
        "desc_location": "Das Nakas Hotel liegt an der Tuzla-Straße im Zentrum von Fethiye (531. Sk. No:6), 100 m vom Meer, ca. 45 Min. vom Flughafen Dalaman. Karte, Route und VIP-Transfer.",
        "h1_location": "Im Herzen von Fethiye,<br><em>100 m vom Meer</em>",
        "nav_location": "Lage",
        "room1_name": "Penthouse-Zimmer", "room2_name": "Standardzimmer", "room3_name": "Gartenzimmer",
        "rooms_count": "14 Zimmer · 3 Zimmertypen",
        "rooms_more": "Alle Zimmer ansehen",
        "loc_more": "Lage & Anreise",
        "in_all_rooms": "In allen Zimmern",
        "directions": "Route planen",
        "ct_whatsapp": "Per WhatsApp schreiben",
        "address": "Adresse",
        "explore": "Fethiye entdecken",
        "crumb_home": "Startseite",
        "privacy": "Datenschutzerklärung",
        "lang_label": "Sprache",
        "gallery_open": "Foto vergrößern",
        "alt_exterior": "Nakas Hotel Außenansicht, Fethiye",
        "alt_bay": "Fethiye-Bucht und Stadt von oben",
        "alt_room_sofa": "Zimmer mit Doppelbett und Sofa",
        "alt_bed": "Doppelbett",
        "alt_balcony": "Balkon mit Bergblick",
        "alt_room": "Zimmeransicht",
        "alt_bathroom": "Badezimmer",
        "alt_garden": "Gartenzimmer mit Privatgarten",
        "alt_washbasin": "Waschbecken im Bad",
        "alt_bath": "Bad mit Waschtisch",
        "alt_oludeniz": "Ölüdeniz bei Fethiye",
    },
    "ru": {
        "title_home": "Nakas Hotel | Бутик-отель в центре Фетхие, 100 м от моря",
        "desc_home": "Современный бутик-отель в центре Фетхие на улице Тузла, в 100 м от моря. Пентхаус, стандартные номера и номер с садом, бесплатный Wi-Fi, круглосуточный сервис. Бронируйте напрямую.",
        "badge": "Nakas Hotel · Фетхие, Турция",
        "h1_home": "Бутик-отель в центре Фетхие,<br><em>в 100 м от моря</em>",
        "title_rooms": "Номера – пентхаус, стандарт и номер с садом | Nakas Hotel Фетхие",
        "desc_rooms": "14 номеров Nakas Hotel: пентхаус 37 м² с частным балконом, стандартный номер и номер с частным садом. Кондиционер в каждом номере, бесплатный Wi-Fi.",
        "h1_rooms": "Номера <em>бутик-отеля</em> в Фетхие",
        "title_location": "Расположение – центр Фетхие, 100 м до моря | Nakas Hotel",
        "desc_location": "Nakas Hotel находится на улице Тузла в центре Фетхие (531. Sk. No:6), в 100 м от моря и примерно в 45 мин. от аэропорта Даламан. Карта, маршрут и VIP трансфер.",
        "h1_location": "В самом сердце Фетхие,<br><em>в 100 м от моря</em>",
        "nav_location": "Расположение",
        "room1_name": "Пентхаус", "room2_name": "Стандартный номер", "room3_name": "Номер с садом",
        "rooms_count": "14 номеров · 3 типа номеров",
        "rooms_more": "Подробнее о номерах",
        "loc_more": "Как добраться",
        "in_all_rooms": "Во всех номерах",
        "directions": "Построить маршрут",
        "ct_whatsapp": "Написать в WhatsApp",
        "address": "Адрес",
        "explore": "Откройте Фетхие",
        "crumb_home": "Главная",
        "privacy": "Политика конфиденциальности",
        "lang_label": "Язык",
        "gallery_open": "Увеличить фото",
        "alt_exterior": "Nakas Hotel, вид снаружи, Фетхие",
        "alt_bay": "Залив Фетхие и город с высоты",
        "alt_room_sofa": "Номер с двуспальной кроватью и диваном",
        "alt_bed": "Двуспальная кровать",
        "alt_balcony": "Балкон с видом на горы",
        "alt_room": "Интерьер номера",
        "alt_bathroom": "Ванная комната",
        "alt_garden": "Номер с частным садом",
        "alt_washbasin": "Раковина в ванной",
        "alt_bath": "Ванная с раковиной",
        "alt_oludeniz": "Олюдениз недалеко от Фетхие",
    },
    "zh": {
        "title_home": "Nakas 酒店 | 费特希耶市中心精品酒店，距海边100米",
        "desc_home": "位于费特希耶市中心图兹拉街的现代精品酒店，距海边仅100米。提供顶层套房、标准客房和花园客房，免费Wi-Fi，24小时服务。直接预订享最优价格。",
        "badge": "Nakas 酒店 · 土耳其费特希耶",
        "h1_home": "费特希耶市中心精品酒店<br><em>距海边100米</em>",
        "title_rooms": "客房 – 顶层套房、标准客房与花园客房 | Nakas 酒店 费特希耶",
        "desc_rooms": "Nakas 酒店共有14间客房：37平方米带私人阳台的顶层套房、标准客房以及带私家花园的花园客房。全室空调，免费Wi-Fi。",
        "h1_rooms": "费特希耶<em>精品酒店客房</em>",
        "title_location": "位置与交通 – 费特希耶市中心，距海边100米 | Nakas 酒店",
        "desc_location": "Nakas 酒店位于费特希耶市中心图兹拉街（531. Sk. No:6），距海边100米，距达拉曼机场约45分钟。地图、路线与VIP接送信息。",
        "h1_location": "费特希耶中心地带<br><em>距海边100米</em>",
        "nav_location": "位置",
        "room1_name": "顶层套房", "room2_name": "标准客房", "room3_name": "花园客房",
        "rooms_count": "14间客房 · 3种房型",
        "rooms_more": "查看全部客房",
        "loc_more": "交通与位置详情",
        "in_all_rooms": "所有客房均配备",
        "directions": "获取路线",
        "ct_whatsapp": "通过 WhatsApp 联系",
        "address": "地址",
        "explore": "探索费特希耶",
        "crumb_home": "首页",
        "privacy": "隐私政策",
        "lang_label": "语言",
        "gallery_open": "放大照片",
        "alt_exterior": "Nakas 酒店外观，费特希耶",
        "alt_bay": "费特希耶湾与城市鸟瞰",
        "alt_room_sofa": "配有双人床和沙发的客房",
        "alt_bed": "双人床",
        "alt_balcony": "山景阳台",
        "alt_room": "客房内景",
        "alt_bathroom": "浴室",
        "alt_garden": "带私家花园的花园客房",
        "alt_washbasin": "浴室洗手台细节",
        "alt_bath": "带洗手台的浴室",
        "alt_oludeniz": "费特希耶附近的厄吕代尼兹",
    },
}


def load_strings():
    existing = json.loads((Path(__file__).parent / "strings_existing.json").read_text())
    strings = {}
    for lang in LANGS:
        s = dict(existing[lang])
        s.update(FIXES.get(lang, {}))
        overlap = set(NEW_STRINGS[lang]) & set(s)
        assert not overlap, f"{lang}: new strings shadow existing keys {overlap}"
        s.update(NEW_STRINGS[lang])
        strings[lang] = s
    keys = set(strings[DEFAULT_LANG])
    for lang in LANGS:
        assert set(strings[lang]) == keys, f"{lang}: key mismatch {keys ^ set(strings[lang])}"
    return strings
