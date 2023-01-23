from django.contrib import admin
from .models import Endpoint, Request
# Register your models here.

@admin.register(Endpoint)
class EndpointAdmin(admin.ModelAdmin):

    list_display = ['endpoint', 'threshold', 'fail_times']
    list_editable = ['threshold',]

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):

    list_display = ['get_endpoint', 'created_at', 'result']

