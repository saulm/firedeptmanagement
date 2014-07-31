$(document).ready(function () {
    $(".moreinfo").hide();
    
    $(".preview").click(function () {
        var id = $(this).attr("id").split("_")[1];
        $("#moreinfo_"+id).slideToggle("slow");
    });
});
