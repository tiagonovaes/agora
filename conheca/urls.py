# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'conheca'
urlpatterns = [
  url(r'pdpu/conheca/$', views.TemplatePDPUConhecaView.as_view(template_name="conheca/pdpu-conheca.html"), name='pdpu-conheca'),
  url(r'^pdpu/conheca/artigos/(?P<pk>[0-9]+)/$', views.ArticlePageView.as_view(), name='article_page'),
]
