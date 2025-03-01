// $(".dragable-list").owlCarosel({
//     autoplay:true,
//     slideSpeed:3000,
//     items:3,
//     nav:true,
//     navText:['<i class="fa-solid fa-arrow-left"></i>', '<i class="fa-solid fa-arrow-right"></i>'],
//     margin:30,
//     dots:false,
//     responsive:{
//         320:{
//             items:1
//         },
//         767:{
//             items:2
//         },
//         600:{
//             items:3
//         },
//         1000:{
//             items:3
//         }
//     }
// });


$(document).ready(function(){
    $(".owl-carousel").owlCarousel({
    autoplay:false,
    slideSpeed:3000,
    items:5,
    nav:false,
    rtl:true,
    // navText:['<i class="fa-solid fa-arrow-left"></i>', '<i class="fa-solid fa-arrow-right"></i>'],
    margin:10,
    loop:false,
    dots:true,
    responsive:{
        320:{
            items:1
        },
        600:{
            items:2
        },
        767:{
            items:3
        },
        1000:{
            items:5
        }
    }
    });
});