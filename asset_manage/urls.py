"""itdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from . import views


app_name = 'asset_manage'
urlpatterns = [
    url(r'^asset_manage/id/(?P<asset_id>(.+))/$', views.Asset_manage_json.as_view()),       #根据asset_id查询该条资产详情接口
    url(r'^asset_info/asset/search/$', views.Asset_info_json.as_view()),                    #资产出入库页面查询接口
    url(r'^asset_info/user/(?P<username>(.+))/$', views.User_info_json.as_view()),          #查询用户信息接口
    url(r'^operation_logs/id/(?P<asset_id>(.+))/$', views.Operation_Logs_json.as_view()),   #资产操作记录信息查询接口
    url(r'^export/asset/(?P<owner>(.+))/$', views.ExportAsset.as_view() ),                       #资产导出excel文件接口
    url(r'^export/download_template/(?P<file_name>(.+))', views.Download_template.as_view(),name="download_template"),
]
