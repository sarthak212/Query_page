from django.urls import path
from cloneapp import views
from django.conf import settings
from django.conf.urls.static import static

app_name='cloneapp'


urlpatterns=[
        path('',views.firstpage,name='firstpage'),
        path('list/',views.frontpage.as_view(),name='question_list'),
        path('detail/<int:pk>/',views.detailpage.as_view(),name='question_detail'),
        path('update/<int:pk>/',views.updatepost.as_view(),name='question_update'),
        path('delete/<int:pk>/',views.deletequestion,name='delete_question'),
        path('questioncreate/',views.question_create,name='question_create'),
        path('usrinf/<int:pk>/',views.profile_user_info,name='userinfo'),
        path('draft/',views.draftquestions.as_view(),name='draft_question'),
        path('published/<int:pk>/',views.published_question,name='publish_question'),
        path('login/',views.login_user,name='login'),
        path('deleteanswer/<int:pk>/',views.delete_answer,name='delete_answer'),
        path('logout/',views.logout_user,name='logout'),
        path('registration/',views.register_user,name='registration'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
