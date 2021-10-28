var checkbox=document.getElementsByClassName('filter-checkbox');
checked=[];
for(var i=0;i<checkbox.length;i++){
    checkbox[i].addEventListener('change',function(){
    if (this.checked) {
       checked.push(this.value);
    }
    else {
        var index = checked.indexOf(this.value);
        if (index > -1) {
            checked.splice(index, 1);
        }
    }
    });
}

$(document).on("click","#filterbtn",function(){
    var body=JSON.stringify({'checked':checked});
    $.ajax({
        url:'/store/filter/',
        type:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
            //csrftoken code updated in base_layout.html
        },
        data: JSON.stringify({'checked':checked}),
        success:function(data){
            $('#filter-sel').html(data);
        }
    });
});

$(document).on("click","#search-item",function(){
    var item = $('#item').val();
    $.ajax({
        url:'/store/search/',
        type:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
            //csrftoken code updated in base_layout.html
        },
        data: JSON.stringify({'item':item}),
        success:function(data){
            $('#filter-sel').html(data);
        }
    });
});
