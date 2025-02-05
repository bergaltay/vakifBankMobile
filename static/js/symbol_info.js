function price_info_toggleBtn(){
    const x = document.getElementById("price-info-toggleBtn")
        if (x.classList.contains("fa-caret-down")){
            x.classList.remove("fa-caret-down")
            x.classList.add("fa-caret-up")
        }else{
            x.classList.remove("fa-caret-up")
            x.classList.add("fa-caret-down")
        }
        $("#price-info").animate({
          height: 'toggle'
        });
}
function stock_info_toggleBtn(){
    const x = document.getElementById("stock-info-toggleBtn")
    if (x.classList.contains("fa-caret-down")){
        x.classList.remove("fa-caret-down")
        x.classList.add("fa-caret-up")
    }else{
        x.classList.remove("fa-caret-up")
        x.classList.add("fa-caret-down")
    }
    $("#stock-info").animate({
    height: 'toggle'
    });
}