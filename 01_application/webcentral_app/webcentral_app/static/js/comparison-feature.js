
function comparisonButtonHandeling(){
    comparisonBar.style.display='';
    firstCompareButton.style.display='none';
    var inputs = document.getElementsByClassName('comparisonInput');
    for (let i = 0; i < inputs.length; i++) {
        inputs[i].style.visibility="visible";
    }
}

// define the behaviour of the checkbox input
$(document).ready(function () {
    // Card Multi Select
    $('input[type=checkbox]').click(function () {
      if ($(this).parent().hasClass('comparison-active')) {
        $(this).parent().removeClass('comparison-active');
        var storedNames = JSON.parse(sessionStorage.getItem("ids")).replace($(this).parent().attr('id')+',','')
        sessionStorage.setItem("ids", JSON.stringify(storedNames));
      }
      else
      { 
        
        $(this).parent().addClass('comparison-active');
        if (sessionStorage.ids != null){
            var storedNames = JSON.parse(sessionStorage.getItem("ids")) + $(this).parent().attr('id')+',';
        }
        else{  
            var storedNames= $(this).parent().attr('id')+',';
        }
        sessionStorage.setItem("ids", JSON.stringify(storedNames));
      }
      console.log(sessionStorage.ids);
    });
});

// Handling the comparison based on the session storage
$(document).ready(function () {
    let data = sessionStorage.getItem("comparison");
    let values = JSON.parse(sessionStorage.ids).slice(0,-1);
    // if session storage variable comparison is True, then the comparison should be carried over to new page
    if (data=="True"){
        comparisonButtonHandeling();
    }
    var ids = values.split(",");
    for (let i = 0; i < ids.length; i++) {
        try {

        var comparisonBar = document.getElementById(ids[i]);
        var inputNode =comparisonBar.getElementsByClassName('comparisonInput')[0];
        comparisonBar.classList.add("comparison-active");
        inputNode.checked=true;
        }
        catch(e){
            continue
        }
    }
});



  // functions that describe the behaviour of the 3 buttons that control the comparison feature
var firstCompareButton = document.getElementById('comparisonButton');
var comparisonBar = document.getElementById('comparisonBar');
firstCompareButton.addEventListener('click', function () {
    comparisonButtonHandeling();
    sessionStorage.setItem("comparison", "True");
})

var secondCompareButton = document.getElementById('compareButton');
secondCompareButton.addEventListener('click', function (event) {
    var url =document.getElementById('comparisonUrl');
    href="/TechnicalStandards/comparison/";
    ids=JSON.parse(sessionStorage.ids);
    if (ids.length <3){
        event.preventDefault()
        alert("Please select at least 2 items !!")
    }
    else{
        href+=ids;
        url.href=href.slice(0,-1);
    }
})
  
var cancelButton = document.getElementById('cancelButton');
cancelButton.addEventListener('click', function () {
    var inputs = document.getElementsByClassName('comparisonInput');
    for (let i = 0; i < inputs.length; i++) {
        inputs[i].style.visibility="hidden";
    }
    firstCompareButton.style.display='';
    comparisonBar.style.display='none';
    $('input[type=checkbox]').prop('checked', false);
    var elements=document.getElementsByClassName('comparison-active');
    while (elements.length) {    
        elements[0].classList.remove('comparison-active'); 
    }
    sessionStorage.clear();    
})