from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'one.view.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/userinfo/', 'portal.view.userView.user_info'),
    url(r'^api/insertuser/', 'portal.view.userView.insert_user'),
    url(r'^api/login/','portal.view.userView.login'),
    url(r'^api/logout/','portal.view.userView.logout'),
]
