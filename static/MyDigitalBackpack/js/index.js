$(document).ready(function(){

var third = $(window).height() / 3;
    $('.third').css({"height":third+"px"});

	 $(window).resize(function(){
        var third = $(window).height() / 3;
    $('.third').css({"height":third+"px"});
    });

var halfHeight = $(".formHalf").height() / 2 - 85;
    $('.or').css({"top":halfHeight+"px"});

	 $(window).resize(function(){
        var halfHeight = $(".formHalf").height() / 2 - 85;
    $('.or').css({"top":halfHeight+"px"});
    });

var halfWidth = $(".whiteHeader").width() / 2 - 50;
    $('.or').css({"left":halfWidth+"px"});

	 $(window).resize(function(){
        var halfWidth = $(".whiteHeader").width() / 2 - 50;
    $('.or').css({"left":halfWidth+"px"});
    });

var taskScroller = $(".confirmMain").height() - 260;
    $('.taskScroll').css({"height":taskScroller+"px"});

	 $(window).resize(function(){
        var taskScroller = $(".confirmMain").height() - 260;
    $('.taskScroll').css({"height":taskScroller+"px"});
    });

var width = $(".table").width();
    $('.addNewEvent').css({"width":width+"px"});

	 $(window).resize(function(){
        var width = $(".table").width();
    $('.addNewEvent').css({"width":width+"px"});
    });

});
