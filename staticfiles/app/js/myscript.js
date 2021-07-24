$('#slider1, #slider2, #slider3, #slider4',).owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 2,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 6,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$(".plus-cart").click(function(){
    var id = $(this).attr("pid").toString();
    var ele = this.parentNode.children[2]
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            pro_id: id
        },
        success: function(data){
            ele.innerText = data.quantity
            document.getElementById("amount").innerText =  data.amount
            document.getElementById("total_amount").innerText = data.total_amount
        }
    })
})

$(".minus-cart").click(function(){
    var id = $(this).attr("pid").toString();
    var ele = this.parentNode.children[2]
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            pro_id: id
        },
        success: function(data){
            ele.innerText = data.quantity
            document.getElementById("amount").innerText =  data.amount
            document.getElementById("total_amount").innerText = data.total_amount
        }
    })
})

$(".remove-cart").click(function(){
    var id = $(this).attr("pid").toString();
    var ele = this
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            pro_id: id
        },
        success: (data) => {
            ele.parentNode.parentNode.parentNode.parentNode.remove();
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("total_amount").innerText = data.total_amount;
        }
    })
})


