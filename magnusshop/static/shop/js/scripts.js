// navbar section
document.addEventListener("DOMContentLoaded", function() {
    var dropdown = document.getElementById('categoryDropdown');
    var dropdownMenu = dropdown.nextElementSibling;
    var subcategoryLists = document.querySelectorAll('.subcategory-list');

    dropdown.addEventListener('mouseenter', function() {
        dropdownMenu.classList.add('show');
    });

    dropdown.addEventListener('mouseleave', function() {
        dropdownMenu.classList.remove('show');
    });

    dropdownMenu.addEventListener('mouseenter', function() {
        this.classList.add('show');
    });

    dropdownMenu.addEventListener('mouseleave', function() {
        this.classList.remove('show');
    });

    var parentItems = dropdownMenu.querySelectorAll('.dropdown-submenu > a');
    parentItems.forEach(function(item) {
        item.addEventListener('mouseenter', function() {
            var categoryId = this.closest('.dropdown-submenu').getAttribute('data-category-id');
            subcategoryLists.forEach(function(list) {
                if (list.getAttribute('data-category-id') === categoryId) {
                    list.classList.add('show');
                } else {
                    list.classList.remove('show');
                }
            });
        });
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const userDropdown = document.getElementById('userDropdown');
    const dropdownMenu = document.querySelector('.user-dropdown .dropdown-menu');

    // بستن dropdown با کلیک خارج از آن
    document.addEventListener('click', function (event) {
        if (!userDropdown.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.classList.remove('show');
        }
    });

    // باز کردن dropdown با کلیک روی دکمه
    userDropdown.addEventListener('click', function (event) {
        event.stopPropagation(); // جلوگیری از بسته شدن فوری منو
        dropdownMenu.classList.toggle('show');
    });
});








let slideIndex = 1;
let remainingTime = 70000;

function setTime(){
    if(remainingTime==0) return;
    let h = Math.floor(remainingTime/3600);
    let m = Math.floor(remainingTime%3600/60);
    let s = (remainingTime%3600)%60;
    document.querySelector('#hrs').innerHTML = h
    document.querySelector('#mins').innerHTML = m
    document.querySelector('#secs').innerHTML = s
}

setInterval(()=>{
    remainingTime -=1;
    setTime()
} , 1000)

function setSlide(input, index){
    slideIndex = index;
    let item = document.querySelector(`#${input}`);
    let slides = [...document.querySelector('.slides').children];
    slides.forEach((element)=>{
        element.classList.remove('active');
    })
    item.classList.add('active');
}

setInterval(()=>{
    slideIndex +=1;
    if(slideIndex==6){
        slideIndex=1;
    }
    setSlide(`slide${slideIndex}`, slideIndex)

}, 4500)


// $(document).ready(function(){
    $(".owl-carousel").owlCarousel({
        // autoplay:false,
        // slideSpeed:3000,
        // items:5,
        nav:true,
        navText:['<i class="fa-solid fa-arrow-left"></i>', '<i class="fa-solid fa-arrow-right"></i>'],
        margin:10,
        dots:true,
        rtl:false,
        loop:true,
        responsive:{
            320:{
                items:1
            },
            600:{
                items:2
            },
            767:{
                items:4
            },
            1000:{
                items:5
            }
        }
    });
    // });