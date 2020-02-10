
    // 获取数字 最大值+多少个数+字符串是否加0+是否是向上取整
    function getRandByParm(max, len, blnz = false, blnt = false) {
        var _arr = [];
        while (_arr.length < len) {
            if (!blnt) {
                var n = Math.floor(Math.random() * max)
            } else {
                var n = Math.ceil(Math.random() * max)
            }
            if (n < max && blnz) {
                n = '0' + n
            }
            var reg = new RegExp(n, 'g');
            if (!reg.test(_arr.toString())) {
                _arr.push(n)
            }
        }
        return _arr
    }


    //封装方法 获取url中 参数=name的值
    function getUrlParam(name) {
            var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
            var r = window.location.search.substr(1).match(reg); //匹配目标参数
            if (r != null) return unescape(r[2]);
            return null; //返回参数值
            }