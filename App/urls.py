from django.conf.urls import url

from App import views
from App.views import UserRegisterView, UserLoginView

urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^market/', views.market, name='market'),
    url(r'^marketwithparams/(?P<typeid>\d+)/(?P<cid>\d+)/(?P<sort_rule>\d+)/', views.marketWithParams,
        name='marketWithParams'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^mine/', views.mine, name='mine'),

    url(r'^addtocart/', views.add_to_cart, name='add_to_cart'),

    url(r'^userregister/', UserRegisterView.as_view(), name='userregister'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^checkuser/', views.check_user, name='check_user'),

    url(r'^userlogin/', UserLoginView.as_view(), name='user_login'),

    url(r'^active/', views.active, name='active'),
    url(r'^changecartstatus/', views.change_cart_status, name='change_cart_status'),
    url(r'^changecartliststatus/', views.change_cart_List_status, name='change_cart_List_status'),
    url(r'^subtocart/', views.sub_to_cart, name='sub_to_cart'),
    # url(r'^test/', views.test, name='test'),

]
