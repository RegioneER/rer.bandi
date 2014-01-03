$(document).ready(function(){
    if (! ($("input#use_solr").is(':checked'))) {
        $(".siteSelection").hide();
    }
    $("input#use_solr").change(function(event) {
        if ($(this).is(':checked')) {
            $(".siteSelection").slideDown();
        }
        else {$(".siteSelection").slideUp();}
    });
});
