from django.shortcuts import render,redirect
from .models import*
from django.core.paginator import Paginator
from django.contrib import messages
import razorpay

# Create your views here.
def index(request):
    pid = Product.objects.all()
    
    context = {

        "pid": pid,
      
    }
    return render (request,'index.html',context)

def blog(request):
    return render (request,'blog.html')

def single_product(request,sp):
    spid=Product.objects.get(id=sp) 
    return render (request,'single_product.html',{"spid":spid})

def couponCode(request):
    uid = Register.objects.get(email=request.session['email'])
    if request.method == "POST":
        coupon_code = request.POST.get('coupon')
        ccid=Coupon.objects.filter(coupon_code=coupon_code).exists()
        if ccid:
            ccid1=Coupon.objects.get(coupon_code=coupon_code)
            ucid=User_coupon.objects.filter(user_id=uid, coupon_id=ccid1).exists()
            if ucid:
                messages.info(request, "You have already used this coupon.")
                return redirect("cart")
            else:
                User_coupon.objects.create(user_id=uid, coupon_id=ccid1,ex=True)
                messages.success(request, "Coupon applied successfully!")
                return redirect("cart")
        else:
            messages.error(request, "Invalid coupon code .")
            return redirect("cart")
    else:
        return render(request,"cart.html")    
    

def wish_list1(request,pi):
    if "email" in request.session:
        uid = Register.objects.get(email=request.session['email'])
        print(uid)
        pid = Product.objects.get(id=pi)
        print(pid)
        wish = Wish_list.objects.filter(user_id=uid,product_id=pid).first()
        if wish == None:
                Wish_list.objects.create(
                    user_id = uid,
                    product_id = pid,
                    name = pid.name,
                    price = pid.price,
                    img = pid.image,
                )
                messages.success(request, "product add in to wish list successfully .")
                return redirect ("category")
        else:
            wish.delete()
            messages.info(request, "product has removed in to the wish list .")
            return redirect ('category')
    else:
        return render(request, 'login.html', {"msg": "You are not logged in"})

def wish_list(request):
    if "email" in request.session:
        uid = Register.objects.get(email=request.session['email'])
        wish = Wish_list.objects.filter(user_id=uid)
        count = Wish_list.objects.filter(user_id=uid).count()
        context = {
            "wish":wish,
            "count":count
        }
        return render (request, "wish_list.html",context)
    else:
        return render(request, 'login.html', {"msg": "You are not logged in"})

def list_delete(request,did):
    if "email" in request.session:
        uid = Register.objects.get(email=request.session['email'])
        wish_id= Wish_list.objects.get(id=did)
        prodect_id = wish_id.product_id
        wish1 = Wish_list.objects.filter(user_id=uid,product_id=prodect_id).first()
        if wish1:
            wish1.delete()
            return redirect('wish_list')
    else:
        return render(request, 'login.html', {"msg": "You are not logged in"})



def cart(request):
    if "email" in request.session:
        try:
            uid = Register.objects.get(email=request.session['email'])
            cart1 = Add_cart.objects.filter(user_id=uid)
            ucid=User_coupon.objects.filter(user_id=uid,ex=True).order_by("-id").first()
            subtotal = sum(item.total_price for item in cart1)
            shipping =  50
            count = Add_cart.objects.filter(user_id=uid).count()
            total_product_price = subtotal+shipping
            if ucid == None:
                discount=0
            else:  
                discount=ucid.coupon_id.discount
                total_product_price-=ucid.coupon_id.discount
        except Register.DoesNotExist:
            return render(request, 'login.html', {"msg": "User not found"})
        except Product.DoesNotExist:
            return render(request, 'cart.html', {"msg": "Product not found"})
        context = {
                    "cart1": cart1,
                    "subtotal":subtotal,
                    "count":count,
                    "shipping":shipping,
                    "discount":discount,
                    "total_product_price":total_product_price,
                }
        return render(request, 'cart.html',context)
    else:
        return render (request,'cart.html',{"msg": "User not found"})

def addToCart(request, sp):
    if "email" in request.session:
        try:
            cart1 = Product.objects.get(id=sp)
            print(cart1)
            user = Register.objects.get(email=request.session['email'])
            print(user)
            existing_cart = Add_cart.objects.filter(user_id=user, product_id=cart1).first()
            print(existing_cart)
            if existing_cart:
                existing_cart.quantity += 1
                existing_cart.total_price = existing_cart.quantity * existing_cart.price
                existing_cart.save()
            else:
                Add_cart.objects.create(
                    product_id=cart1,
                    user_id=user,
                    name=cart1.name,
                    img=cart1.image,
                    price=cart1.price,
                    quantity=1,
                    total_price=cart1.price,
                )
            return redirect('cart')
        except Product.DoesNotExist:
            return render(request, 'cart.html', {"msg": "Product not found"})
        except Register.DoesNotExist:
            return render(request, 'login.html', {"msg": "User not found"})
    else:
        return render(request, 'login.html', {"msg": "You are not logged in"})
    


def addCart(request,sp):
    if "email" in request.session:
        try:   
            cart1 = Add_cart.objects.get(id=sp)
            user = Register.objects.get(email=request.session['email'])
            product = cart1.product_id
            existing_cart = Add_cart.objects.filter(user_id=user, product_id=product).first()
            if existing_cart:
                existing_cart.quantity += 1
                existing_cart.total_price = existing_cart.quantity * existing_cart.price
                existing_cart.save()
            return redirect('cart')
        except :
            return render(request, 'cart.html', {"msg": "somethings wrong"})
    else:
        return render(request, 'login.html', {"msg": "You are not logged in"})
        
def decreaseCart(request,sp):
    if "email" in request.session:  
        try:   
            cart1 = Add_cart.objects.get(id=sp)
            user = Register.objects.get(email=request.session['email'])
            product = cart1.product_id
            existing_cart = Add_cart.objects.filter(user_id=user, product_id=product).first()
            if existing_cart:
                if existing_cart.quantity == 1:
                    existing_cart.delete()
                else:
                    existing_cart.quantity -= 1
                    existing_cart.total_price = existing_cart.quantity * existing_cart.price
                    existing_cart.save()
            return redirect('cart')
        except :
            return render(request, 'cart.html', {"msg": "somethings wrong"})
    else:
        return render(request, 'login.html', {"msg": "You are not logged in"})
    
def delete(request,sp):
    if "email" in request.session:
        try:
            cart1 = Add_cart.objects.get(id=sp)
            user = Register.objects.get(email=request.session['email'])
            product = cart1.product_id
            existing_cart = Add_cart.objects.filter(user_id=user, product_id=product).first()
            if existing_cart:
                existing_cart.delete()
                return redirect('cart')
        except :
            return render(request, 'cart.html',{"msg": "something's wrong"})
    else:
        return render(request, 'login.html', {"msg": "You are not logged in"})

        

def category(request):

    mc = Main_Category.objects.all()
    brid = Brand.objects.all()
    coid = Color.objects.all()
    pid = Product.objects.all()
    l1 = []
    if "email" in request.session:
        user = Register.objects.get(email = request.session['email'])
        wid = Wish_list.objects.filter(user_id=user)
        for i in wid:
            l1.append(i.product_id_id)

    mc2 = request.GET.get("mc2")
    if mc2:
        pid = pid.filter(sub_category=mc2)

    br2 = request.GET.get("br2")
    if br2:
        pid = pid.filter(brand=br2)

    co2 = request.GET.get("co2")
    if co2:
        pid = pid.filter(color=co2)

    if request.method == "POST":
        min1 = request.POST.get("min1")
        max1 = request.POST.get("max1")

        if min1:
            pid = pid.filter(price__gte=min1)
        if max1:
            pid = pid.filter(price__lte=max1)
    else:
        min1, max1 = None, None
    if request.method == "GET":
        ps = request.GET.get('psearch')
        if ps :
            pid = Product.objects.filter(name__icontains = ps)
        else:
            pass
    paginator = Paginator(pid,9)
    page_number = request.GET.get('page',1)
    pid1 = paginator.get_page(page_number)
    try:
        page_number = int(page_number)
    except (TypeError, ValueError):
        page_number = 1  
    show_page =paginator.get_elided_page_range(page_number,on_each_side=1,on_ends=1)

    context = {
        "mc": mc,
        "pid": pid,
        "brid": brid,
        "coid": coid,
        "min1": min1,
        "max1": max1,
        "l1":l1,
        "pid1":pid1,
        "show_page":show_page,
    }
    return render(request, 'category.html', context)

    

def checkout(request):
    if "email" in request.session:
        uid = Register.objects.get(email=request.session['email'])  
        try:
            count = Add_cart.objects.filter(user_id=uid).count()
            if count > 0:
                cart = Add_cart.objects.filter(user_id=uid)
                ucid = User_coupon.objects.filter(user_id=uid, ex=True).order_by("-id").first()
                shipping = 50
                discount = 0
                subtotal = 0
                total_product_price = 0
                subtotal = sum(item.total_price for item in cart)
                total_product_price = subtotal+shipping
                ucid=User_coupon.objects.filter(user_id=uid,ex=True).order_by("-id").first()
                if ucid == None:
                    discount=0
                else:
                    discount = ucid.coupon_id.discount
                    total_product_price = subtotal+shipping-ucid.coupon_id.discount
            else:
                return render(request, 'checkout.html', {"msg": "please Add items"})
        except:
            pass
        client = razorpay.Client(auth=('rzp_test_uqhoYnBzHjbvGF', 'jEhBs6Qp9hMeGfq5FyU45cVi'))
        response = client.order.create({
            'amount': int(total_product_price * 100),
            'currency': 'INR',
            'payment_capture': 1
        })
        print("Razorpay response:", response)
        context = {
            "subtotal":subtotal,
            "shipping":shipping,
            "cart":cart,
            "discount":discount,
            "total_product_price":total_product_price,
            "response":response,
            "count":count
            }
        return render (request,'checkout.html', context)
    else:
        return render(request, 'login.html', {"msg": "You are not logged in"})

def order(request):
    if 'email' in request.session:
        try:
            uid = Register.objects.get(email=request.session["email"])
            cart_items = Add_cart.objects.filter(user_id=uid)
            cart_count = cart_items.count()
            total_price = sum(item.total_price for item in cart_items)
            # response = None  # 🛠️ Ensures Razorpay response exists

            if cart_count > 0:
                ucid = User_coupon.objects.filter(user_id=uid, ex=True).order_by("-id").first()
              
                if ucid:
                    ucid.ex = False
                    ucid.save()
                    
            if request.method == "POST": 
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                company_name = request.POST['company_name']
                phone = request.POST['phone']
                email = request.POST['email']
                country = request.POST['country']
                address1 = request.POST['address1']
                address2 = request.POST['address2']
                city = request.POST['city']
                district = request.POST['district']
                pincode = request.POST['pincode']
                note = request.POST['note']
                Checkout.objects.create(
                    user_id=uid,
                    first_name=first_name,
                    last_name=last_name,
                    company_name=company_name,
                    phone=phone,
                    email=email,
                    country=country,
                    address1=address1,
                    address2=address2,
                    city=city,
                    district=district,
                    pincode=pincode,
                    note=note,
                )
            client = razorpay.Client(auth=('rzp_test_uqhoYnBzHjbvGF', 'jEhBs6Qp9hMeGfq5FyU45cVi'))
            response = client.order.create({
                'amount': int(total_price * 100),
                'currency': 'INR',
                'payment_capture': 1
            })
            print("Razorpay response:", response)
            for item in cart_items:
                Order.objects.create(
                    order_id=response['id'],
                    user_id=uid,
                    name=item.name,
                    price=item.price,
                    quantity=item.quantity,
                )
                item.delete()
            return redirect('confirmation')
                
        except:
            pass
            return redirect("confirmation")

    

def confirmation(request):
    if 'email' in request.session:
        uid = Register.objects.get(email=request.session["email"])
        oid = Order.objects.filter(user_id=uid)

        con={
            "oid":oid,
            }
        return render(request, "confirmation.html", con)
    else:
        return render(request, "login.html")

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        Contect.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        return render (request,'contact.html')
    else:
        return render (request,'contact.html')

def elements(request):
    return render (request,'elements.html')


def register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        try:
            uid=Register.objects.get(email=email)
            if uid.email==email:
                con={
                    "msg":"already exists"
                    }
                return render(request, 'register.html', con) 
        except:
            if password == confirm_password:
                Register.objects.create(
                    name=name, 
                    email=email, 
                    password=password
                )
                con={
                    "msg":"Register succsessfully"
                    }
                return render (request, "login.html", con)
            else:
                con={
                    "msg": "password dosen't match"
                    }
                return render(request, 'register.html',con)
    else:
        return render(request, 'register.html')


def login(request): 
    if "email" in request.session:
        return render(request, 'index.html', {"msg": "you are already logd in!"})
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            uid = Register.objects.get(email=email)
            if uid.email == email:
                request.session['email']=uid.email
                if uid.password == password:
                    return redirect('index') 
                else:
                    return render(request, 'login.html', {"msg": "Incorrect password."})
            else:
                return redirect('login')
        except Register.DoesNotExist:
            return render(request, 'login.html', {"msg": "Email not registered."})
    return render(request, 'login.html')  


def logout(request):
    if "email" in request.session:
        del request.session['email']
    request.session.flush()
    return render (request,'login.html')


import random
from django.core.mail import send_mail
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        otp = random.randint(1000, 9999)
        try:
            user = Register.objects.get(email=email)
            user.otp = otp
            user.save()
            send_mail(
                "OTP Verification",
                f"Your OTP is: {otp}",
                'meghmakvana7@gmail.com',
                [email],)
            return render(request, "confirm_password.html", {"email": email})
        except :
            er = {"msg":"This Email is not registere"}
            return render(request, "forgot_password.html",er)
    return render (request, 'forgot_password.html')


def confirm_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        try:
            uid=Register.objects.get(email=email)
            if uid.otp==otp:
                if new_password == confirm_password:
                    uid.password=new_password
                    uid.save()               
                    return redirect("login")
                else:
                    con={"msg":"password dosen't match"}
                    return render(request, 'confirm_password.html', con)
            else:
                con={"msg":"wrong otp"}
                return render(request, 'confirm_password.html', con)
        except Register.DoesNotExist:
            con = {"msg":"This Email is not registere"}   
            return render(request, 'register.html', con)
    else:
        con ={"msg":"else part runing"}            
        return render (request, 'confirm_password.html',con)





def single_blog(request):
    return render (request,'single_blog.html')

def tracking(request):
    return render (request,'tracking.html')

