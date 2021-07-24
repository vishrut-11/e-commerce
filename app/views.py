from django.shortcuts import render,redirect
from django.views import View
from .models import Customer, Product, OrderPlaced, Cart
from .forms import CustomerRegistrationform, CustomerProfileform
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required    #functions based views
from django.utils.decorators import method_decorator        #classed based views (login_required, name="dispatch")
from django.db.models import Q
from django.http import JsonResponse



class ProductView(View):
    def get(self, request):
        totalitem = 0
        topwear = Product.objects.filter(category="TW")
        bottomwear = Product.objects.filter(category="BW")
        mobiles = Product.objects.filter(category="M")
        laptop = Product.objects.filter(category="L")
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        context = {"topwear":topwear, "bottomwear":bottomwear, "mobiles":mobiles, "laptop":laptop, "totalitem":totalitem}
        return render(request, "app/home.html", context)
        
class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_incart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_incart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists
        return render(request, "app/productdetail.html",
        {"product":product, "item_already_incart":item_already_incart, "totalitem":totalitem})

@login_required
def add_to_cart(request):
    totalitem = 0
    user = request.user
    product_id = request.GET.get("pro-id")
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return redirect("/cart", {"totalitem":totalitem})

def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == user] #list comprehension
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.selling_price)
                amount = amount + temp_amount
            total_amount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {"carts":cart, "total_amount":total_amount, "amount":amount, "totalitem":totalitem})
        else:
            return render(request, "app/emptycart.html")


def plus_cart(request):
    if request.method == "GET":
        pro_id = request.GET["pro_id"]
        print(pro_id)
        c = Cart.objects.get(Q(product=pro_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.selling_price)
            amount = amount + temp_amount
            total_amount = amount
        data ={
            "quantity": c.quantity,
            "amount":amount,
             "total_amount":total_amount + shipping_amount,
            }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == "GET":
        pro_id = request.GET['pro_id']
        c = Cart.objects.get(Q(product=pro_id) & Q(user=request.user))
        c.quantity-= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.selling_price)
            amount = amount + temp_amount
            total_amount = amount 
        data ={
            "quantity": c.quantity,
            "amount":amount,
              "total_amount":total_amount + shipping_amount,
            }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        pro_id = request.GET["pro_id"]
        c = Cart.objects.get(Q(product=pro_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.selling_price)
            amount = amount + temp_amount
            total_amount = amount 

        data ={
            "amount":amount,
            "total_amount":total_amount + shipping_amount,
            }
        return JsonResponse(data)

        
@login_required
def buy_now(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    add = Customer.objects.filter(user=user)
    buy_product = Customer.objects.filter(user=user)
    product_id = request.GET.get("pro-id")
    product = Product.objects.get(id=product_id)
    amount = 0.0
    shipping_amount = 70.0
    return render(request, 'app/buynow.html',{"add":add, "product":product, "totalitem":totalitem})

def mobile(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        mobiles = Product.objects.filter(category="M")
    elif data == "APPLE" or data == "SAMSUNG" or data == "Redmi" or data == "POCO":
        mobiles = Product.objects.filter(category="M").filter(brand=data)
    elif data == "below":
        mobiles = Product.objects.filter(category="M").filter(selling_price__lt=20000)
    elif data == "above":
        mobiles = Product.objects.filter(category="M").filter(selling_price__gt=20000)
    return render(request, 'app/mobile.html', {"mobiles": mobiles, "active":"btn-primary","totalitem":totalitem })

def topwear(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        topwear = Product.objects.filter(category="TW")
    elif data == "HELMONT" or  data == "Tricky" or data == "Eyebogler"  or data == "Try" or data == "FastColors":
        topwear = Product.objects.filter(category="TW").filter(brand=data)
    elif data == "below":
        topwear = Product.objects.filter(category="TW").filter(selling_price__lt=500)
    elif data == "above":
        topwear = Product.objects.filter(category="TW").filter(selling_price__gt=500)
    return render(request, "app/topwear.html", {"topwear":topwear, "totalitem":totalitem})

def bottomwear(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        bottomwear = Product.objects.filter(category="BW")
    elif data == "Lzard" or data == "DENIM" or data =="METRONAUT" or data == "HIGHLANDER" or data == "Billion":
        bottomwear = Product.objects.filter(category="BW").filter(brand=data)
    elif data == "below":
        bottomwear = Product.objects.filter(category="BW").filter(selling_price__lt=500)
    elif data == "above":
        bottomwear = Product.objects.filter(category="BW").filter(selling_price__gt=500)
    return render(request, "app/bottomwear.html", {"bottomwear":bottomwear, "totalitem":totalitem})

def laptop(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        laptop = Product.objects.filter(category="L")
    elif data == "APPLE" or data == "ASUS" or data == "HP" or data == "acer" or data == "Lenovo":
        laptop = Product.objects.filter(category="L").filter(brand=data)
    elif data == "below":
        laptop = Product.objects.filter(category="L").filter(selling_price__lt=100000)
    elif data == "above":
        laptop = Product.objects.filter(category="L").filter(selling_price__gt=100000)
    return render(request,"app/laptop.html", {"laptop":laptop, "totalitem":totalitem})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationform()
        return render(request, 'app/customerregistration.html', {"form":form})
    def post(self, request):
        form = CustomerRegistrationform(request.POST)
        if form.is_valid():
            messages.success(request, "Congrulations!! Your account is created successfully")
            form = CustomerRegistrationform()
        return render(request, 'app/customerregistration.html', {"form":form})



@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    def get(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileform()
        return render(request, "app/profile.html",{"form":form,  "active":"btn-primary", "totalitem":totalitem})

    def post(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileform(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data["name"]      
            locality = form.cleaned_data["locality"]      
            city = form.cleaned_data["city"]      
            state = form.cleaned_data["state"]      
            zipcode = form.cleaned_data["zipcode"]   
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)   
            reg.save()
            messages.success(request, "Congratulations !! profile Created successfully")
            form = CustomerProfileform()
        return render(request,"app/profile.html",{"form":form, "totalitem":totalitem, "active":"btn-primary"})



@login_required
def address(request):
    totalitem = 0
    add = Customer.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html', {"add":add, "active":"btn-primary", "totalitem":totalitem})


#This function will update or edit the info.
@login_required
def update_data(request, id):
    if request.method == 'POST':
        pi = Customer.objects.get(pk=id)
        form = CustomerProfileform(request.POST, instance=pi)
        if form.is_valid():
            form.save()
        messages.info(request, "Congratulations !! profile updated successfully")
        return render(request, "app/profile.html",{"form":form,  "active":"btn-primary"})
    else:
        pi = Customer.objects.get(pk=id)
        form = CustomerProfileform(instance=pi)
        return render(request, "app/update.html",{'form':form})



#This function will delete the info.
@login_required
def delete_data(request, id):
    if request.method == "POST":
        pi = Customer.objects.get(pk=id)
        pi.delete()
        messages.warning(request, "profile Delete successfully")
        return redirect("profile")

        
@login_required
def checkout(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_product = Customer.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            temp_amount = (p.quantity * p.product.selling_price)
            amount = amount + temp_amount
        temp_amount = amount + shipping_amount
    return render(request, 'app/checkout.html',{"add":add, "cart_product":cart_product, "temp_amount":temp_amount, "totalitem":totalitem})
    # else:
    #     return render(request, 'app/buynow.html',{"add":add, "cart_product":cart_product, "totalitem":totalitem})


@login_required
def orders(request):
    totalitem = 0
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {"order_placed": op, "totalitem":totalitem})       

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get("custid")
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

def search(request):
    query=request.GET['query']
    if len(query)>78:
       data = Product.objects.none()
    else:
        dataTitle= Product.objects.filter(title__icontains=query)
        databrand= Product.objects.filter(brand__icontains=query)
        data = dataTitle.union(dataTitle, databrand)
        
    if data.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'data': data, 'query': query}
    return render(request, 'app/search.html',params)