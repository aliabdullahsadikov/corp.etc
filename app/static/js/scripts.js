(function($){

	'use strict';

    /**
     * Table Of Content
     * 
     *  1. [Preloader]          					- Loading Page
     *  2. [Navigation Menu]						- Header Menu
     *  3. [Navigation Menu]						- Burger Menu
     *  4. [Navigation] - Sticky Menu               - Header Menu
	 *  5. [Header] - Ticker News                   - HEader Menu
     *
     */
    
    //1. [Preloader]          - Loading Page
	NProgress.start();
	NProgress.done();

	$(document).ready(function () {
		// 2. [Navigation Menu] - Header Menu
		$('.navbar-menu .dropdown-menu .dropdown-toggle').on('click', function(e) {
			if (!$(this).next().hasClass('show')) {
				$(this).parents('.navbar-menu .dropdown-menu').first().find('.show').removeClass("show");
			}
			$(this).next(".navbar-menu .dropdown-menu").toggleClass('show');
			return false;
		});
		// For product mega menu
		$('.navbar-menu .megamenu-heading').click(function(){
			if (!$(this).next().hasClass('active')) {
				$('.navbar-menu .megamenu-dropdown-list').removeClass('active');
				$(this).next().addClass('active');
			}
			else if ($(this).next().hasClass('active')) {
				$(this).next().removeClass('active');
			}
			return false;
		});
		$('.navbar-menu .carousel-control-prev ,.navbar-menu .carousel-control-next').click(function(e){
			e.preventDefault();
			$(this).parent().parents('.dropdown-menu').addClass('active')
		});
		// For Search
        $('#section-search').on('click','.navigation-search .ns-close .close', function () {
            $('#section-search').addClass('close-search');
        });
        $('.navbar-search').on('click','img', function () {
            $('#section-search').removeClass('close-search');
        });

		// 3. [Navigation Menu]	- Burger Menu
		$('.navbar-menu #sidebarCollapse').on('click', function () {
            $('.navbar-menu .collapse.in').toggleClass('in');
            // Change icon collapse
            $(this).toggleClass('active');
        });

        // 4. [Navigation] - Sticky Menu
		var s = $("nav.navbar-menu");
		var pos = s.position();					   
		$(window).on( 'scroll',function() {
			var windowpos = $(window).scrollTop();
			if (windowpos >= pos.top) {
				s.addClass("sticky-menu");
			} else {
				s.removeClass("sticky-menu");	
			}
		});
		
		// 5. [Header] - Ticker News
		if ( $('.ticker-content').length ) {
			$('.ticker-content').newsTicker({
				row_height: 48,
			    max_rows: 1,
			    speed: 600,
			    direction: 'up',
			    duration: 2000,
			    autostart: 1,
			    pauseOnHover: 0
			});
		}

		// 6. Scroll To Top
		$('.ft_backtotop').on( 'click',function () {
	        $("html, body").animate({
	            scrollTop: 0
	        }, 600);
	        return false;
	    });

	    // 7. Carousel
	    if( $('.block-style-21 .owl-carousel').length ){
		    $('.block-style-21 .owl-carousel').owlCarousel({
			    loop:true,
			    margin:0,
			    nav:true,
			    dots:0,
			    responsive:{
			        0:{
			            items:1
			        },
			        600:{
			            items:1
			        },
			        1000:{
			            items:1
			        }
			    }
			});
		}

		// 8. Carousel
	    if( $('.block-style-23 .owl-carousel').length ){
		    $('.block-style-23 .owl-carousel').owlCarousel({
			    loop:true,
			    margin:0,
			    nav:true,
			    responsive:{
			        0:{
			            items:1
			        },
			        600:{
			            items:1
			        },
			        1000:{
			            items:1
			        }
			    }
			});
		}

		// 9. Carousel
	    if( $('.block-style-25 .owl-carousel').length ){
		    $('.block-style-25 .owl-carousel').owlCarousel({
			    loop:true,
			    margin:90,
			    nav:false,
			    responsive:{
			        0:{
			            items:1
			        },
			        768:{
			            items:2
			        },
			        1000:{
			            items:3
			        }
			    }
			});
		}

		// 10.Comments Reply
		$('.block-style-31').on('click','.content-wrapper .answers .see-answer', function(){
			$('.block-style-31 .content-wrapper .answers').toggleClass('hide show');
		});

    });

})(jQuery);
        
   