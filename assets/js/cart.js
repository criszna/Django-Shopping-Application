$(document).on("click",".update-cart",function(){
    var productid=$(this).attr("data-product");
    var action=$(this).attr("data-action");
    console.log('USER',user)
    if(user=='AnonymousUser'){
         addCookieItem(productid,action)
    }
    else{
         UpdateUserOrder(productid,action)
    }
});

function addCookieItem(productid,action){
    console.log('user is not authenticated')
    if(action=='add'){
        if(cart[productid]==undefined){
            cart[productid]={'quantity':1}
        }
        else{
            cart[productid]['quantity']+=1
        }
    }
    if(action=='remove'){
        cart[productid]['quantity']-=1
        if(cart[productid]['quantity']<=0){
            delete cart[productid]
        }
    }
    console.log('cart',cart)
    document.cookie='cart='+JSON.stringify(cart)+";domain=;path=/";
    location.reload()
}

function UpdateUserOrder(productid,action){
    console.log('user is authenticated and sending data...')
    fetch('/store/updateitem/',{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
            //csrftoken code updated in base_layout.html
        },
        body: JSON.stringify({'productid':productid,'action':action})
    })
    .then((response)=>{
        return response.json();
    })
    .then((data)=>{
        console.log('data',data)
        location.reload()
    })
}
