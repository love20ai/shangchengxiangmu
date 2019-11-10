from django.conf.urls import url

from . import views

urlpatterns = [

    # 1.列表页
    url(r'^list/(?P<category_id>\d+)/(?P<page_num>\d+)/$', views.ListView.as_view(), name='list'),
    # 2.热销商品 hot/(?P<category_id>\d+)/
    url(r'^hot/(?P<category_id>\d+)/$', views.HotView.as_view()),

    # 3.详情页  detail/(?P<sku_id>\d+)/
    url(r'^detail/(?P<sku_id>\d+)/$', views.DetailView.as_view(),name="detail"),

    # 4.商品分类 访问量
    url(r'^detail/visit/(?P<category_id>\d+)/$', views.VisitCountView.as_view(), name="visit"),


]
