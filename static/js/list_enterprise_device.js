
//初始化
$(function(){
	$("#tDeviceTable").tmpl().appendTo( ".content" );
		
	//设置分页	 
	$("#device_table").Pagination({
		'pagerName': 'device_pagination',
		'mode': 'url',
		'dataCount': count, //后台获取总条数
		'viewCount': num_per_page, //配置每页显示
		'listCount': 6,                 //默认模板此值不能小于5
		'urlbase':url_base,
		'enableFirst':false,
		'currentPage':current_page,
		'selectClass': 'selectno',
	});
	
	//删除
	$(".delete").click(function() {
		var id = $(this).attr("data-mid");
		
		if (confirm("是否确定删除？")) {

			$.ajax({
				type : "POST",
				'url' : delete_device_url,
				'data' : {
					'device_id' : id,
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
				'dataType' : 'json',
			});
		}
	});
	
});

