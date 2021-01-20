from django.contrib import admin
from .models import *

admin.site.register(Employee)
admin.site.register(MobileNumber)
admin.site.register(Customer)
admin.site.register(Handsets)
admin.site.register(HandsetTariffs)
admin.site.register(SimOnlyTariffs)
admin.site.register(SimOnlyOrder)
admin.site.register(SpendCaps)
admin.site.register(Insurance)
admin.site.register(HandsetOrder)
admin.site.register(HandsetStock)
