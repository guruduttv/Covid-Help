
# Register your models here.
from django.contrib import admin
from .models import Hospitals,Hospital_phones,District,Totalcases,State_wise,Self_assess,Locations,At_Risk

admin.site.register(Hospitals)
admin.site.register(District)
admin.site.register(Hospital_phones)
admin.site.register(Totalcases)
admin.site.register(State_wise)
admin.site.register(Self_assess)
admin.site.register(At_Risk)
admin.site.register(Locations)


# Register your models here.
