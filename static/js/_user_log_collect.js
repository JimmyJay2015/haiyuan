$(function(){
    $("#tUserLogCollect").tmpl().appendTo(".content");
    
    //分页
    $("#collect_task_table").Pagination({
        'pagerName': 'collect_task_pagination',
        'mode': 'url',
        'dataCount': count, //后台获取总条数
        'viewCount': num_per_page, //配置每页显示
        'listCount': 6,            //默认模板此值不能小于5
        'urlbase':url_base,
        'enableFirst':false,
        'currentPage':current_page,
        'selectClass': 'selectno',
    });
    
    $(".reCollect").click(function(){
        var id = $(this).attr("data-id");
        alert("任务 ID："+id);
    });
});

function startCollect(){
    var start_time = $("#log_start_time").val();
    var end_time = $("#log_end_time").val()
    
    if ( !checkTime(start_time, end_time)  ){
        setAlert(1,"日期格式不正确");
        return;
    }
    
    $.ajax({
        type : "POST",
        'url' : start_collect,
        'data' : {
            'username' : username,
            'start_time':start_time,
            'end_time':end_time
        },
        'success' : function(e) {
            if (e.return_code == 0) {
                setAlert(e.return_code, e.description);
                setTimeout("location.reload(true);", 1000);
            }else {
                setAlert(e.return_code, "操作异常:"+e.description);   
            }
            
        },
        'error' : ajaxExceptionAlert,
        'dataType' : 'json',
    });
}

function checkTime(start_time, end_time){
    if (start_time.length <= 0 || end_time.length <= 0){
        return false;
    }
    return true;
}
function translateStatus( statusValue ){
    statusValue = statusValue.toLowerCase() 
    var displayTxt = '未知';
    switch(statusValue){
    case 'ready':
        displayTxt = '未开始';
        break;
    case 'start':
        displayTxt = '等待上传';
        break;
    case 'stop':
        displayTxt = '已完成';
        break;
    }
    return displayTxt;
}




