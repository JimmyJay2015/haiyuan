//初始化
$(function(){   
    $("#tAddUser").tmpl().appendTo(".content");
    
    $("#user_add_submit").click(function(){
        var new_user = {};
        
        //用户名
        new_user.username = $.trim($("#user_username").val());
        var valid_username = parseInt(new_user.username).toString();
        if( valid_username.length != new_user.username.length || valid_username.length != 11 ){
            setAlert(1, "用户名不合法");
            return;
        }
        
        //昵称
        new_user.name = $.trim($("#user_name").val());
        // TODO 检验非法字符
        
        //密码
        var user_password_1 = $.trim($("#user_password_1").val());
        var user_password_2 = $.trim($("#user_password_2").val());
        if ( user_password_1.length < 6 ){
            setAlert(1, "密码长度不能小于6");
            return;
        }else if ( user_password_1 != user_password_2 ){
            setAlert(1, "2次输入的密码不一致");
            return;
        }
        new_user.password = user_password_1;
        
        //性别
        new_user.sex = $("#user_sex").val();
        
        $.ajax({
            type : "POST",
            'url' : addUserUrl,
            'data' : {
                'user' : $.toJSON(new_user),
            },          
            'success' : function(e) {
                if (e.return_code == 0) {
                    setAlert(e.return_code, "添加成功");
                    setTimeout("window.location.href=showUserUrl;", 1000);
                } else {                    
                    setAlert(e.return_code, "添加失败:"+e.description);
                }
            },
            'error' : ajaxExceptionAlert,
            'dataType' : 'json',
        });
    })
});