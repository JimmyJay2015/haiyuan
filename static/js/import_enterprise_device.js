//初始化
$(function(){
    
    $("#tDeviceEdit").tmpl().appendTo(".content");
    
    if ( catalog_type == "info" ) {
        showImportResult();
    }else{
        showImportTask();
    }
    //执行导入
    $(".exec_import").click(function(){
        var task_name = $(this).attr("data-taskname");
        
        if (confirm("是否确定导入数据？")) {
            $.ajax({
                type : "POST",
                'url' : exec_import_url,
                'data' : {
                    'task_name' : task_name
                },
                'success' : function(e) {
                    if (e.return_code == 0) {
                        setTimeout("location.reload(true);", 100);
                    } else {
                        setAlert(e.return_code, "执行失败:"+e.description);
                        setTimeout("location.reload(true);", 2000);
                    }
                },
                'error' : ajaxExceptionAlert,
            });
        }
    })
    
    //删除任务
    $(".delete_task").click(function(){
        if (confirm("是否删除任务？")) {
            delet_task_or_info( $(this).attr("data-taskname"),  "task")
        }
    })
    
    //删除记录
    $(".delete_info").click(function(){
        if (confirm("是否确定删除记录？")) {
            delet_task_or_info( $(this).attr("data-taskname"),  "info")
        }
    })
    
});

function showImportTask(){
    $("#import_result_li").removeClass("active");
    $("#import_task_li").addClass("active");
    $("#Import_Info").remove();
    
    $("#tImport_Task").tmpl().appendTo("#import_task_content");
    
    $("#tImport_Task_item").tmpl(data_list).appendTo("#Import_Task_Body");
    
    //设置分页
    $("#import_task_table").Pagination({
        'pagerName': 'import_task_pagination',
        'mode': 'url',
        'dataCount': count, //后台获取总条数
        'viewCount': num_per_page, //配置每页显示
        'listCount': 6,            //默认模板此值不能小于5
        'urlbase':task_base_url,
        'enableFirst':false,
        'currentPage':current_page,
        'selectClass': 'selectno',
    });
    setTimeout(loadUploadButton, 1000);
}
function loadUploadButton(){
    $("#file_upload").uploadify({
        'auto'          : true,
        'height'        : 32,
        //'multi'         : false,
        'buttonClass'   : 'btnGrayU',
        'buttonText'    : '上传',
        'swf'           : '/static/res/uploadify/uploadify.swf',
        'uploader'      : '/oss/enterprise_device/import_upload_file',
        'width'         : 142,
        'fileObjName'   : 'Filedata',
        'fileTypeExts'  : '*.csv;',
        'method'        : 'post',
        'queueSizeLimit': 1,
        'onSelectError' : function(file, errorCode, errorMsg){
            switch(errorCode) {
                case -100:
                    alert("上传的文件数量已经超出系统限制的"+$('#file_upload').uploadify('settings','queueSizeLimit')+"个文件！");
                    break;
                case -110:
                    alert("文件 ["+file.name+"] 大小超出系统限制的"+$('#file_upload').uploadify('settings','fileSizeLimit')+"大小！");
                    break;
                case -120:
                    alert("文件 ["+file.name+"] 大小异常！");
                    break;
                case -130:
                    alert("文件 ["+file.name+"] 类型不正确！");
                    break;
            }
        },
        'onUploadSuccess':function(file, data, response){
            if(response == true ){
                var return_code = JSON.parse(data); 
                if (return_code['return_code'] != 0){
                    alert(return_code['description'])
                    return;
                }
                filename = file.name;
                if(filename == ''){
                    setAlert(1, "没有上传文件");
                    return;
                }
                setTimeout("location.reload(true);", 300);
            }
            else{
                alert(response);
                return;
            }
        }
    });
}

function showImportResult(){
    $("#import_task_li").removeClass("active");
    $("#import_result_li").addClass("active");
    $("#Import_Task").remove();
    
    $("#tImport_Info").tmpl().appendTo("#import_task_content");
    
    
    $("#tImport_Info_Item").tmpl(data_list).appendTo("#Import_Info_Body");
    //设置分页   
    $("#import_info_table").Pagination({
        'pagerName': 'import_info_pagination',
        'mode': 'url',
        'dataCount': count, //后台获取总条数
        'viewCount': num_per_page, //配置每页显示
        'listCount': 6,            //默认模板此值不能小于5
        'urlbase':info_base_url,
        'enableFirst':false,
        'currentPage':current_page,
        'selectClass': 'selectno',
    });
}


function delet_task_or_info( task_name, delete_type ){
    $.ajax({
        type : "POST",
        'url' : delete_task_url,
        'data' : {
            'task_name' : task_name,
            'delete_type': delete_type
        },
        'success' : function(e) {
            if (e.return_code == 0) {
                setTimeout("location.reload(true);", 100);
            } else {
                setAlert(e.return_code, "删除失败:"+e.description);
                setTimeout("location.reload(true);", 2000);
            }
        },
        'error' : ajaxExceptionAlert,
    });
}









