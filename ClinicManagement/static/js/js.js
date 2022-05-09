function confirmForm(e){
    if (!confirm("Xác nhận đăng kí?"))
        e.preventDefault();
}


function FirstLoad(){
    if(localStorage.getItem("first") == null){
        var localDate = new Date();
        localStorage.setItem("date", localDate);
        localStorage.setItem("first","done");
    }
    setDate();
}

function getDateList(){
    var start = document.querySelector('input[name="date"]');
    var date = new Date(start.value);
    var d = date.getDate();
    var m = date.getMonth()+1;
    var y = date.getFullYear();
    if(d<10){
      d='0'+dd;
    }
    if(m<10){
      m='0'+m;
    }
    var date2 = y+'-'+m+'-'+d;
    document.getElementById("date").value = date2;
    fetch('/update_list');
}

function getDateList2(){
    var start = document.querySelector('input[name="date-exam"]');
    var date = new Date(start.value);
    var d = date.getDate();
    var m = date.getMonth()+1;
    var y = date.getFullYear();
    if(d<10){
      d='0'+dd;
    }
    if(m<10){
      m='0'+m;
    }
    var date2 = y+'-'+m+'-'+d;
    document.getElementById("date").value = date2;
    fetch('/update_patient_list');
}

function getCurrentDate(int){
    var today = new Date();
    var d = today.getDate();
    var m = today.getMonth()+1;
    var y= today.getFullYear();
    if(d<10){
      d='0'+dd;
    }
    if(m<10){
      m='0'+m;
    }
    if (int !=0){
        var m_max = today.getMonth()+2;
        if(m_max<10){
            m_max='0'+m_max;
        }
        today = y+'-'+m_max+'-'+d;
        return today;}
    today = y+'-'+m+'-'+d;
    return today;
}

function getDateMM(){
    var today = getCurrentDate(0);
    document.getElementById("date").value = today;
    document.getElementById("date").setAttribute("min", today);
    document.getElementById("date").setAttribute("max", getCurrentDate(1));
}

function getDate(){
    document.getElementById("date").value = getCurrentDate(0);
}

function saveDate(){
    var start = document.querySelector('input[name="date-exam"]');
    var date = new Date(start.value);
    localStorage.setItem("date", date);
}

function setDate(){
    var date1 = new Date(localStorage.getItem("date"));
    var d = date1.getDate();
    var m = date1.getMonth()+1;
    var y = date1.getFullYear();
    if(d<10){
      d='0'+d
    }
    if(m<10){
      m='0'+m
    }
    var date2 = y+'-'+m+'-'+d;
    document.getElementById("date-exam").value = date2;
    getDateList();
}










































































window.globalCounter = 1;

