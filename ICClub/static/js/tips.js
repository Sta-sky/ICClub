// var citys = [{provence_name:'四川省',pid:1,city:[{city_name:'成都市',cid:101,
//             area:[{area_name:'高新区',aid:1001},{area_name:'金牛区',aid:1002},
//                 {area_name:'锦江区',aid:1003},{area_name:'武侯区',aid:1004},{
//                 area_name:'青羊区',aid:1005},{area_name:'成华区',aid:1006},{
//                 area_name:'龙泉驿区',aid:1007},{area_name:'温江区',aid:1008},{
//                 area_name:'新都区',aid:1009},{area_name:'郫都区',aid:1010},{
//                 area_name:'青白江区',aid:1011},{area_name:'天府新区',aid:1012},
//                 {area_name:'双流区',aid:1013}]}]}];


$("#act_intro").blur(function () {
    if (!this.value) {
        $(this).text('请输入活动标题');
        $(this).css('color', 'red');
        return false;
    }
});


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

// 生成随机标签
function make_label() {
    var nums = getRandByParm(LOCALLABELLIST.length, 8);
    var mes = ''
    var label_list = []
    $.each(nums, function (index, num) {
        num = Number(num)
        label_list.push(LOCALLABELLIST[num])
    })

    $.each(label_list, function (index, val) {
        tit_url = 'label.html?sub=' + val
        mes += '<li><a' + ' href=' + tit_url + '>' + val + '</a></li>'
    })

    $('#lab').html(mes)
}

// 获取标签 生成随机标签
function get_label(state) {
    if (!state) {
        // 未登录 从静态文件取随机标签
        make_label()
    } else {
        token = window.localStorage.getItem('user_token')
        $.ajax({
            type: 'POST',
            headers: {'Authorization': token},
            contentType: 'application/json',
            url: SER_URL + 'label',
            success: function (response) {
                if (response.code === 200) {
                    var data = response.data
                    var mes = ''
                    $.each(data, function (index, val) {
                        tit_url = 'label.html?sub=' + val
                        mes += '<li><a' + ' href=' + tit_url + '>' + val + '</a></li>'
                    })
                    $('#lab').html(mes)
                } else {
                    get_label(false)
                }
            }
        })
    }
}

// 换一换标签触发器
$('#lab_btn').on('click', function () {
    var loginName = window.localStorage.getItem('user_name');
    get_label(loginName)
})

$('#lab_btn').click()

