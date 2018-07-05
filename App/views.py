from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from App.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, UserModel
from App.viewhelper import get_user

ALL_TYPE = "0"

TOTAL_RULE = "0"

PRICE_UP = "1"

PRICE_DOWN = "2"


def home(request):
    wheels = MainWheel.objects.all()

    navs = MainNav.objects.all()

    mustbuys = MainMustBuy.objects.all()

    shops = MainShop.objects.all()

    shop0 = shops[0:1]

    shop1_3 = shops[1:3]

    shop3_7 = shops[3:7]

    shop7_11 = shops[7:11]

    mainshows = MainShow.objects.all()

    data = {
        "title": "首页",
        "wheels": wheels,
        "navs": navs,
        "mustbuys": mustbuys,
        "shop0": shop0,
        "shop1_3": shop1_3,
        "shop3_7": shop3_7,
        "shop7_11": shop7_11,
        "mainshows": mainshows
    }

    return render(request, 'home/home.html', context=data)


def market(request):
    return redirect(reverse("axf:marketWithParams", kwargs={"typeid": "104749", "cid": "0", "sort_rule": "0"}))


def marketWithParams(request, typeid, cid, sort_rule):
    foodtypes = FoodType.objects.all()

    if cid == ALL_TYPE:
        goodsList = Goods.objects.filter(categoryid=typeid)
    else:
        goodsList = Goods.objects.filter(categoryid=typeid).filter(childcid=cid)

    """
        全部分类:0#进口水果:110#国产水果:120

        全部分类，进口水果，国产水果
        数字是它名字的标识

        for in 迭代显示
            可迭代元素
        切割
            # 
        [全部分类:0, 进口水果:110, 国产水果:120]

        切割
            :
        [[全部分类, 0], [进口水果, 110], [国产水果, 120]]
    """
    foodtype = FoodType.objects.get(typeid=typeid)

    childtypenames = foodtype.childtypenames

    childtypename_list = childtypenames.split("#")

    child_type_name_list = []

    for childtypename in childtypename_list:
        child_type_name_list.append(childtypename.split(":"))

    print(child_type_name_list)

    """
        综合排序
            就是对筛选结果进行一个order_by

        服务器能接收对应的字段 （排序字段）
        客户端发送排序字段
            两端有一个约定
                0 综合排序
                1 价格升序
                2 价格降序
                3 ...
                4 ...
            简历
                和前端定制接口字段
    """
    if sort_rule == TOTAL_RULE:
        pass
    elif sort_rule == PRICE_UP:
        goodsList = goodsList.order_by("price")
    elif sort_rule == PRICE_DOWN:
        goodsList = goodsList.order_by("-price")

    data = {
        "title": "闪购",
        "foodtypes": foodtypes,
        "goodsList": goodsList,
        "typeid": int(typeid),
        "child_type_name_list": child_type_name_list,
        "cid": cid,
        "sort_rule": sort_rule,
    }

    return render(request, 'market/market.html', context=data)


def cart(request):
    data = {
        "title": "购物车"
    }

    return render(request, 'cart/cart.html', context=data)


def mine(request):
    user_id = request.session.get('user_id')

    data = {
        "title": "我的",
        "is_login": False
    }

    if user_id:
        user = UserModel.objects.get(pk=user_id)
        data['is_login'] = True
        data["username"] = user.u_name
        data["icon"] = "/static/upload/" + user.u_icon.url

    return render(request, 'mine/mine.html', context=data)


def add_to_cart(request):
    print(request.GET)
    return JsonResponse({"msg": "ok"})


class UserRegisterView(View):

    def get(self, request):
        return render(request, 'user/user_register.html')

    def post(self, request):
        u_username = request.POST.get("u_username")

        u_email = request.POST.get("u_email")

        u_password = request.POST.get("u_password")

        u_icon = request.FILES.get("u_icon")

        user = UserModel()

        user.u_name = u_username

        user.set_password(u_password)

        user.u_email = u_email

        user.u_icon = u_icon

        user.save()

        request.session["user_id"] = user.id

        response = redirect(reverse("axf:mine"))

        return response


class UserLoginView(TemplateView):
    template_name = 'user/user_login.html'

    def post(self, request):

        username = request.POST.get("u_username")

        password = request.POST.get("u_password")

        user = get_user(username)

        if user:
            if user.check_password(password):
                # 用户名和密码都对了，跳转到个人中心
                request.session['user_id'] = user.id
                return redirect(reverse("axf:mine"))
            else:
                # 密码错误
                redirect(reverse("axf:user_login"))
        #    用户名不存在
        return redirect(reverse("axf:user_login"))


def logout(request):
    # session cookie 一起清除
    request.session.flush()

    return redirect(reverse('axf:mine'))


def check_user(request):
    username = request.GET.get("username")

    user = get_user(username)

    data = {
        "msg": '<span style="color: green">用户名可用</span>'
    }

    if user:
        data["status"] = "901"
        data["msg"] = '<span style="color: red">用户名已存在</span>'
    else:
        data["status"] = "200"
    return JsonResponse(data)
