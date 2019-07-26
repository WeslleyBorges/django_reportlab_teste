"""djangotest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from teste.views import UserListView, pdf_test, write_pdf_view, pdf_lorem_ipsum, pdf_table_test, my_own_grid #, html_to_pdf_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('teste/', UserListView.as_view()),
    path('pdfteste/', pdf_test),
    path('pdfteste2/', write_pdf_view),
    #path('pdfteste3/', html_to_pdf_view),
    path('pdfteste4/', pdf_table_test),
    path('pdf_lorem_ipsum/', pdf_lorem_ipsum),
    path('my_own_grid/', my_own_grid)
]
