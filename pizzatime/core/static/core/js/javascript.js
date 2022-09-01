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

// $(".mainMenu").on("click", function() {
//     $(".pageMenu").children().toggleClass("grey").attr("id", "couldntGreen")
// })

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