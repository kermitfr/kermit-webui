from django.conf import settings

SUB_APPS = (
        'oc4j',
        'weblogic',
        'bar',
)


# Admin Site Title
INSTALLED_PLATFORMS = getattr(settings, "INSTALLED_PLATFORMS", SUB_APPS)