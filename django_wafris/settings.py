from django.conf import settings

wafris_settings = {
    "REDIS_URL": "redis://localhost:6379/0",
}

user_settings = getattr(settings, "WAFRIS", {})
wafris_settings.update(user_settings)
