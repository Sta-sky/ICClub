$('#sub').click(function () {    //获取 ajax  异步发送信息    var username = $('#username').val();    var password = $('#passwd').val();    var code = $('#code').val();    var phone = $('#phone').val();    //生成  json对象    data = {'username': username, 'password': password, 'code': code, 'phone': phone};    var token = window.localStorage.getItem('user_token');    //    判断 username 密码 规则    if (username !== '' && password !== '' && code !== '') {        $.ajax({            type: 'POST',            //HTTP_AUTHORIZATION            headers: {                'Authorization': token            },            url: SER_URL + 'user/login',            dataType: 'json',            contentType: 'application/json;charset=utf8',            data: JSON.stringify(data),            success: function (result) {                if (result.code === 200) {                    //将数据存储到本地 存储                    window.localStorage.clear();                    window.localStorage.setItem('user_name', result.username);                    window.localStorage.setItem('user_id', result.id);                    window.localStorage.setItem('user_token', result.token);                    //新页面打开url地址                    //在当前页面打开指定的url页面                    window.location.href = 'index.html';                } else {                    alert(result.message)                }            }        })    } else {        alert('登录信息不能为空')    }});//页面跳转$('#h1').click(function () {    window.location.href = STIC_URL + 'login.html'});$('#h2').click(function () {    window.location.href = STIC_URL + 'regist.html'});//短信发送$('#but').click(function () {    var phone = $('#phone').val();    var username = $('#username').val();    var phone_number = {'phone_number': phone, 'username': username};    if (phone === 0 || !(/^1[34578]{1}\d{9}$/).test(phone) || username === '') {        alert('手机格式有误请核对')    } else {        //设置时间倒计时        time($('#but'));        $.ajax({            type: 'post',            url: SER_URL + 'user/send_sms',            dataType: 'json',            data: JSON.stringify(phone_number),            success: function (result) {                if (result.code === 200) {                    alert('短信已发送')                } else {                    alert(result.message)                }            }        })    }});// 检测地址是否在服务区function myFun(result) {    var cityName = result.name;    if (cityName !== '成都市') {//        alert('系统检测到您当前地址不在服务区内,相关活动将会有所限制')    }//     alert('欢迎使用')}var myCity = new BMap.LocalCity();myCity.get(myFun);$('#passwd_forget').click(function () {    $.ajax({        type:'GET',        url:SER_URL+'user/find_passwd',        success:function (result) {            if (result.code === 200){                alert(result.message);                window.location.href = STIC_URL +'find_passwd.html'            } else {                alert(result.message)            }        }    })});