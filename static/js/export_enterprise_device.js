//初始化
$(function(){   
    $("#tDeviceEdit").tmpl().appendTo(".content");
    
    //设置标签页

    
    //设置分页   
    $("#device_table").Pagination({
        'pagerName': 'export_file_pagination',
        'mode': 'url',
        'dataCount': count, //后台获取总条数
        'viewCount': num_per_page, //配置每页显示
        'listCount': 6,            //默认模板此值不能小于5
        'urlbase':url_base,
        'enableFirst':false,
        'currentPage':current_page,
        'selectClass': 'selectno',
    });
    
    
    
    //删除
    $(".delete").click(function() {
        var filename = $(this).attr("data-filename");
        
        if (confirm("是否确定删除？")) {
            $.ajax({
                type : "POST",
                'url' : deleteExportfileUrl,
                'data' : {
                    'filename' : filename
                },
                'success' : function(e) {
                    if (e.return_code == 0) {
                        setAlert(e.return_code, "删除成功");
                        setTimeout("location.reload(true);", 1000);
                    } else {
                        setAlert(e.return_code, "删除失败:"+e.description);
                    }
                },
                'error' : ajaxExceptionAlert,
            });
        }
    });
     
});


function exportDevice(){
    showBlock("正在导出数据");
    $.ajax({
        type : "POST",
        'url' : exportUrl,
        'success' : function(e) {
            if (e.return_code == 0) {
                unBlock();
                var url = window.location.origin+exportfilePath+e.exportFileName;
                location.href = url;
                setTimeout("location.reload(true);", 100);
            }else{
                unBlock();
                setTimeout("showBlock('导出失败');", 100);
                setTimeout(unBlock, 1500);
            }
        },
        'error' : function(){
            unBlock();            
            setTimeout("showBlock('导出失败');", 200);
            setTimeout(unBlock, 1500);
        },
    });
}

function showBlock(msg){
    var prompt_css =  { 
            'font-size' : '22px',
            'height' : '30px',
            'padding-top': '15px',
            'color': 'rgb(58, 135, 173)',
            'background-color': 'rgb(217, 237, 247)',
            'border-color':'rgb(188, 232, 241)', 
            'border': '2px', 
            'fadeOut': '100',
            'border-radius':'10px',
            'box-shadow': '10px 10px 5px #888888',
            'font-weight':'bold'
        }

    $.blockUI({ message : msg , css: prompt_css, overlayCSS: { backgroundColor: '#cccccc', opacity:'0.6' }}); 
}
function unBlock(){
    $.unblockUI();
}



