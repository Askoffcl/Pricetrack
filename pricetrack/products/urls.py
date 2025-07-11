from django.urls import path
from . import views

urlpatterns=[
    path('addproducts/',views.addproducts),
    path('viewproducts/',views.viewproducts),
    path('order/<int:id>/',views.order,name='order'),
    path('orderplaced/',views.order_placed,name='orderplaced'),
    path('feed/<int:id>/',views.feed,name='feed'),
    path('complaint/<int:id>/',views.complaint,name='complaint'),
    path('productsearch',views.productsearch,name="productsearch"),
    path('viewComplaint',views.viewComplaint,name='viewComplaint'),
    path('updateStatus/<int:id>/',views.updateStatus,name='updateStatus'),
    path('activate/<int:id>/',views.activate,name='active'),
    path('deactivate/<int:id>/',views.deactivate,name='deactive'),
    path('viewShopowner/',views.viewShopowner,name='viewShopowner'),
    path('complaintStatus',views.complaintStatus),
    path('viewFeedback',views.viewFeedback),
    path('viewShopuser/',views.viewShopuser,name='viewShopuser')
    

]


