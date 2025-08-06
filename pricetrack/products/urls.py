from django.urls import path
from . import views

urlpatterns=[
    path('addproducts/',views.addProducts),
    path('viewproducts/',views.viewProducts,name='viewproducts'),
    path('order/<int:id>/',views.order,name='order'),
    path('orderplaced/',views.order_placed,name='orderplaced'),
    path('feed/<int:id>/',views.feedback,name='feed'),
    path('complaint/<int:id>/',views.complaint,name='complaint'),
    path('productsearch',views.productSearch,name="productsearch"),
    path('viewComplaint',views.viewComplaint,name='viewComplaint'),
    path('updateStatus/<int:id>/',views.updateStatus,name='updateStatus'),
    path('activate/<int:id>/',views.activate,name='active'),
    path('deactivate/<int:id>/',views.deactivate,name='deactive'),
    path('viewShopowner/',views.viewShopowner,name='viewShopowner'),
    path('complaintStatus',views.complaintStatus),
    path('viewFeedback',views.viewFeedback),
    path('viewShopuser/',views.viewShopuser,name='viewShopuser'),
    path('addShopProduct/<int:id>/',views.add_ShopProduct,name = 'addShopProduct'),
    path('viewshopProduct/',views.viewShopProducts,name='viewshopitems'),
    path('shopSearch',views.shopSearch,name="shopSearch"),
    path('allProducts/<int:id>/',views.allProducts,name="allproduct"),
    path('request/',views.available),
    path('notavailable',views.viewRequest),
    path('notAvailablereq/<int:id>/',views.notAvailablereq,name='notAvailablereq'),
     path('rejected/<int:id>/',views.rejected,name='rejected'),
    path('viewallreq/',views.viewallreq),
    path('editProduct/<int:id>/',views.editProduct,name='editProduct'),
    path('orderplaced/<int:id>/',views.orderplaced,name = 'orderplaced'),
    path('productdetail/<int:id>/',views.productDetail,name = 'productdetail'),
    path('filters/<str:category>/',views.filters,name = 'filters'),
    path('detail/<int:id>/',views.detail,name = 'detail'),
    path('requestHistory',views.requestHistory),
    path('category',views.category),            
    path('delete_cat/<int:id>/',views.delete_cat),
    path('viewFeed/<int:id>',views.viewFeed),
    path('cart/<int:id>/',views.cart,name='cart'),
    path('viewCart',views.viewCart,name='viewcart'),
    path('cart/update-quantity/<int:cart_id>/', views.update_quantity, name='update_quantity'),
    path('checkout/<int:id>/',views.checkout,name='checkout'),
    path('totalCheckout',views.totalCheckout),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('card/<int:id>',views.card,name='process_payment'),
    path('upi/<int:id>',views.upi,name='upi'),
    path('cod/<int:id>',views.cod,name='cod'),
    path('checkout/multiple/', views.checkout_multiple, name='checkout_multiple'),
    path('order/place-bulk/', views.place_bulk_order, name='place_bulk_order'),
    path('orderdone',views.orderdone,name='orderdone'),
    path('product/delete/<int:id>/', views.delete_product, name='deleteproduct'),
    path('product/delete/<int:id>/', views.delete_products, name='deleteproducts'),




]


