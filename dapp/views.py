from django.shortcuts import render, redirect
from django.http import HttpResponse # import
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Item, CartItem




def cart_view(request):
    if request.method == "GET":
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        context = {}
        context["cart_items"] = cart_items
        return render(request, "cart.html", context)
    if request.method == "POST":
        item_name = request.POST.get("item_name") # get value from post
        item_qty = request.POST.get("item_qty") # get value from post

        item = Item.objects.get(name=item_name) # create item instance
        user=request.user # get logined uesr instance

        CartItem.objects.create(user=user, item=item, quantity=item_qty)

        return redirect("/cart/")


def item_view(request):
    if request.method == "GET":
        items = Item.objects.all()
        context = {}
        context["items"] = items
        return render(request, "item.html", context)

def index_view(request):
    return HttpResponse("Hello, world!")

@login_required(login_url="/login/")
def hello_view(request):
    get_name = request.GET.get('getname') # to get user input via get
    login_user = request.user # logined user
    items = Item.objects.all() #from .models import Item

    context = {}
    context["login_user"] = login_user
    context["get_name"] = get_name # return value to template
    context["items"] = items
    return render(request, "hello.html", context)

def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/hello/")
        else:
            return HttpResponse("Invalid login details given.")
