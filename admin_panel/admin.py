from django.contrib import admin

from .models import *

# 
admin.site.register(customar)
admin.site.register(customar_ditail)
admin.site.register(owed_detail)
admin.site.register(total_cost)