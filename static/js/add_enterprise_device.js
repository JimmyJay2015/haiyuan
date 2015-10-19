//初始化
$(function(){	
	$("#tDeviceEdit").tmpl().appendTo(".content");
	
	$( "#publishtime" ).datepicker({ dateFormat: "yy-mm-dd" });
	
	$("#save").click(function(t) {
		var device = {};
		
		device.device_serial_no = $.trim($("#device_serial_no").val());
		if(device.device_serial_no.length>50 || device.device_serial_no.length==0){
        	setAlert(1, "设备ID不能为空且长度不能超过50字");        	
        	return;
        }
		
		device.device_type = $.trim($("#device_type").val());
		if(device.device_type.length>50 || device.device_type.length==0){
        	setAlert(1, "设备类型不能为空且长度不能超过50字");        	
        	return;
        }
		
		device.interface_type = $("#interface_type").val();
		
		device.publishtime = $.trim($("#publishtime").val());
		
		if(device.publishtime.length>0){
			device.publishtime = Date.parse(device.publishtime);
			if(isNaN(device.publishtime)){
				setAlert(1, "出厂日期格式不正确");        	
	        	return;
			}
			else{
				device.publishtime = device.publishtime/1000;
			}
		}
		else{
			device.publishtime = 0;
		}
		
        $.ajax({
			type : "POST",
			'url' : saveUrl,
			'data' : {				
				'device' : $.toJSON(device),				
			},			
			'success' : function(e) {
				if (e.return_code == 0) {
					setAlert(e.return_code, "操作成功");
										
					setTimeout("window.location.href=showUrl;", 1000);
					
				} else {					
					setAlert(e.return_code, "操作失败:"+e.description);
				}
			},
			'error' : ajaxExceptionAlert,
			'dataType' : 'json',
		});
	});
	
	
});