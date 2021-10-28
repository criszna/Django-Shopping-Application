from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import json
import datetime
from .models import *
from .utils import cartdata,guestorder

# Create your views here.
def store(request):
    data=cartdata(request)

    cartitems=data['cartitems']

    main_categories=MainCategory.objects.all()
    products=Product.objects.all()
    main_cat_filter={}
    for main_category in main_categories:
        category=Category.objects.filter(main_category=main_category)
        main_cat_filter[main_category.main_category]=category

    context={'products':products,'cartitems':cartitems,'shipping':False,'main_cat_filter':main_cat_filter}
    return render(request,'store.html',context)

def cart(request):
    data=cartdata(request)

    cartitems=data['cartitems']
    order=data['order']
    items=data['items']

    context={'items':items,'order':order,'cartitems':cartitems}
    return render(request,'cart.html',context)

def checkout(request):
    data=cartdata(request)

    cartitems=data['cartitems']
    order=data['order']
    items=data['items']

    context={'items':items,'order':order,'cartitems':cartitems}
    return render(request,'checkout.html',context)

def updateitem(request):
    data=json.loads(request.body)
    productid=data['productid']
    action=data['action']
    customer=request.user.customer
    product=Product.objects.get(id=productid)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action=="add":
        orderitem.quantity=orderitem.quantity+1
    elif action=="remove":
        orderitem.quantity=orderitem.quantity-1
    orderitem.save()
    if orderitem.quantity<=0:
        orderitem.delete()
    return JsonResponse('item added',safe=False)

def processorder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        customer=request.user.customer
        order = Order.objects.get(customer=customer,complete=False)
    else:
        order,customer=guestorder(request,data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    return JsonResponse('paymwnt completed', safe=False)

def searchitem(request):
    jsondata = json.loads(request.body)
    item = jsondata['item']
    products=[]
    try:
        category = Category.objects.get(sub_category__iexact=item)
        product = Product.objects.filter(category=category)
        for each in product:
            products.append(each)
    except:
        pass

    if len(products)==0:
        try:
            main_category = MainCategory.objects.get(main_category__iexact=item)
            main_categories = Category.objects.filter(main_category=main_category)
            for sub_category in main_categories:
                product = Product.objects.filter(category=sub_category)
                for each in product:
                    products.append(each)
        except:
            pass

    if len(products)==0:
        product = Product.objects.filter(name__iexact=item)
        for each in product:
            products.append(each)

    if len(products)==0:
        return HttpResponse('<img id="no_product" src="/media/no_product.jpg">')

    context = {'products': products}
    return render(request, 'filter.html', context)

def filteritem(request):

    jsondata = json.loads(request.body)
    checked = jsondata['checked']
    products=[]

    if len(checked)>0:
        for category in checked:
            category=Category.objects.get(sub_category=category)
            product=Product.objects.filter(category=category)
            for each in product:
                products.append(each)
    else:
        products = Product.objects.all()

    context = {'products': products}
    return render(request, 'filter.html', context)

def detailitem(request,id):
    data = cartdata(request)

    cartitems = data['cartitems']
    product = Product.objects.get(id=id)
    context={'product':product,'cartitems':cartitems}
    return render(request, 'detail.html', context)

