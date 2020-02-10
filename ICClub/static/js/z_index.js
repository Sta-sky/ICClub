// 生成页码
function getpage(page, pagenums) {
    res = ''
    var i = page - 4
    if (i <= 0) {
        i = 1
    }
    if (page > 1) {
        res += '<li class="page" id="firstpage">上一页</li>'
    }
    for (var j = i; j <= 10; j++) {
        if (j > pagenums) break
        // console.log(j)
        if (j == page) {
            res += '<li class="page" id="page_now">' + j + '</li>'
            continue
        }
        res += '<li class="page" >' + j + '</li>'
    }
    if (page < pagenums) {
        res += '<li class="page" id="lastpage">下一页</li>'
    }
    // console.log(res)
    $('#l_num>ul').html(res)
}


//==========================
function webrequestpage(pag) {
act_nh = 'new'

// 页面加载初始化请求第一页
    if ('WebSocket' in window) {
        ws = new WebSocket(WEBSOCKET_URL + 'active/new/'+pag)
        // ws = new WebSocket(WEBSOCKET_URL + 'active/new/1')

        ws.onopen = function () {
            // 最新活动点击事件
            $('#z_new_act').on('click', function () {
                act_nh = 'new'
                ws.close()
                webrequestpage('1')
                // ws.send(JSON.stringify({'page': '1'}))
            })
            // 模拟点击最新活动
            // $('#z_new_act').click()
        //
        //     $('#l_num>#ul').on('click', '.page', function () {
        //         if (act_nh !== 'new') {
        //             return;
        //         }
        //
        //         var page = $(this).text()
        //         var page_now = $('#page_now').text()
        //         if (page === '上一页') {
        //             page = Number(page_now) - 1
        //         }
        //         if (page === '下一页') {
        //             page = Number(page_now) + 1
        //         }
        //         if (page === page_now) {
        //             alert('您已经在当前页面')
        //             return
        //         }
        //         if (ws) {
        //             ws.close()
        //         }
        //         webrequestpage(page)
        //         // ws.send(JSON.stringify({'page': page}))
        //     })
        }


        ws.onmessage = function (mes) {

            // console.log(JSON.parse(mes.data).data)
            // 将数据转换成JSON格式
            var respon = JSON.parse(mes.data)
            if (respon.code === 200) {
                var message = respon.data
                var res = ''
                $.each(message, function (index, val) {
                    res += '<div id="new_act_">'
                    res += '<a href="activity.html?act_id=' + val.id + '">'
                    res += '<img src="' + ACTIMG_URL + val.actimg + '" alt="" act_id="' + val.id + '">'
                    res += '</a>'
                    res += '<div id="new_content">'
                    res += '<div id="n_tit" act_id="' + val.id + '">'
                    res += '<a href="activity.html?act_id=' + val.id + '">' + val.title
                    res += '</a></div>'
                    res += '<div id="n_cont" act_id="' + val.id + '">'
                    res += '<a href="activity.html?act_id=' + val.id + '"><p>' + val.content + '</p>'
                    res += '</a></div>'
                    res += '<div id="n_lt">'
                    res += '<div id="n_lab">' + val.label + '</div>'
                    res += '<div id="n_time">' + val.date + '</div>'
                    res += '</div></div></div>'
                })
                $('#b2_l2').html(res)
                var pagearr = JSON.parse(mes.data).page
                getpage(pagearr[0], pagearr[1])
            } else {
                $('#b2_l2').html('')
                getpage(1, 1)
            }
        }

        ws.onclose = function () {
            console.log('连接关闭')
        }
    }

}

webrequestpage('1')
//=======================


// --------
// function webreq({pag = '1'}) {
//
// // 页面加载初始化请求第一页
//     if ('WebSocket' in window) {
//         ws = new WebSocket(WEBSOCKET_URL + 'active/new/' + pag)
//         // ws = new WebSocket(WEBSOCKET_URL + 'active/new/1')
//
//         ws.onopen = function () {
//             // 最新活动点击事件
//             $('#z_new_act').on('click', function () {
//                 act_nh = 'new'
//                 alert(123546)
//                 // ws.send(JSON.stringify({'page': '1'}))
//                 ws.close()
//                 webreq({pag: '1'})
//             })
//             // 模拟点击最新活动
//             // $('#z_new_act').click()
//
//             $('#l_num>#ul').on('click', '.page', function () {
//                 if (act_nh !== 'new') {
//                     return;
//                 }
//                 alert(123)
//                 var page = $(this).text()
//                 var page_now = $('#page_now').text()
//                 if (page === '上一页') {
//                     page = Number(page_now) - 1
//                 }
//                 if (page === '下一页') {
//                     page = Number(page_now) + 1
//                 }
//                 if (page === page_now) {
//                     alert('您已经在当前页面')
//                     return
//                 }
//                 // -----------
//                 // ws.send(JSON.stringify({'page': page}))
//                 ws.close()
//                 webreq({pag: page})
//             })
//         }
//
//
//         ws.onmessage = function (mes) {
//
//             // console.log(JSON.parse(mes.data).data)
//             // 将数据转换成JSON格式
//             var respon = JSON.parse(mes.data)
//             if (respon.code === 200) {
//                 var message = respon.data
//                 var res = ''
//                 $.each(message, function (index, val) {
//                     res += '<div id="new_act_">'
//                     res += '<a href="activity.html?act_id=' + val.id + '">'
//                     res += '<img src="' + ACTIMG_URL + val.actimg + '" alt="" act_id="' + val.id + '">'
//                     res += '</a>'
//                     res += '<div id="new_content">'
//                     res += '<div id="n_tit" act_id="' + val.id + '">'
//                     res += '<a href="activity.html?act_id=' + val.id + '">' + val.title
//                     res += '</a></div>'
//                     res += '<div id="n_cont" act_id="' + val.id + '">'
//                     res += '<a href="activity.html?act_id=' + val.id + '"><p>' + val.content + '</p>'
//                     res += '</a></div>'
//                     res += '<div id="n_lt">'
//                     res += '<div id="n_lab">' + val.label + '</div>'
//                     res += '<div id="n_time">' + val.date + '</div>'
//                     res += '</div></div></div>'
//                 })
//                 $('#b2_l2').html(res)
//                 var pagearr = JSON.parse(mes.data).page
//                 getpage(pagearr[0], pagearr[1])
//             } else {
//                 $('#b2_l2').html('')
//                 getpage(1, 1)
//             }
//         }
//
//         ws.onclose = function () {
//             console.log('连接关闭')
//         }
//     }
//
// }
//
// webreq({pag: '1'})
//-------

// 构造html
function makeresult(data) {
    var res = ''
    $.each(data, function (index, val) {
        res += '<div id="new_act_">'
        res += '<a href="activity.html?act_id=' + val.id + '">'
        res += '<img src="' + ACTIMG_URL + val.actimg + '" alt="" act_id="' + val.id + '">'
        res += '</a>'
        res += '<div id="new_content">'
        res += '<div id="n_tit" act_id="' + val.id + '">'
        res += '<a href="activity.html?act_id=' + val.id + '">' + val.title
        res += '</a></div>'
        res += '<div id="n_cont" act_id="' + val.id + '">'
        res += '<a href="activity.html?act_id=' + val.id + '"><p>' + val.content + '</p>'
        res += '</a></div>'
        res += '<div id="n_lt">'
        res += '<div id="n_lab">' + val.label + '</div>'
        res += '<div id="n_time">' + val.date + '</div>'
        res += '</div></div></div>'
    })
    return res
}

// 请求历史活动数据
function request_data({state, cond = '1'}) {
    var mes = localStorage["history" + cond]
    if (mes) {
        mes = JSON.parse(mes)
        var pagea = JSON.parse(localStorage["historypage"])
        $('#b2_l2').html(makeresult(mes))
        getpage(pagea[0], pagea[1])
    } else {
        $.ajax({
            type: 'GET',
            contentType: 'application/json',
            // url: SER_URL + 'active/' + state + '/' + cond + '?tag=' + tag,
            url: SER_URL + 'active/' + state + '/' + cond,
            success: function (response) {
                if (response.code === 200) {
                    var data = response.data
                    var res = makeresult(data)
                    $('#b2_l2').html(res)
                    var pagearr = response.page
                    getpage(pagearr[0], pagearr[1])
                    if (state === 'history') {
                        localStorage['history' + cond] = JSON.stringify(data)
                        localStorage['historypage'] = JSON.stringify(pagearr)
                    }
                }
                if (response.code === 201) {
                    $('#b2_l2').html('')
                    getpage(1, 1)
                }
            }
        })
    }
}


// 历史活动点击事件
$('#z_his_act').on('click', function () {
    act_nh = 'history'
    request_data({state: 'history'})
})


// 页码点击事件
$('#l_num>#ul').on('click', '.page', function () {
    // if (act_nh === 'new') {
    //     return;
    // }
    var page = $(this).text()
    var page_now = $('#page_now').text()
    if (page === '上一页') {
        page = Number(page_now) - 1
    }
    if (page === '下一页') {
        page = Number(page_now) + 1
    }
    if (page == page_now) {
        alert('您已经在当前页面')
        return
    }
    if (act_nh === 'search') {
        if (searchmes) {
            search_data({state: 'search', cond: page, mes: searchmes})
        }
        return;
    }
    if (act_nh === 'history') {
        request_data({state: act_nh, cond: page})
    }
    if (act_nh === 'new') {
        ws.close()
        webrequestpage(page)
    }
})


//    ---------------------

// pass

// if (act_nh === 'new') {
//     if (typeof (ws) == 'object') {
//         alert(123456789)
//         websend(page)
//     }
// } else {
//     request_data({state: act_nh, cond: page})
// }


// websocket 请求最新活动数据
// function web_request({state, cond = '1'}) {
//     // ws = new WebSocket(WEBSOCKET_URL + 'active/' + state + '/' + cond + '?tag=' + tag)
//     // ws = new WebSocket(WEBSOCKET_URL + 'active/' + state + '/' + cond)
//
// }

// // 过滤非第一次请求
// function fnew() {
//     var mes = localStorage["history" + cond]
//     if (mes) {
//         mes = JSON.parse(mes)
//         var pagea = JSON.parse(localStorage["historypage"])
//         $('#b2_l2').html(makeresult(mes))
//         getpage(pagea[0], pagea[1])
//     } else {
//         web_request({state: 'new'})
//     }
// }


// 获取页码
// $.ajax({
//     type: 'GET',
//     contentType: 'application/json',
//     url: SER_URL + 'active/page',
//     success: function (response) {
//         if (response.code == 200) {
//             var data = response.data
//             res = ''
//             $.each(data,function (index,val) {
//                 res += '<li class="page">'+val+'</li>'
//             })
//             $('#l_num>ul').html(res)
//         }}})

// 标记当前状态 已移除
// act_nh = '';

// 触发跳转到活动详情页
// $('#2_l2>#new_act_>img,#2_l2>#new_content>#n_tit,#2_l2>#new_content>#n_cont').on('click', function () {
//     var act_id = $(this).attr('act_id')
//     window.location.href = 'activity.html?act_id=' + act_id
// });

// websocket 连接方法 参数 sendfunc: 发送的方法 recivefunc: 接收
// function web() {
//     if ('websocket' in window) {
//         alert('您的浏览器支持websocket')
//     }
//     // 'ws:'+ '127.0.0.1:8000/' + 'active/new'
//     // 创建连接
//     ws = new WebSocket('ws://127.0.0.1:8000/active/new')
//
//
//     ws.onopen = function () {
//         ws.send('发送数据')
//         // alert('发送中')
//     }
//
//
//     ws.onmessage = function (mes) {
//         var res = mes.data
//         alert(res)
//     }
//
//     ws.onclose = function () {
//         alert('连接关闭')
//     }
// }

// web()


// $('#ul>li:first').addClass('pageup')
// $('.pageup').text('上一页')
// }
// $.each($('#ul>.page'), function (index, data) {
//     pag = page-5+index
//     if (pag > page)return
//     $(data).text(pag)
// })
// for (var j = 1; j <= 10; j++, i++) {
//     if (i > pagenums) break
//     console.log(i)
//     var $page = $('.page' + String(j))
//     if (j == page) {
//         $page.text(i)
//         continue
//     }
//     $page.text(i)
// $('#ul>li:last').addClass('pagedown')
//      $('.pagedown').text('下一页')
// }

