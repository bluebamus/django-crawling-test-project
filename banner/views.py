from django.shortcuts import render
from django.views.generic import TemplateView
from .models import BannerIndex, BannerBanner

# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get(self, request, *args, **kwargs):
        client_ip = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        is_bot = 'bot' in user_agent.lower()
        
        # 세션이 없는 경우 생성
        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key
            
        banner_index = BannerIndex.objects.create(
            ip=client_ip,
            session_id=session_id,
            user_agent=user_agent,
            is_bot=is_bot
        )
        print("banner_index.id: ",banner_index.id)
        request.session['banner_index_id'] = banner_index.id
        return super().get(request, *args, **kwargs)

class BannerView(TemplateView):
    template_name = 'banner.html'
    
    def get(self, request, *args, **kwargs):
        client_ip = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        is_bot = 'bot' in user_agent.lower()
        clicked_image = request.GET.get('image', '')
        print("request.session.session_key : ",request.session.session_key)
        session_id = request.session.session_key
        banner_id = request.session.get('banner_index_id')
        
        BannerBanner.objects.create(
            banner_index_id=banner_id,
            ip=client_ip,
            session_id=session_id,
            user_agent=user_agent,
            is_bot=is_bot,
            clicked_image=clicked_image
        )
        
        return super().get(request, *args, **kwargs)
