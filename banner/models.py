from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.html import format_html

class BannerIndex(models.Model):
    ip = models.GenericIPAddressField()
    session_id = models.CharField(max_length=100)
    user_agent = models.TextField()
    is_bot = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.ip}"
    
    class Meta:
        verbose_name = "배너 인덱스"
        verbose_name_plural = "배너 인덱스 목록"

class BannerBanner(models.Model):
    banner_index = models.ForeignKey(
        BannerIndex, 
        on_delete=models.CASCADE,
        verbose_name="배너 인덱스"
    )
    ip = models.GenericIPAddressField()
    session_id = models.CharField(blank=True,null=True,max_length=100)
    user_agent = models.TextField()
    is_bot = models.BooleanField(default=False)
    clicked_image = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.ip}"
        
    @property
    def banner_index_link(self):
        url = reverse('admin:banner_bannerindex_change', args=[self.banner_index.id])
        return format_html('<a href="{}">{}</a>', url, self.banner_index.ip)
    banner_index_link.fget.short_description = '배너 인덱스'
    
    class Meta:
        verbose_name = "배너 클릭"
        verbose_name_plural = "배너 클릭 목록"
