from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import View
from . models import Product, Customer, Cart
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
# from django.contrib.auth.decorators import login_required

# Create your views here.
def my_view(request):
    context = {'foo': 'bar'}
    return render(request, 'my_template.html', context)

def home(request):
    return render(request, "app/home.html")

def about(request):
    return render(request, "app/about.html")

def contact(request):
    return render(request, "app/contact.html")

class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html", locals())
    
class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, "app/category.html", locals())
       
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request, "app/productdetail.html", locals())
    
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! You have registered Successfully")
        else:
            messages.warning(request,"Invalid Data Input")
        return render(request, 'app/customerregistration.html',locals())

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, "app/profile.html", locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            county = form.cleaned_data['county']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, county=county, zipcode=zipcode)
            reg.save()
            messages.warning(request,"Congratulations! Your profile has been saved successfully")
        else:
             messages.warning(request,'Invalid Data Input')
        return render(request, "app/profile.html", locals())

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, "app/address.html", locals())

class updateAddress(View):
    def get(self,request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, "app/updateAddress.html", locals())
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']                     
            add.city = form.cleaned_data['city']  
            add.mobile = form.cleaned_data['mobile']          
            add.county = form.cleaned_data['county']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, 'Your profile was successfully updated!')
        else:
            messages.warning(request, 'Invalid Data Input.')
        return redirect('address')
    
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product =Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount= 0
    for p in cart:
        value =p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 50    
    return render(request, 'app/addtocart.html',locals())   

class checkout(View):
    def get(self,request):
        user = request.user
        add= Customer.objects.filter(user=user)
        cart_items= Cart.objects.filter(user=user)
        famount= 0
        for p in cart_items:
            value =p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 50   
        return render(request,'app/checkout.html', locals())
    
def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.object.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount= 0
        for p in cart:
            value =p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 50    
        # print(prod_id)
        data={  
              'quantity':c.quantity,
              'amount':amount,
              'totalamount':totalamount       
        }
        return JsonResponse(data)
        
def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.object.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount= 0
        for p in cart:
            value =p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 50    
        # print(prod_id)
        data={  
              'quantity':c.quantity,
              'amount':amount,
              'totalamount':totalamount       
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.object.get(Q(product=prod_id) & Q(user=request.user))        
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount= 0
        for p in cart:
            value =p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 50    
        # print(prod_id)
        data={  
              'quantity':c.quantity,
              'amount':amount,
              'totalamount':totalamount       
        }
        return JsonResponse(data)

def status(self, obj):
    if obj.payment.paid:
        return 'Accepted'
    else:
        return 'Pending'
        
        
        
    


# @login_required
# def cart(request):
#     cart = Cart.objects.filter(user=request.user)
#     amount = 0.0
#     shipping_amount = 50.0
#     totalamount = 0.0
#     cart_product = [p for p in cart]
#     if cart_product:
#         for p in cart_product:
#             value = (p.quantity * p.product.discounted_price)
#             amount += value
#             totalamount = amount + shipping_amount
#         context = {'cart': cart_product, 'totalamount': totalamount, 'amount': amount}
#         return render(request, 'app/addtocart.html', context)
#     else:
#         return render(request, 'app/addtocart.html')

