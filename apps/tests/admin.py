from django.db import models
from django.forms import Textarea
from django.contrib import admin

from apps.tests.models import Test, TestCase

class TestCaseAdmin(admin.TabularInline):
    model = TestCase
    formfield_overrides = { models.TextField: {'widget': Textarea(attrs={'rows': 1,'cols': 18})}, }
    extra = 1

class TestAdmin(admin.ModelAdmin):
    inlines = [TestCaseAdmin]

admin.site.register(Test, TestAdmin)
