from django.contrib import admin
from .models import Employee, Job, Candidate, Feedback, Field, JD, RequisitionCandidate

# Register your models here.
admin.site.register(Employee)
admin.site.register(Job)
admin.site.register(Candidate)
admin.site.register(Feedback)
admin.site.register(Field)
admin.site.register(JD)
admin.site.register(RequisitionCandidate)
