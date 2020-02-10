var id = getUrlParam('act_id');
var data = {'act_id': id};
var token = window.localStorage.getItem('user_token');

//获取每月的天数
function getMonthDays(year,month) {
    var thisDate = new Date(year, month,0); //当天数为0 js自动处理为上一月的最后一天
    return thisDate.getDate();
}


// 页面初始化加载活动数据
$.ajax({
    type: 'POST',
    url: SER_URL + 'active/detail',
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify(data),
    success: function (result) {
        if (result.code === 200) {
            begtime = result.starttime;
            $('#title').text(result.subject);
            $('#nr').text(result.content);
            $('#like').text(result.like);
            var res = '';

            var year = Number(begtime.split('-')[0]);
            var month = Number(begtime.split('-')[1]);
            date = Number(begtime.split("-")[2]);
            var  day = getMonthDays(year,month);

            // alert(date);
            for (var i = 0; i < 5; i++) {

                if (date<day){
                    date +=1;
                }else {
                    var date = 0;
                    month +=1;
                    if (month > 12) {
                        month = 0;
                        month += 1;
                        year += 1;
                    }
                    date +=1;
                }
                begtime = year+'-'+month+'-'+date;
                res += '<li>' + begtime + '</li>'
            }
            $('#opt').html(res)
        } else {
            alert('服务器繁忙!')
        }
    }
});


//    收藏单击事件
function changeVal(statu) {
    var data = ''
    if (statu === 'collection') {
        var nowstatus = $('#sc').text()
        data = {'collection': nowstatus, 'actid': id}
    } else {
        data = {'actid': id}
    }
    $.ajax({
        type: 'POST',
        headers: {
            'Authorization': token
        },
        url: SER_URL + 'label/' + statu,
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (result) {
            if (result.code === 200) {
                if (statu === 'collection') {
                    if (nowstatus === "收藏") {
                        $('#sc').text("已收藏");
                    } else {
                        $('#sc').text("收藏")
                    }
                } else {
                    $('#like').text(result.data)
                }
            }
        },
        error: function () {
            alert('服务器繁忙!')
        }
    })
}


// 收藏点击
$('#sc').on('click', function () {
    if (token){}else {return}
    changeVal('collection')
})

// 点赞点击
$('#clicklike').on('click', function () {
    changeVal('like')
})

//显示投票框
$('#fbtn').on('click', function () {
    $('#tuo').removeAttr('style')
})

// 返回
$('#btn_qx').on('click', function () {
    $('#tuo').attr('style', 'display:none')
})

// 移除样式
function rmclass() {
    $.each($('#opt>li'), function (index, ele) {
        $(ele).removeClass('hover')
    })
}

// 选择日期
$('#opt').on('click','li', function () {
    rmclass()
    $(this).addClass('hover')
})

// 免责申明
$('#jr').on('click', function () {
    $('#mz').removeAttr('style')
})

// 退出免责申明
$('#mz').on('click', function () {
    $('#mz').attr('style', 'display:none')
})

// ==============留言开始===================
// 留言按钮
// $('#send').on('click', function () {
//     // alert('此功能暂未开放')
//     // return
// //    console.log(11111111111111111)
//    var comment_text = $('#ly').val();
//    var data={'comment_text':comment_text};
//    console.log(comment_text);
//    console.log(act_id)
//    $.ajax({
//     //    data: comment_text,
//        type: 'post',
//        dataType: 'json',
//        headers: {'Authorization': token},
//        url: SER_URL + 'v1/comment/act?act_id=' + act_id,
//        contentType: 'application/json;charset=UTF-8',
//        data: JSON.stringify(data),
//        success: function (response) {
//            if (response.code == 201) {
//                console.log(222222222222)
//                alert('评论成功')
               
//            }else{
//                alert(response.data)
//            }
//        },
//        error: function (err) {
//         console.log('网页渲染错误')
//         console.log(err)
//     }
//    })
// });
// ==============留言结束===================

// ==============回复开始===================
// 点击回复，弹出回复下拉框
//页面加载完毕后开始执行的事件
// $(function(){
    // $(".review-btn").on('click',function(){
    //     var review_id=$(this).attr('review_id');
    //     alert(review_id)
    //     $(".review-textarea").remove();
    //     $(this).parent().append("<div class='review-textarea'><textarea name='review_text' cols='40' rows='5'></textarea><br/><input type='submit' value='发表' /></div>");
    // });
// });

// ==============回复结束==================

// // 虚化背景
// var dj = document.getElementById('dj');
// var boxx = document.getElementById('box2_act');
//
// dj.onclick = function () {
//     boxx.style.opacity = 0.2;
// }
//
//
// // 恢复正常
// var r = document.getElementById('hid');
// var boxx = document.getElementById('box2_act');
// r.onclick = function () {
//     boxx.style.opacity = 1
// }

// var chak = $("#read");
// $("#hid").on('click', function () {
//     if ($(chak).is(":checked")) {
//         return true
//     } else {
//         alert('请阅读"免责声明"并勾选')
//     }
// });

// 提交
$('#btn_qd').on('click', function () {
    if (token){}else {alert('请先登录');return}
    var result = $('.hover').text();
    var id = getUrlParam('act_id');
    alert(result);
    if (result) {
    } else {
        alert('您还没有投票')
    }
    $.ajax({
        type: 'GET',
        headers: {
            'Authorization': token
        },
        url: SER_URL + 'label/' + id + '?&date=' + result,
        success: function (result) {
            if (result.code === 200) {
                alert('投票成功')
            } else {
                alert('服务器繁忙!  敬请期待')
            }
        },
        error: function () {
            alert('服务器繁忙！')
        }
    });
});
