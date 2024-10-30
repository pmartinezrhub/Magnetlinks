#!/usr/bin/env python
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "magnetlinks.settings")  
django.setup()

from magnetlinks.tasks import update_magnetlinks  

update_magnetlinks.delay() 
