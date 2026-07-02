import json
import os

class I18n:
    def __init__(self, default_locale="en"):
        self.default_locale = default_locale
        self.translations = {}
        self.load_translations()

    def load_translations(self):
        locales_dir = "locales"
        if not os.path.exists(locales_dir):
            return
        
        for filename in os.listdir(locales_dir):
            if filename.endswith(".json"):
                locale = filename[:-5]
                with open(os.path.join(locales_dir, filename), "r", encoding="utf-8") as f:
                    self.translations[locale] = json.load(f)

    def get(self, key, locale=None, **kwargs):
        if locale is None:
            locale = self.default_locale
        text = self.translations.get(locale, {}).get(key, self.translations.get(self.default_locale, {}).get(key, key))
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text

i18n = I18n()
_ = i18n.get
