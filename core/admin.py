from django.contrib import admin

from core.models import DocumentType, LostPassport

admin.site.register(DocumentType)
admin.site.register(LostPassport)
