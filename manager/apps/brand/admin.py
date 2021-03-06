from django.contrib import admin
from django.db import models
from .models import Brand, BrandOwner, BrandType, BrandProposal
from .widget import AdminImageWidget


class BrandTypeAdmin(admin.ModelAdmin):
    actions = None

    # Never delete a brand, update its BSIN
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(BrandType, BrandTypeAdmin)


class BrandOwnerAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('owner_nm', 'owner_logo_admin', 'owner_link')
    fields = (
        'owner_nm', 'owner_link', 'owner_wiki_en', 'owner_logo')
    search_fields = ['owner_nm']

    # Never delete a brand, update its BSIN
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(BrandOwner, BrandOwnerAdmin)


class BrandAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('bsin', 'brand_nm', 'brand_logo_admin', 'flag_delete')
    fields_add = (
        (None, {
            'classes': ('wide',),
            'fields': ('bsin', 'brand_nm', 'owner_cd', 'brand_type_cd',
                       'brand_link', 'brand_logo', 'comments', 'last_modified')
        }),
    )
    fields_change = (
        (None, {
            'classes': ('wide',),
            'fields': ('bsin', 'brand_nm', 'owner_cd', 'brand_type_cd',
                       'brand_link', 'brand_logo',
                       ('flag_delete', 'comments'),
                       'last_modified')
        }),
    )
    readonly_fields_su = ('bsin', 'last_modified')
    readonly_fields_moderator = ('bsin', 'last_modified', 'brand_nm')
    search_fields = ['bsin', 'brand_nm', 'owner_cd__owner_nm']
    list_filter = ('flag_delete', )
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget},
    }

    # Never delete a brand, update its BSIN
    def has_delete_permission(self, request, obj=None):
        return False

    def get_fieldsets(self, request, obj=None):
        # if editing
        if obj:
            return self.fields_change
        return self.fields_add

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields_su
        return self.readonly_fields_moderator

admin.site.register(Brand, BrandAdmin)
admin.site.register(BrandProposal)
