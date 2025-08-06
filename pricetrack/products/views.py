from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.db.models import Sum, F



def addProducts(request):
    if request.method == "POST":
        form = AddProduct(request.POST,request.FILES)
        if Product.objects.filter(productname = request.POST.get('productname')).exists():
            messages.error(request, 'Productname already exists')
            return render(request,'addProducts.html',{'form' : form})   
        if form.is_valid():
            product = form.save(commit = False)
            product.shopid = request.user
            product.save()
            return redirect('/homepage')
        else :
            print(form.errors)
            messages.error(request,form.errors)
    form = AddProduct()
    return render(request,'addProducts.html',{'form' : form})








def order_placed(request):
    if request.user.role == 'User':
        orders = Order.objects.filter(userid = request.user).order_by('-id')
        for order in orders:
            payment = Payment.objects.filter(orderid=order).first()
            order.payment_method = payment.method if payment else "Cash On delivery"

    elif request.user.role == 'retailer':
        orders = Order.objects.filter(productid__shopid=request.user).order_by('-id')
        for order in orders:
            payment = Payment.objects.filter(orderid=order).first()
            order.payment_method = payment.method if payment else "Cash on delivery"
    else :
        orders = Order.objects.all().order_by('-id')
        for order in orders:
            payment = Payment.objects.filter(orderid=order).first()
            order.payment_method = payment.method if payment else "Cash sson delivery"
    return render (request,'orderplaced.html',{'orders':orders})


def feedback(request,id):
    order = Order.objects.get(id=id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            feedback = form.save(commit = False)
            feedback.productid = shopProduct.objects.get(id=order.productid.id)
            feedback.userid = request.user
            feedback.orderid = order
            feedback.save()
            messages.success(request, 'Feedback submitted successfully!')
            order.fed = 2
            order.save()
            return redirect('/homepage')
        else:
            print(form.errors)
            messages.error(request,form.errors)
    else:
        form = FeedbackForm()
        

    return render(request, 'feedBack.html', {'form': form})


def complaint(request,id):
    if request.method == 'POST':
        form = ComplaintForm(request.POST,request.FILES)
        if form.is_valid():
            complaint = form.save(commit = False)
            complaint.userid = request.user  
            complaint.save()
            messages.success(request,'complaint was success')
            return redirect('/homepage')
        else :
            print(form.errors)
            messages.error(request,form.errors)
    else :
        form = ComplaintForm()


    return render(request,'complaint.html',{'form':form})


def viewComplaint(request):
    complaint = Complaint.objects.filter(
    status__in=['pending', 'working on']
).order_by('-id')

    return render(request,'ViewComplaint.html',{'complaint':complaint})

def updateStatus(request,id):
    complaint = Complaint.objects.get(id = id)
    if request.method == 'POST':
        newStatus = request.POST.get('status')
        reason = request.POST.get('reason')
        if newStatus in ['pending','working on','resolved']:
            complaint.status = newStatus
            complaint.reason = reason
            complaint.save()
            print('success')
        else:
            print('failed')
        return redirect('viewComplaint')

def activate(request,id):
    user = Register.objects.get(id = id)
    user.is_active = True
    user.save()
    return redirect('viewShopowner')
def deactivate(request,id):
    user = Register.objects.get(id = id)
    user.is_active = False
    user.save()
    return redirect('viewShopowner')

def viewShopowner(request):
    users = Register.objects.filter(role = 'retailer')
    return render(request,'viewShopowner.html',{'users':users})

def complaintStatus(request):
    complaint = Complaint.objects.filter(userid = request.user).order_by('-id') 
    return render(request,'complaintStatus.html',{'complaints':complaint})


def viewFeedback(request):
    fed = Feedback.objects.filter(productid__shopid = request.user)
    return render(request,'viewFeedback.html',{'feds':fed})

def viewFeed(request,id):

    fed = Feedback.objects.get(orderid = id)
    
    return render(request,'viewFeedback.html',{'fed':fed})

def viewShopuser(request):
    users = Register.objects.filter(role = 'User')
    return render(request,'viewShopuser.html',{'users':users})

def add_ShopProduct(request,id):
      shop = Product.objects.get(id=id)
      if request.method == "POST":
        form = addShopProduct(request.POST,request.FILES)
        if form.is_valid():
            product = form.save(commit = False)
            product.productid = shop
            product.shopid = request.user
            product.productname = shop.productname
            product.save()
            return redirect('/homepage')
        else :
            print(form.errors)
            messages.error(request,form.errors)
           
        form = addShopProduct()
        return render(request,'addShopProduct.html',{'form' : form})
      


def productSearch(request):
    query = request.GET.get('search', ' ').strip()
    if query :
        products = (
            Product.objects.filter(productname__icontains=query) |
            Product.objects.filter(brand__icontains=query)
        ).order_by('price')
      
    else:
        products = Product.objects.all().order_by('price')

    return render(request, 'viewproducts.html', {
        'products': products,
        
        'search':1
    })

def viewProducts(request):
    pro = Product.objects.all()
    return render(request,'viewproducts.html',{'products':pro, 'search': 1, 'available': 1})

from django.db.models import Q

def shopSearch(request):
    cat = Category.objects.all()
    fed = Feedback.objects.all()
    query = request.GET.get('search', '').strip()
    print(query + ' in 2')

    # For User or Admin
    if request.user.role == 'User' or request.user.role == 'admin':
        if query:
            products = shopProduct.objects.filter(
                Q(productname__icontains=query) |
                Q(productid__brand__icontains=query) |
                Q(productcate__name__icontains=query)
            ).order_by('price')
        else:
            products = shopProduct.objects.all().order_by('price')

        recommend = products.first()

        return render(request, 'myShopProduct.html', {
            'products': products,
            'recommended': recommend,
            'search': 2,
            'fed': fed,
            'cats': cat
        })

    # For Shop Owner
    else:
        if query:
            products = shopProduct.objects.filter(
                shopid=request.user
            ).filter(
                Q(productname__icontains=query) |
                Q(productid__brand__icontains=query) |
                Q(productcate__name__icontains=query)
            ).order_by('price')
        else:
            products = shopProduct.objects.filter(shopid=request.user).order_by('price')

        return render(request, 'myShopProduct.html', {
            'products': products,
            'search': 2,
            'cats': cat
        })

        
def viewShopProducts(request):

    cat = Category.objects.all()
    print(cat)
    fed = Feedback.objects.all()
    if request.user.role == 'User'or request.user.role == 'admin':
        pro = shopProduct.objects.all().order_by('price')
        return render(request,'myShopProduct.html',{'products':pro, 'search': 2,'cats':cat,'fed':fed})
    pro = shopProduct.objects.filter(shopid=request.user)
 

    return render(request,'myShopProduct.html',{'products':pro, 'search': 2,'cats':cat})


def order(request, id):
    product = shopProduct.objects.get(id=id)
    products = Product.objects.get(id=product.productid.id)

    if request.method == 'POST':
        quantity_str = request.POST.get('quantity')
        payment = request.POST.get('payment_method')
        print(payment)
        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                messages.error(request, 'Quantity must not be zero or negative')
                return redirect('viewshopitems')
        except (ValueError, TypeError):
            messages.error(request, 'Invalid quantity')
            return redirect('viewshopitems')

        available = product.quantityAvailable

        if quantity > available:
            messages.error(request, 'Stock not available')
            return redirect('viewshopitems')


        od=Order.objects.create(userid=request.user, quantity=quantity, productid=product, pid=products)
        product.quantityAvailable -= quantity
        product.save()

     
        if payment == 'card':
            return redirect('/product/card/'+str(od.id))
        elif payment == 'upi':
            return redirect('/product/upi/'+str(od.id))
        elif payment == 'cod':
            messages.success(request, 'Order placed successfully with Cash on Delivery!')
            return redirect('/product/cod/'+str(od.id))
        else:
            messages.error(request, 'Invalid payment method')
            return redirect('viewshopitems')






def allProducts(request,id):
    pro = shopProduct.objects.filter(shopid = id)
    return render(request,'myShopProduct.html',{'products':pro, 'search': 2})

def available(request):
    if request.method == "POST":
        form = notAvailable(request.POST,request.FILES)
        if form.is_valid():
            product = form.save(commit = False)
            product.shopid = request.user
            product.save()
            return redirect('/homepage')
        else :
            print(form.errors)
            messages.error(request,form.errors)
    form = notAvailable()
    return render(request,'request.html',{'form' : form})

def viewRequest(request):
    req = Available.objects.filter(status = "Not Added")
    return render(request,'notAvailable.html',{'reqs':req})

def notAvailablereq(request,id):
    req = Available.objects.get(id = id)
    if request.method == 'POST':
        
        Product.objects.create(shopid=req.shopid,productname=req.productname,productcate=req.productcate,brand=req.brand,price=req.price,description=req.description,image=req.image)
        req.status = "ADDED"
        req.save()
        return redirect('/homepage')
    
def rejected(request,id):
    print('d')
    req = Available.objects.get(id = id)
    print("fefe")
    if request.method == 'POST':
        req.status = "Product Rejected"
        req.save()
        return redirect('/homepage')

    return render(request,'notAvailable.html',{'reqs':req})
def viewallreq(request):
    req = Available.objects.filter(shopid=request.user)
    return render(request,'viewAvailableReq.html',{'reqs':req})




def editProduct(request, id):
    product = Product.objects.get(id = id )

    if request.method == "POST":
        
        mrp = request.POST.get("mrp")
        feature = request.POST.get("feature")
        if mrp:
            product.price = mrp
        if feature:
            product.description = feature
        product.save()

        return redirect("viewproducts")  

    return render(request, "editProduct.html", {"product": product})

def orderplaced(request,id):
    pro = Register.objects.get(id = id)
    orders = Order.objects.filter(userid = pro).order_by('-id')

    return render (request,'orderplaced.html',{'orders':orders})


def productDetail(request,id):
    pro = Product.objects.get(id = id)
    return render(request,'productDetails.html',{'pro':pro})



def  filters(request, category):
    cat = Category.objects.all()
    products = shopProduct.objects.filter(productid__productcate=category)
    return render(request, 'myShopProduct.html', {'products': products,'search':2,'cats':cat})
def detail(request,id):
    pro = shopProduct.objects.get(id = id)
    return render(request,'detail.html',{'pro':pro})

def requestHistory(request):
    req = Available.objects.all()
    return render(request,'requestHistory.html',{'req':req})


def category(request):
    if request.method == 'POST':
        name = request.POST.get('category')
        
        if name:
            name = name.strip().capitalize()
            Category.objects.get_or_create(name=name)
    obs = Category.objects.all()

    return render(request, 'category.html',{'ob':obs})



def delete_cat(request,id):
    cat=Category.objects.get(id=id)
    cat.delete()
    return redirect('/product/category')
    
def cart(request, id):
    product = shopProduct.objects.get(id=id)
    user = Register.objects.get(id=request.user.id)
    existing_item = Cart.objects.filter(shopid=user, productid=product).first()
    if existing_item:
        messages.warning(request, 'Product is already in your cart.')
    else:
        Cart.objects.create(shopid=user, productid=product, quantityAvailable=1)
        messages.success(request, 'Added to cart.')

    return redirect('viewcart')


def viewCart(request):
    pro = Cart.objects.filter(shopid=request.user.id).order_by('-id')
    for item in pro:
        item.total_price = item.productid.price * item.quantityAvailable 
    total = pro.aggregate(
        cart_total=Sum(F('productid__price') * F('quantityAvailable'))
    )['cart_total'] or 0
    return render(request,'cart.html',{'pros':pro,'total':total})





@require_POST
@csrf_exempt
def update_quantity(request, cart_id):
    try:

        data = json.loads(request.body)
        new_quantity = int(data.get('quantity', 0))  

        if new_quantity < 1:
            return JsonResponse({'error': 'Invalid quantity'}, status=400)

        cart_item = Cart.objects.get(id=cart_id)
        sp = shopProduct.objects.get(id=cart_item.productid.id)

        if new_quantity <= sp.quantityAvailable:       
            cart_item.quantityAvailable = new_quantity
            cart_item.save()
        else :
            messages.error(request,'stock not available')     

        return JsonResponse({
            'success': True,
            'new_quantity': new_quantity,
            'available_stock': sp.quantityAvailable
        })

    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Cart item not found'}, status=404)

    except shopProduct.DoesNotExist:
        return JsonResponse({'error': 'Product not available in shop'}, status=404)

    except ValueError:
        return JsonResponse({'error': 'Invalid quantity format'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def checkout(request, id):
    product = shopProduct.objects.get(id=id)
    
    return render(request, 'checkout.html', {
        'product': product,'total':1
    })




def totalCheckout(request):
    return render(request,'checkout.html')



@csrf_exempt
@require_POST
def remove_from_cart(request, cart_id):
    try:
        cart_item = Cart.objects.get(id=cart_id)
        cart_item.delete()
        return JsonResponse({'success': True})
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Cart item not found'}, status=404)


def card(request,id):
    try:
        od=Order.objects.get(id=id)
    except:
        od=None
    if request.method == 'POST':
        name = request.POST.get('name')
        number = request.POST.get('number')
        cvv = request.POST.get('cvv')
        date = request.POST.get('expiry')
        Payment.objects.create(name=name,method='card',orderid=od)
        messages.success(request, 'Order placed successfully !')
        return redirect('orderdone')
    return render(request,'card.html',{'order':od})

def upi(request,id):
    try:
        od=Order.objects.get(id=id)
    except:
        od=None
    if request.method == 'POST':
        name = request.POST.get('upi_id')
        Payment.objects.create(name=name,method="upi",orderid=od)
        messages.success(request, 'Order placed successfully !')
        return redirect('orderdone')
    return render(request,'upi.html',{'order':od})

def cod(request,id):
    try:
        od=Order.objects.get(id=id)
    except:
        od=None
    Payment.objects.create(method='cod',orderid=od)
    messages.success(request, 'Order placed successfully !')
    return redirect('orderdone')


def payment(request):
    product = Payment.objects.all()
    return render(request, 'order.html', {'product': product, 'quantity': quantity})




def checkout_multiple(request):

    if request.method == 'POST':
        product_ids = request.POST.getlist('product_ids')
        print(product_ids)
        products = shopProduct.objects.filter(productid__id__in=product_ids)
        total = sum([p.productid.price * p.quantityAvailable for p in products])
        return render(request, 'checkout_multiple.html', {'products': products, 'total': total,'product_ids':product_ids})
    return redirect('/product/viewCart')


def place_bulk_order(request):
    print('outf')
    if request.method == 'POST':
        print('inf')
        print(request.body)

        payment_method = request.POST.get('payment_method')
        product_ids = request.POST.getlist('product_ids')  
        print(product_ids)
        ct=Cart.objects.filter(productid__in=product_ids,shopid__id=request.user.id)
        print(ct)
        print(ct,"fknf")
        for cart_item in ct :
            pid = cart_item.productid.id
            print(pid)
            quantity = cart_item.quantityAvailable  
            # base_product = Product.objects.get(id=pid)
            products = shopProduct.objects.filter(id=pid)
            print(products,"ksfjndfj")
            print('out')
            for product in products:
                if quantity <= product.quantityAvailable:
                    print('in')
                    od=Order.objects.create(
                        userid=request.user,
                        quantity=quantity,
                        productid=product,
                        # pid=base_product,
                        # method=payment_method
                    )
                    
                    product.quantityAvailable -= quantity
                    product.save()
                    if payment_method:
                        
                        Payment.objects.create(orderid=Order.objects.get(id=od.id),method=payment_method)
                    break
                else:
                    messages.error(request, f'Stock not available for {product.productname}')
                    return redirect('cart')

        # Optionally clear the cart
        ct.delete()

        if payment_method == 'card':
            return redirect('/product/card/'+str(0))
        elif payment_method == 'upi':
            return redirect('/product/upi/'+str(0))
        else:
            messages.success(request, 'Order placed successfully!')
            return redirect('/product/cod/'+str(0))

    return redirect('/product/viewCart')


def orderdone(request):
    return render(request,'orderdone.html')



def delete_product(request, id):
    product = shopProduct.objects.get(id=id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('homepage')  # change to your desired redirect page
    return redirect('productdetail', id=id)
    
def delete_products(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('homepage')  # change to your desired redirect page
    return redirect('productdetail', id=id)