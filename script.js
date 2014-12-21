$(document).ready(function(){
    
    var offSet = 0;
    var prevScroll = 0;
    
    $.localScroll({
            duration: 300,
            easing: "linear",
            offset: -93
    });
    
     //Sticky Header
    $(window).scroll(function() {

        if ($(window).scrollTop() > 350) {
            $('.top-nav').addClass('sticky');
        } else {
            $('.top-nav').removeClass('sticky');
            
        }
        
        if ($('.top-nav').hasClass('sticky')){
            $.localScroll({
                duration: 300,
                easing: "linear",
                offset: -54
            });
        } else {
            $.localScroll({
                duration: 300,
                easing: "linear",
                offset: -93
            });    
        }
    });
    
    $('#nav-icon4').click(function(){
		$(this).toggleClass('open');
        $('.container').toggleClass('open');
        $('.top.nav').addClass('sticky');
	});
    
    $('a').click(function(){
        $('#nav-icon4').removeClass('open');
        $('.container').removeClass('open');              
    })
//    var prevScroll = 0;
//    $(window).scroll(function() {
//        if ($(window).scrollTop() > 350) {
//            var currScroll = $(this).scrollTop();
////            alert(currScroll);
//            if (currScroll < prevScroll){
//                $('.top-nav').addClass('sticky');
////                alert('up');
//            } else {
//                $('.top-nav').removeClass('sticky');
//            } 
//        } else {
//            $('.top-nav').removeClass('sticky');
//        }
//        prevScroll = currScroll;
//    });

});