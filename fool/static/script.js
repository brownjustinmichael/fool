$(document).ready (function () {
    $("select+a.add-another").each(function(){
        $(this).after("&nbsp;<a class='changelink' href='#'>Edit</a>");
        $(this).next().click(function(){
            var link = ($(this).prev().attr('href').replace (/add.+/,"")+$(this).prev().prev().val ());
            var win = window.open(link + '?_popup=1', link, 'height=600,width=1000,resizable=yes,scrollbars=yes');
            win.focus();
            return false;
        });
    });
});
