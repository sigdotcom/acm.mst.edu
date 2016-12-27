# ACM\_General App Breakdown

## Table of contents
+ ACM\_General
  - [settings.py](ACM_General/settings.py)
  - [urls.py](ACM_General/urls.py)
  - [wsgi.py](ACM_General/wsgi.py)
+ accounts
  - [forms/](accounts/forms/)
  - [templates/](accounts/templates/)
  - [admin.py](accounts/admin.py)
  - [apps.py](accounts/apps.py)
  - [backends.py](accounts/backends.py)
  - [models.py](accounts/models.py)
  - [tests.py](accounts/tests.py)
  - [urls.py](accounts/urls.py)
  - [views.py](accounts/views.py)
+ core
  - [static/core/css](core/static/core/css/)
    + [baseStyle.css](core/static/core/css/baseStyle.css)
  - [templates/](core/templates/)
  - [admin.py](core/admin.py)
  - [apps.py](core/apps.py)
  - [models.py](core/models.py)
  - [tests.py](core/tests.py)
  - [views.py](core/views.py)
+ events
  - [templates/](events/templates/)
  - [admin.py](events/admin.py)
  - [apps.py](events/apps.py)
  - [forms.py](events/forms.py)
  - [models.py](events/models.py)
  - [tests.py](events/tests.py)
  - [urls.py](events/urls.py)
  - [views.py](events/views.py)
+ home
  - [admin.py](home/admin.py)
  - [apps.py](home/apps.py)
  - [models.py](home/models.py)
  - [tests.py](home/tests.py)
  - [urls.py](home/urls.py)
  - [views.py](home/views.py)

## Before Production
1. Comment every file which needs commenting
2. Document each template as what variables they expect/need
