from django.shortcuts import render
from django.views.generic import TemplateView
from .models import BannerIndex, BannerBanner
import logging

# 로깅 설정
logger = logging.getLogger(__name__)

# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get(self, request, *args, **kwargs):
        # 클라이언트 정보 로깅
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        logger.info("Client IP: %s", client_ip)
        logger.info("User Agent: %s", user_agent)
        logger.info("REMOTE_ADDR: %s", request.META.get('REMOTE_ADDR'))
        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(',')[0].strip()
        else:
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
        logger.info("banner_index.id: %s", banner_index.id)
        request.session['banner_index_id'] = banner_index.id
        return super().get(request, *args, **kwargs)

class BannerView(TemplateView):
    template_name = 'banner.html'
    
    def get(self, request, *args, **kwargs):
        # 클라이언트 정보 로깅
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        logger.info("Client IP: %s", client_ip)
        logger.info("User Agent: %s", user_agent)
        logger.info("REMOTE_ADDR: %s", request.META.get('REMOTE_ADDR'))
        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(',')[0].strip()
        else:
            client_ip = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        is_bot = 'bot' in user_agent.lower()
        clicked_image = request.GET.get('image', '')
        logger.info("request.session.session_key: %s", request.session.session_key)
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
