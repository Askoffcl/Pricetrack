from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product,Order,Complaint,Register,Feedback
from .forms import AddProduct,FeedbackForm,ComplaintForm


def addProducts(request):
    if request.method == "POST":
        form = AddProduct(request.POST,request.FILES)
        if form.is_valid():
            product = form.save(commit = False)
            product.shopid = request.user
            product.save()
            return redirect('/homepage')
        else :
            print(form.error)
            messages.error(request,'invalid form data')
    form = AddProduct()
    return render(request,'addProducts.html',{'form' : form})


def viewProducts(request):
    pro = Product.objects.all()
    return render(request,'viewproducts.html',{'products':pro, 'search': 1})



def order(request,id):
    product = Product.objects.get(id = id)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        Order.objects.create(userid = request.user,quantity = quantity,productid = product)
    return render(request,'order.html',{'product':product,'quantity':quantity})

def order_placed(request):
    orders = Order.objects.filter(userid = request.user)
    return render (request,'orderplaced.html',{'orders':orders})


def feedback(request,id):
    product=Product.objects.get(id = id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            feedback = form.save(commit = False)
            feedback.productid = product
            feedback.userid = request.user
            feedback.save()
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('/homepage')
        else:
            print(form.errors)
            messages.error(request, 'Invalid form data')
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
            messages.error(request,'invalid form')
    else :
        form = ComplaintForm()


    return render(request,'complaint.html',{'form':form})

def productSearch(request):
    query = request.GET.get('search', ' ').strip()
    print(query)
    print(Product.objects.filter(productname__icontains=query))
    if query :
        products = (
            Product.objects.filter(productname__icontains=query) |
            Product.objects.filter(brand__icontains=query)
        ).order_by('price')
    else:
        products = Product.objects.all().order_by('price')

    
    recommend = products.first()

    return render(request, 'viewproducts.html', {
        'products': products,
        'recommended': recommend ,
        'search':1
    })



def viewComplaint(request):
    complaint = Complaint.objects.all()
    return render(request,'ViewComplaint.html',{'complaint':complaint})

def updateStatus(request,id):
    complaint = Complaint.objects.get(id = id)
    if request.method == 'POST':
        newStatus = request.POST.get('status')
        if newStatus in ['pending','working on','resolved']:
            complaint.status = newStatus
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
    complaint = Complaint.objects.filter(userid = request.user)
    return render(request,'complaintStatus.html',{'complaints':complaint})


def viewFeedback(request):
    fed = Feedback.objects.filter(productid__shopid = request.user)
    return render(request,'viewFeedback.html',{'feds':fed})

def viewShopuser(request):
    users = Register.objects.filter(role = 'User')
    return render(request,'viewShopowner.html',{'users':users})