$(function () {
    $(".confirm").click(function () {
        var $confirm = $(this)

        var cartid = $confirm.parents("div").attr("cartid")

        console.log(cartid)

        $.getJSON("/axf/changecartstatus/", {"cartid": cartid}, function (data) {

            console.log(data);

            if (data["status"] == "200") {
                if (data["is_select"]) {
                    $confirm.find("span").find("span").html("√")
                    $("#total_price").html(data["total_price"])

                    // 全选按钮可能变成选中

                    if (data["all_select"]) {
                        $(".all_select span span").html("√")
                        $("#total_price").html(data["total_price"])

                    }

                } else {
                    $confirm.find("span").find("span").html("")
                    // 全选按钮需要变成未选中
                    $(".all_select span span").html("")
                    $("#total_price").html(data["total_price"])


                }
            }

        })
    })

    $(".all_select").click(function () {

        var select_list = [];

        var un_select_list = [];

        $(".menuList").each(function () {

            var $menuList = $(this);

            var cartid = $menuList.attr("cartid");

            var content = $menuList.find(".confirm span span").html();

            if (content.trim().length) {

                select_list.push(cartid)

            } else {
                un_select_list.push(cartid)
            }

        });

        console.log(select_list);
        console.log(un_select_list);

        if (un_select_list.length) {
            $.getJSON("/axf/changecartliststatus/", {
                "action": "select",
                "cartList": un_select_list.join('#')
            }, function (data) {

                console.log(data);

                if (data["status"] == "200") {
                    $(".confirm span span").html("√");
                    $(".all_select span span").html("√")
                    $("#total_price").html(data["total_price"])

                }

            })
        } else {

            $.getJSON("/axf/changecartliststatus/", {
                "action": "unselect",
                "cartList": select_list.join('#')
            }, function (data) {

                console.log(data)

                if (data["status"] == "200") {
                    $(".confirm span span").html("");
                    $(".all_select span span").html("")
                    $("#total_price").html(data["total_price"])

                }
            })
        }

    })


    $(".subShopping").click(function () {

        var $subShopping = $(this)

        var cartid = $subShopping.parents(".menuList").attr('cartid');

        console.log(cartid)

        $.getJSON("/axf/subtocart/", {"cartid": cartid}, function (data) {

            console.log(data);

            if (data["status"] == "200") {

                if (data["c_goods_num"] > 0) {
                    $subShopping.next("span").html(data['c_goods_num']);
                } else {
                    $subShopping.parents(".menuList").remove();
                }
                $("#total_price").html(data["total_price"])
            }
        })
    });


    $(".addShopping").click(function () {

        var $addShopping = $(this);

        var cartid = $addShopping.parents(".menuList").attr('cartid');

        console.log(cartid);

        $.getJSON("/axf/addtocart/", {"cartid": cartid}, function (data) {

            console.log(data);

            if (data["status"] == "200") {
                $addShopping.prev("span").html(data['c_goods_num']);
                $("#total_price").html(data["total_price"])
            }
        })
    });
})