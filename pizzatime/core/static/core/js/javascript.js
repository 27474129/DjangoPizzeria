"use strict"

/* ------- */
const url = "http://127.0.0.1:8000/"

if (location.href == url || location.href == url + "?form=reg") {
    $(".pageMenu").children().addClass("grey")
    $(".pageMenu").children().attr("id", "couldntGreen").css("cursor", "unset")
}
/* ------ */



$(".log_in-form").toggleClass("none")

$(".log_in-Btn").click(function() {
    $(".log_in-form").fadeIn()
    $(".log_in-Btn span").css("color", "grey").css("background", "#fff")
})

$(".log_in-IconCross").click(function() {
    $(".log_in-form").fadeOut()
    $(".log_in-Btn span").css("color", "").css("background", "")
})



$(".mainMenu").click(function() {
    $(".centering").toggleClass("none")
    $(".log_in-form").fadeOut("fast")
    $(".log_in-Btn span").css("color", "").css("background", "")
})





/* массив для наполнения классов, которые не будут выделяться */

const unselectedArray = [".burgerChaptersInner a, .burgerChaptersInner a", ".log_in-Btn span", ".log_in-IconCross", ".mainMenu"]
for (var i = 0; i < unselectedArray.length; i++) {
    $(unselectedArray[i]).addClass("unselect")
}



if (location.href == url + "?form=reg") {
    $(".centering").toggleClass("none")
    $(".log_in-form").fadeIn()
    $(".log_in-Btn span").css("color", "grey").css("background", "#fff")
}



/* add to busket */

$(".mainProduct button").each(function(i, elem) {
    $(elem).parent().attr("id", "product_" + i)
    $(elem).attr("onclick", "add_to_basket($(this))")
})

function add_to_basket(attr) {
    const inst = "#" + attr.parent().attr("id")
    $(inst).children("div").clone().appendTo(".products-in-basket")
}