
function stocks_div_toggleBtn(){
    const x = document.getElementById("stocks-div-toggleBtn")
          if (x.classList.contains("fa-caret-down")){
              x.classList.remove("fa-caret-down")
              x.classList.add("fa-caret-up")
          }else{
              x.classList.remove("fa-caret-up")
              x.classList.add("fa-caret-down")
          }
        $("#stocks-div").animate({
          height: 'toggle'
        });
}function funds_div_toggleBtn(){
    const x = document.getElementById("funds-div-toggleBtn")
    if (x.classList.contains("fa-caret-down")){
        x.classList.remove("fa-caret-down")
        x.classList.add("fa-caret-up")
    }else{
        x.classList.remove("fa-caret-up")
        x.classList.add("fa-caret-down")
    }
  $("#funds-div").animate({
    height: 'toggle'
  });
}
var pageUrl = window.location.href;
const urlList = pageUrl.split("/");
var date = urlList[urlList.length-1].split("#")[0];
console.error(date);
document.getElementById(date).classList.add("active");
var lastColumnIndex = $('#data-table').find('th').length - 1;
$('#data-table').DataTable({
    paging: false,
    scrollY: '400px',
    searching: true,
    info: true,
    pageLength: 10,
    lengthMenu: [5, 10, 25, 50, 100],
    ordering: true,
    order: [[lastColumnIndex, 'des']],
    language: {
        info: "_TOTAL_ veri gösteriliyor",
        search: "Ara:",
        lengthMenu: "Display _MENU_ records per page"
    }
});

$('#new-data-table').DataTable({
    paging: false,
    scrollY: '400px',
    searching: true,
    info: true,
    pageLength: 10,
    lengthMenu: [5, 10, 25, 50, 100],
    ordering: true,
    language: {
        info: "_TOTAL_ veri gösteriliyor",
        search: "Ara:",
        lengthMenu: "Display _MENU_ records per page"
    }
});
