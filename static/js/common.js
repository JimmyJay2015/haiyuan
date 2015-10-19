//删除右边的空格
var rtrim = function (str){  
 return str.replace(/(\s*$)/g,"");
}

function displayBoolean (value){
	   if (value == 0)
	       return "否";
	   return "是";
};

function displayStringBoolean (value){
	   if (value.toLowerCase() == "false")
	       return "否";
	   return "是";
};

function displaySexBoolean (value){	
	if ((value) == 0)
	       return "未透露";
	else if((value) == 1)
		return "男";
	else if((value) = 2)
		return "女";
	return "未知";
};

function displayStatusBoolean (value){
	if(value == "1")
		return "发布";
	return "未发布";
};

function displayOrderStatus(value){
	var displayTxt = '未知';
	switch(value){
	case '0':
		displayTxt = '未完成';
		break;
	case '1':
		displayTxt = '已取消';
		break;
	case '3':
		displayTxt = '已完成';
		break;
	}
	return displayTxt;
}



function displayStringArrayAbbr(vegetables, maxlength){
	//默认20个字符
	if(!maxlength)
		maxlength = 20;
	var value = vegetables.join(",");
	if (value.length>maxlength)
		value = value.substr(0, maxlength-2)+"..";
	return value;
}

function countStrByte(e) {
	var n = function(e) {
        return e.charCodeAt()
    };
	var r = function (e) {
	    return e.toString(16).length / 2;
	};
    var t = 0, i, s = 0;
    while (i = e[t++])
        s += r(n(i));
    return s
}

function formatDate(e, t) {
    var n = e.getFullYear(), r = "0" + (e.getMonth() + 1);
    r = r.substring(r.length - 2);
    var i = "0" + e.getDate();
    i = i.substring(i.length - 2);
    var s = "0" + e.getHours();
    s = s.substring(s.length - 2);
    var o = "0" + e.getMinutes();
    return o = o.substring(o.length - 2), t.replace("yyyy", n).replace("MM", r).replace("dd", i).replace("hh", s).replace("mm", o)
}


//set alert 
function setAlert(returnCode, description, delay)
{
	var alert_tmpl = '<div id="acp-alert"><div class="alert in alert-block fade  ${type}">\
		<a class="close" data-dismiss="alert">×</a><strong>${description}</strong></div></div>';
	$.template('tAlert', alert_tmpl);
	
	$('#acp-alert').empty();
	
	if(returnCode==0)
	{
		var type = 'alert-success';
	}
	else
	{
		var type = 'alert-error';
	}
	
	$.tmpl('tAlert', {'type':type, 'description':description}).prependTo('div.container:first');
	$('#acp-alert.alert').alert();
	
	//滚屏到最上方
	window.scrollTo(0,0);
	
	//自动消失
	if(returnCode==0){
		if(delay==null){
			delay = 3000;
		}		
	}
	else{
		if(delay==null){
			delay = 10000;
		}		
	}
	setTimeout("$('#acp-alert').empty();", delay);
}
var ajaxExceptionAlert = function(xhr) {
	setAlert(1, "发送异常，请稍后重试");
};

function alertDialog(description, handler){
	var msg_tmpl = '<div id="alert_dialog" title="错误" style="display:none">\
		<p><strong>${description}</strong></p>\
		</div>';
	$.template('tAlertDialog', msg_tmpl);
	$('#alert_dialog').remove();
	$.tmpl('tAlertDialog', {'description':description}).appendTo('body');
	$('#alert_dialog').dialog({		      
	      modal: true,
	      buttons: {
	        "确定": function() {	        		        	
	        	handler();
	        },	        
	      },
	      close: function() {		        
	    	  handler();		        
	      }
	    });
	
}

function displayTime(timestamp, format_str){	
	//也支持"yy-M-d h:m:s"格式
	if(format_str===undefined)
		format_str="yyyy-MM-dd hh:mm:ss";
	
	var date = new Date(timestamp);
	
	var z ={y:date.getFullYear(), 
			M:date.getMonth()+1, 
			d:date.getDate(), 
			h:date.getHours(), 
			m:date.getMinutes(), 
			s:date.getSeconds()
			};
    return format_str.replace(/(y+|M+|d+|h+|m+|s+)/g, 
    		function(item) {
    	//补零和截断处理
    	return ((item.length>1?"0":"")+eval('z.'+item.slice(-1))).slice(-(item.length>2?item.length:2));
    	});
}


//字符串拼接函数
String.format = function(src){
		    if (arguments.length == 0) return null;
		    var args = Array.prototype.slice.call(arguments, 1);
		    return src.replace(/\{(\d+)\}/g, function(m, i){
        return args[i];
    });
};


function showUePopMsg(msg)
{
	var pop_tmpl = '<div class="popup" id="pop_msg">\
		<div class="popup-header">${msg}</div>\
		<div class="btn-group" style="position:absolute;left:50%;margin-left:-55px;bottom:10px">\
		<button class="btn" id="pop_close_btn">关闭</button>\
		</div>\
		</div>';
	$.template('tPopMsg', pop_tmpl);
	
	$('#pop_msg').empty();
	
	$.tmpl('tPopMsg', {'msg':msg}).appendTo('body');
	
	$('#pop_close_btn').click(function(){
		$("#pop_msg").remove();
		});
	setTimeout(function() {
		$("#pop_msg").remove();
    }, 4000);
}

function displayDeviceInterfaceType (value){
	var displayTxt = '未知';
	switch(value){
	case 'TF':
		displayTxt = 'TF';
		break;
	case 'USB':
		displayTxt = 'USB';
		break;
	case 'BLUETOOTH':
		displayTxt = '蓝牙';
		break;		
	}
	
	return displayTxt;
};

