from django.contrib import admin

from .models import Mannschaften, Laender, Paarungen, Tipper, Tipps, Gruppen

admin.site.register(Mannschaften)
admin.site.register(Laender)
admin.site.register(Paarungen)
admin.site.register(Tipper)
admin.site.register(Tipps)
admin.site.register(Gruppen)
