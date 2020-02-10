

// 请求最新活动数据
function request_data(state) {
    $.ajax({
        type: 'GET',
        contentType: 'application/json',
        url: SER_URL + 'active/'+state,
        success: function (response) {
            if (response.code == 200) {
                var data = response.data
                var res = ''
                $.each(data, function (index, val) {
                    res += '<div id="new_act_" act_id="' + val.id + '">'
                    res += '<img src="' + val.imgurl + '" alt="">'
                    res += '<div id="new_content">'
                    res += '<div id="n_tit"><h3>' + val.title + '</h3></div>'
                    res += '<div id="n_cont"><p>' + val.content + '</p></div>'
                    res += '<div id="n_lt">'
                    res += '<div id="n_lab">' + val.label + '</div>'
                    res += '<div id="n_time">' + val.date + '</div>'
                    res += '</div></div></div>'
                })
                $('#new_act_').html(res)
            }
        }
    })
}

// 触发跳转到活动详情页
$('#new_act_>img,#new_content>#n_tit,#new_content>#n_cont').on('click',function () {
    var act_id = $(this).attr('act_id')
    window.location.herf = 'active.html?act_id=' + act_id
})

// 最新活动点击事件
$('#z_new_act').on('click',function () {
        request_data('new')
    })

// 模拟点击最新活动
$('#z_new_act').click()

// 历史活动点击事件
$('#z_his_act').on('click',function () {
    request_data('history')
})

//    ---------------------
