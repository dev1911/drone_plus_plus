from django.urls import path,include
from accounts.views import registration_view
from rest_framework.authtoken.views import obtain_auth_token
from .views import logout_view
from .views import user_id
from .views import disable_user
from .views import Login_view
app_name = "accounts"

urlpatterns=[
	path('register/',registration_view,name='register'),
	path('login/',Login_view.as_view(),name="login"),
	path('logout/',logout_view,name="logout"),
	path('user_id/',user_id,name="user_id"),
	path('disable_user/',disable_user,name="disable_user")
]

