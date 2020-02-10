//  定义一个创建异步请求对象的函数
function create_xhr() {
// 定义一个异步对象 初始值为空
    var xhr = null;
    if (window.XMLHttpRequest) {
        //实例化最新的异步对象
        xhr = new XMLHttpRequest();

    } else {
        //实例化一个ActiveXObject对象
        xhr = new ActiveXObject('Microsoft.XMLHttp');

    }
    //返回创建xhr对象
    return xhr
}
// 定义一个根据请求数据发送异步请求的函数
function send_ajax(method, data, url, tip) {
    //创建异步请求对象
    var xhr = create_xhr();
    //开启一个请求
    xhr.open(method, url, true);
    //绑定监测状态和获取返回数据的事件
    xhr.onreadystatechange = function () {
        //如果请求正确发送到服务器,且服务器返回数据
        if (xhr.readyState == 4 && xhr.status == 200) {
            //获取服务器返回的数据
            tip.innerText = xhr.responseText;
        }
    };
    // 如果是POST方式
    if (method=='POST'){
        // 重置发送内容的类型
        xhr.setRequestHeader('Content-Type','application/x-www-form-urlencoded')
    }
    //开始发送
    xhr.send(data);
}