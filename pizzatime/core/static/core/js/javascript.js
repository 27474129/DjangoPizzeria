"use strict"

// $(".btn").click(function() {
//     $("body").toggleClass("darkBgc")
// })
var i = true
$(".mainMenu").click(function() {
    $(".centering").toggleClass("none")
})

$(".mainMenu").click(function() {
    if (location.href == "http://127.0.0.1:8000/html%60s/main.html#password=******") {
        $(".pageMenu").children().toggleClass("grey")
        $(".pageMenu").children().attr("id", "couldntGreen")
    }


})


