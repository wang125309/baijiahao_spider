from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'one.view.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^sys/spider_baijiahao/','backend.views.spider_baijiahao'),
    url(r'^sys/spider_toutiao/','backend.views.spider_toutiao'),
    url(r'^sys/spider_kuaibao/','backend.views.spider_kuaibao'),
    url(r'^sys/spider_bilibili/','backend.views.spider_bilibili'),
    url(r'^sys/spider_youku/','backend.views.spider_youku'),
    url(r'^sys/login/','backend.views.login'),
    url(r'^sys/get_types/','backend.views.get_types'),
    url(r'^sys/new_type/','backend.views.new_type'),
    url(r'^sys/delete_type/','backend.views.delete_type'),
    url(r'^sys/upload_data_resource/','backend.views.upload_data_resource'),
    url(r'^sys/get_data/','backend.views.get_data'),
    url(r'^sys/spider/','backend.views.spider'),
    url(r'^sys/change_weight/','backend.views.change_weight'),
    url(r'^sys/delete_user/','backend.views.delete_user'),
    url(r'^sys/get_total/','backend.views.get_total'),
    url(r'^sys/download_data_resource/','backend.views.download_data_resource'),

]
