//用来初始化表格数据
function _userTableInit(){

	$("#tUserTable").tmpl().appendTo( ".content" );
	
	//设置分页	 
	$("#user_table").Pagination({
		'pagerName': 'user_pagination',
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
		var username = $(this).attr("data-username");
		
		if (confirm("是否确定删除？")) {
			$.ajax({
				type : "POST",
				'url' : delete_user_url,
				'data' : {
					'username' : username,
				},
				'success' : function(e) {
					if (e.return_code == 0) {		
						setTimeout("location.reload(true);", 100);
					} else if ( e.return_code == 131137 ) {
				        setAlert(e.return_code, "用户已删除");
				        setTimeout("location.reload(true);", 1000);
				    }
					else {
						setAlert(e.return_code, "删除失败:"+e.description);   
					}
				},
				'error' : ajaxExceptionAlert,
				'dataType' : 'json',
			});
		}
	});
	/*
	//采集日志 
	$(".collectLog").click(function(){
        var username = $(this).attr("data-username");
        var param = {'username':username};
        $('#tCollectLogSetTime').tmpl(param).appendTo("body");
        
        $("#log_collect_submit").click(function(){
            var username = $(this).attr("data-username");
            var start_time = $("#log_start_time").val();
            var end_time = $("#log_end_time").val()
            $.ajax({
                type : "POST",
                'url' : collect_log_url,
                'data' : {
                    'username' : username,
                    'start_time':start_time,
                    'end_time':end_time
                },
                'success' : function(e) {
                    if (e.return_code == 0) {       
                        setAlert(e.return_code, e.description);
                        $("#collectLogSetTime").remove();
                    }else {
                        setAlert(e.return_code, "操作异常:"+e.description);   
                    }
                    
                },
                'error' : ajaxExceptionAlert,
                'dataType' : 'json',
            });
        });
        
        $("#log_collect_cancel").click(function(){
            $("#collectLogSetTime").remove();
        });
	});
	*/
	//用户搜索
	var user_filter_dialog = null;
	
	$("#userfilter").click(function() {
		if(user_filter_dialog===null){
			$('#tUserFilterDialog').tmpl().appendTo("body");		
		
			$("#filters").multiselect({
			   noneSelectedText: "没有条件",
			   selectedText: "# 个条件",
			   checkAllText: "全选",
			   uncheckAllText: "全部取消",
			   
			   click:function(event, ui){
				   if(ui.checked){
					   $("#control_"+ui.value).removeClass("none");
					   //filterok 方便jquery的搜索
					   $("#control_"+ui.value).addClass("filterok");
				   }
				   else{
					   $("#control_"+ui.value).addClass("none");
					   $("#control_"+ui.value).removeClass("filterok");
				   }				   
			   },
			   checkAll:function(){
				   for(var index in filterFieldDefine){
					   $("#control_"+filterFieldDefine[index].key).removeClass("none");				   
					   $("#control_"+filterFieldDefine[index].key).addClass("filterok");					   
				   }
				   
			   },
			   uncheckAll:function(event, ui ){
				   for(var index in filterFieldDefine){
				   	$("#control_"+filterFieldDefine[index].key).addClass("none");				   
				   	$("#control_"+filterFieldDefine[index].key).removeClass("filterok");
				   }
			   },
			   
		});
		
		user_filter_dialog = $("#user_filter_dialog").dialog({		      
		      modal: true,
		      width:"500px",
		      buttons: {
		        "查询": function() {		        	
		        	var geturl = '/oss/user_management/search?';
		        	var has_filter = false;
		        	
		        	//获取用户名
		        	var username_filter = $("#user_filter_dialog > .filterok > .controls > #username_filter").val();		        	
		        	if(username_filter!=null){
		        		username_filter = $.trim(username_filter);
		        		if(username_filter.length>50 || username_filter.length<6){		        	
		        			setAlert(1, "名称查询长度不能小于6且不能超过50");        	
		        			return;
		        		}
		        		else{
		        			has_filter = true;
		        			geturl += "username=";
		        			geturl += username_filter;
		        			geturl += "&";
		        		}
		            }
		        	
		        	//获取昵称
		        	var name_filter = $("#user_filter_dialog > .filterok > .controls > #name_filter").val();		        	
		        	if(name_filter!=null){
		        		name_filter = $.trim(name_filter);
		        		if(name_filter.length>50 || name_filter.length==0){		        	
		        			setAlert(1, "名称不能为空且长度不能超过50字");        	
		        			return;
		        		}
		        		else{
		        			has_filter = true;
		        			geturl += "nickname=";
		        			geturl += name_filter;
		        			geturl += "&";
		        		}
		            }
		        	
		        	//获取性别
		        	var sex_filter = $("#user_filter_dialog > .filterok > .controls > #sex_filter").val();
		        	if(sex_filter!=null){		        		
		        		has_filter = true;
		        		geturl += "sex=";
		        		geturl += sex_filter;
		        		geturl += "&";		        		
		            }
		        	
		        	//获取地区
		        	var region_filter = $("#user_filter_dialog > .filterok > .controls > #region_filter").val();
		        	if(region_filter!=null){
		        		region_filter = $.trim(region_filter);
		        		if(region_filter.length>20 || region_filter.length==0){		        	
		        			setAlert(1, "地区不能为空且长度不能超过20字");        	
		        			return;
		        		}
		        		else{
		        			has_filter = true;
		        			geturl += "region=";
		        			geturl += region_filter;
		        			geturl += "&";
		        		}
		            }
		        	
		        	//获取绑定状态
		        	var binding_filter = $("#user_filter_dialog > .filterok > .controls > #binding_filter").val();
		        	if(binding_filter!=null){		        		
		        		has_filter = true;
		        		geturl += "binding=";
		        		geturl += binding_filter;
		        		geturl += "&";		        		
		            }	        	
		        	
		        	
		        	if(has_filter==false){
		        		setAlert(1, "请至少选择一个条件");
		        		return;
		        	}	        	
		        	
		        	
		        	location.href = geturl;		        			        	 
		        },
		        "取消": function() {		          	
		        	$( this ).dialog("close");
		        }
		      },
		      close: function() {
		      }
		    });
		}
		else{			
			user_filter_dialog.dialog("open");
		}
	});
}

$(function(){
	_userTableInit();
});

function cls(id){
    var obj = $("#"+id);
    obj.css("color","black");
    obj.val('');
}


