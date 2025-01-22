from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import BannerIndex, BannerBanner

@admin.register(BannerIndex)
class BannerIndexAdmin(admin.ModelAdmin):
    list_display = ['ip', 'session_id', 'is_bot', 'created_at']
    list_filter = ['is_bot', 'created_at']
    search_fields = ['ip', 'session_id']

@admin.register(BannerBanner)
class BannerBannerAdmin(admin.ModelAdmin):
    list_display = ['ip', 'get_banner_index_link', 'session_id', 'clicked_image', 'is_bot', 'created_at']
    list_filter = ['is_bot', 'created_at']
    search_fields = ['ip', 'session_id', 'clicked_image']
    readonly_fields = ['banner_index_link']
    fields = ['banner_index_link', 'banner_index', 'ip', 'session_id', 'user_agent', 'clicked_image', 'is_bot', 'created_at']
    
    def get_banner_index_link(self, obj):
        if obj and obj.banner_index:
            url = reverse('admin:banner_bannerindex_change', args=[obj.banner_index.id])
            return format_html('<a href="{}">{}</a>', url, obj.banner_index.ip)
        return "-"
    get_banner_index_link.short_description = '배너 인덱스'
