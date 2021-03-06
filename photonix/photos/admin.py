from django.contrib import admin

from .models import Camera, Lens, Photo, PhotoFile, Tag, PhotoTag


class CameraAdmin(admin.ModelAdmin):
    pass


class LensAdmin(admin.ModelAdmin):
    pass


class PhotoAdmin(admin.ModelAdmin):
    pass


class PhotoFileAdmin(admin.ModelAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    pass


class PhotoTagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Camera, CameraAdmin)
admin.site.register(Lens, LensAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoFile, PhotoFileAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(PhotoTag, PhotoTagAdmin)
