// 重载页面
$('#quxiao').on('click', function () {
    window.location.reload(false)
})

// 提交页面
$('#add_act').on('click', function () {
    var token = window.localStorage.getItem('user_token');

    if (token !== '') {
        console.log('提交中')
    } else {
        alert('请先登录');
        window.location.href = 'login11111.html';
        return;
    }
    // var money = $('#money').val()
    // var area = $('#area').val()
    var kind = $('#kind').val()
    if (kind === '请选择') {
        alert('请选择活动主题');
        return;
    }
    var title = $('#title').val()
    var actintro = $('#act_intros').val()
    var starttime = $('#start-time').val()
    var endtime = $('#end-time').val()
    var addr = $('#addr').val()
    var condition = $('#condition').val()
    var file = document.getElementById('myfile').files[0];
    if (endtime < starttime) {
        alert('结束时间不能在开始时间之后');
        return
    }
    date = new Date()
    var year = starttime.split('-')[0]
    var mou = starttime.split('-')[1]
    var day = starttime.split('-')[2]
    // console.log(mou)
    // console.log(day)
    if (date.getFullYear() > year || date.getMonth() > mou) {
        alert('本平台不支持穿越活动');
        return;
    }
    if (date.getDate() + 2 > day) {
        alert('时间有点仓促，请至少提前两天发布活动')
        return;
    }
    if (isNaN(Number(condition))) {
        alert('请输入正确的数字格式')
        return;
    }
    console.log(11111111111111111111111)
    var img = ''
    var data = {
        'kind': kind,
        'title': title,
        'content': actintro,
        'addr': addr,
        'condition': condition,
        'starttime': starttime,
        'endtime': endtime,
        'img': img,
         }

    function request() {
        $.ajax({
            data: JSON.stringify(data),
            enctype: 'multipart/form-data',
            headers: {'Authorization': token},
            type: 'POST',
            contentType: 'application/json',
            url: SER_URL + 'active/create',
            success: function (response) {
                if (response.code === 200) {
                    window.location.href = 'activity.html?act_id=' + response.actid
                } else {
                    console.log(response.message)
                    alert('服务器繁忙,请稍后再试~')
                }
            },
            error: function () {
                alert('服务器在开小差，请稍后重试!')
            }
        });
    }

    if (file) {
        let reads = new FileReader();
        reads.readAsDataURL(file);
        reads.onload = function (e) {
            img = reads.result
            request()
        }
    } else {
        request()
    }
});

$.ajax({
    type: 'GET',
    contentType: 'application/json',
    url: SER_URL + 'label/option',
    success: function (response) {
        var data = response.data
        res = ''
        res += '<option>请选择</option>'
        $.each(data, function (index, val) {
            res += '<option>' + val + '</option>'
        })
        $('#kind').html(res)
    }
})

