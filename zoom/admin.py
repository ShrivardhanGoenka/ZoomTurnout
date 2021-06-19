from django.contrib import admin
from zoom.models import StoreData,AuthIds,Files,CurrentMeetinglog,ReportLog,Metrics
# Register your models here.
admin.site.register(StoreData)
admin.site.register(AuthIds)
admin.site.register(Files)
admin.site.register(CurrentMeetinglog)
admin.site.register(ReportLog)
admin.site.register(Metrics)
