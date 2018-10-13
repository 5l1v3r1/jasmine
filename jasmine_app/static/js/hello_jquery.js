
    $(document).ready(function () {

    $("#button_p").click(function () {
        $("h1").text("hello jquery");
        $("p").append("fjl");
        $("#w3s").attr("href", function (i, originvalue) {
            return originvalue;
        })
    });
    $(".add_css").click(function () {
        $("p").remove();
    });
    $("#add_css").click(function () {
        $("h1,p").addClass("blue");
    });
});