$(document).ready(function (){
    $(".form-login").submit(function(){
        account_name = $("#account_name").val();
        password = $("#password").val();
    })
    // 表单数据存放到对象data中
    var data = {
        account_name: account_name,
        password: password
    };
    // 将data转化为json字符串
    var jsonData = JSON.stringify(data);
    $.ajax({
        url: "/session",    // 上传到服务器后要改成绝对路径（加上域名）
        type: "post",
        data: jsonData,
        contentType: "application/json",
        dataType: "json",
        success: function (data){
            if (data.errno == "0"){
                // 登陆成功，跳转到后台管理页面
                location.href = '/admin';
            }
            else{
                // 登录错误
                location.href = '/login'
            }
        }
    });
})