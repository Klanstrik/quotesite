from django.contrib import admin
from .models import Source, Quote, Vote

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("name",)   # только name
    search_fields = ("name",)

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("short_text", "source", "author", "weight", "is_active", "likes", "dislikes", "views", "created_at")
    list_filter = ("is_active", "source",)   # без source__kind
    search_fields = ("text", "author", "source__name")
    autocomplete_fields = ("source",)
    ordering = ("-created_at",)

    @admin.display(description="Текст")
    def short_text(self, obj):
        return (obj.text[:60] + "…") if len(obj.text) > 60 else obj.text

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("quote", "session_key", "value", "created_at")
    search_fields = ("session_key", "quote__text")
