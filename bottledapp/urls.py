from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('adminloginpg/', views.adminloginpg, name='adminloginpg'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('admindb/', views.admindb, name='admindb'),
    path('adminlogout/', views.adminlogout, name='adminlogout'),
    path('viewproduct/<int:pk>/', views.viewproduct, name='viewproduct'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('addcategory/', views.addcategory, name='addcategory'),
    path('addcategoryf/', views.addcategoryf, name='addcategoryf'),
    path('addproductf/', views.addproductf, name='addproductf'),
    path('deletecat/<int:pk>/', views.deletecat, name='deletecat'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('editf/<int:pk>/', views.editf, name='editf'),
    path('deletepdt/<int:pk>/', views.deletepdt, name='deletepdt'),
    path('search/', views.search_product, name='search_product'),
    path('contact_mail',views.contact_mail, name= 'contact_mail'),
    path('userlogin',views.userlogin, name= 'userlogin'),
    path('userreg',views.userreg, name= 'userreg'),
    path('addtocart/', views.addtocart, name='addtocart'),
    path('deleteitem/<int:pk>/', views.deleteitem, name='deleteitem'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
]
