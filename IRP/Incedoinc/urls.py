from django.urls import path
from . import views
from django.conf.urls import url
from  . import views as core_views
from .views import dashboard, manage_jd_view, manage_job_view, upload_jd_view, upload_job_view
from django.contrib.auth import views as auth_views

#download-file
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #pulkit-kartikeyan
    #path("", views.index, name='home'),
    path("home/",views.home_view, name='home_page'),
    path("upload-jd/", views.upload_jd_view, name='upload_jd_page'),
    path("upload-job/", views.upload_job_view, name='upload_job_page'),
    path('manage-jd/', views.manage_jd_view, name='manage_jd_page'),
    path('manage-job/', views.manage_job_view, name='manage_job_page'),
    # path("search-jd/<str:requisition_id>/", views.search_jd_view, name='search_jd_page'),
    # path('media/<str:path>/', views.download_view),
    path("add-candidate/", views.add_candidate_view, name='add_candidate_page'),

    #vaishnavi


    ## rudra
    path('search_candidate/feedback/<str:req_id>/<str:email_id><int:level>/', views.feedback, name='feedback'),
    path("search_candidate/", views.search_candidate, name = 'search_candidate'),
    # path('test/', views.test, name = 'test_name'),
    path('search_candidate/feedback/<str:req_id>/<str:email_id><int:level>/edit<int:edit_level>/', views.edit, name ='edit'),
    path("search_candidate/<str:candidate_email>", views.search_candidate, name = 'search_candidate_email'),
    path("edit_candidate/<str:candidate_email>", views.edit_candidate, name = 'edit_candidate'),
    path("view_candidate/<str:candidate_email>", views.view_candidate, name = 'view_candidate'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
