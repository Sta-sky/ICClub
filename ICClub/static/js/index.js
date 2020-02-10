//首页最热活动跳转
$(function () {

    $('.b2_left2_img').click(function () {
        act_id = $(this).attr('act_id');
        window.location.href = 'activity.html?act_id=' + act_id;
    });


});


//最热活动图片、标题获取
function imgChange() {
    $.ajax({
        type: 'post',
        url: SER_URL + 'active/index/hot',
        contentType: 'application/json',
        success: function (response) {
            if (response.code == 200) {
                data = response.data;
                var msg = '';
                $.each(data, function (index, element) {
                    msg += '<div class="b2_left2"><div><a href="activity.html?act_id=' + element.act_id + '"><img class="b2_left2_img" act_id="' + element.act_id + '" src="';
                    msg += encodeURI(ACTIMG_URL + element.imgurl) + '" alt=""></a>';
                    msg += '</div><p class="b2_left2_text" act_id="' + element.act_id + '">' + element.subject + '</p></div>';
                    if (index == 3) {
                        return false;
                    }
                });
                $('#b2_l1').html(msg);
            }
        },
        error: function () {
            console.log('服务器异常')
        }
    });
}


//最热活动图片、标题自动切换
function autoImgChange() {
    setInterval(function () {
        imgChange();
    }, 600000);
}

// 定义当前页标签
var tag = getUrlParam('sub')
var tags = encodeURI(encodeURI(tag))
// alert(tag)

//搜索跳转
$(function () {
    $('.btn-submit').click(function () {

        var val = $('#keyword').val();
        // var page = 'index.html';

        if (val) {
            // window.location.href = encodeURI(page + '?kw=' + val);
            // //window.location.href = page + '?kw=' +toUnicode(val);
            // act_nh = 'search';
            search_data({state: 'search', acttag: tag});

        } else {
            alert('搜索为空,请重新输入')
        }
    });

    $('#keyword').on('keypress', function (event) {
        if (event.keyCode == 13) {
            $('.btn-submit').trigger('click')
        }
    });
});

function toUnicode(s) {
    return s.replace(/([\u4E00-\u9FA5]|[\uFE30-\uFFA0])/g, function (newStr) {
        return "\\u" + newStr.charCodeAt(0).toString(16);
    });
}

let getQueryString = (searchKey) => {
    /**
     * @param {String} searchKey [查询url数据]
     * @return {String} searchData [查询结果]
     *
     **/
    let searchData = {};
    let urlData = window.location.href;
    urlData = urlData.split('?');
    urlData.shift();
    urlData = urlData[0].split('&');
    urlData.forEach((item, i, self) => {
        let urlDataItem = item.split('=');
        searchData[urlDataItem[0]] = urlDataItem[1];
    });
    return searchData[searchKey];
};

// 标记状态 z_index的标记已移除
act_nh = ''

//搜索事件
function search_data({state, cond = '1', mes = '', acttag = ''}) {
    //let searchData = getQueryString('kw');
    var val = $('#keyword').val();
    var searchData = ''
    // var urls = ''
    if (mes) {
        searchData = mes
    } else {
        searchData = decodeURI(decodeURI(val));
    }
    // if (tag) {
    //     urls = SER_URL + 'active/' + state + '/' + cond + '?tag=' + tag
    // } else {
    //     urls = SER_URL + 'active/' + state + '/' + cond
    // }
    $.ajax({
        url: urls = SER_URL + 'active/' + state + '/' + cond,
        type: 'post',
        data: {
            //q:unescape(searchData.replace(/\\/g, "%")),
            q: searchData,
            tag: acttag
        },
        dataType: 'json',
        contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
        success: function (response) {
            console.log(response)
            // alert(1239999999999999999)
            if (response.code === 200) {
                // alert(123456789);
                var data = response.data;
                var res = '';
                $.each(data, function (index, val) {
                    res += '<div id="new_act_">';
                    res += '<a href="activity.html?act_id=' + val.act_id + '">';
                    res += '<img src="' + encodeURI(ACTIMG_URL + val.imgurl) + '" alt="" act_id="' + val.act_id + '">';
                    res += '</a>';
                    res += '<div id="new_content">';
                    res += '<div id="n_tit" act_id="' + val.act_id + '">';
                    res += '<a href="activity.html?act_id=' + val.act_id + '">' + val.subject;
                    res += '</a></div>';
                    res += '<div id="n_cont" act_id="' + val.act_id + '">';
                    res += '<a href="activity.html?act_id=' + val.act_id + '"><p>' + val.content + '</p>';
                    res += '</a></div>';
                    res += '<div id="n_lt">';
                    res += '<div id="n_lab">' + val.tag + '</div>';
                    res += '<div id="n_time">' + val.date + '</div>';
                    res += '</div></div></div>'
                });
                $('#b2_l2').html(res);
                act_nh = 'search'
                searchmes = searchData
                var pagearr = response.page;
                getpage(pagearr[0], pagearr[1]);
            } else {
                alert(response.error)
            }

        },
        error: function (err) {
            console.log(err)
        }
    })
}


//
//
// document.addEventListener('DOMContentLoaded', () => {
//     //SER_URL = 'http://127.0.0.1:8000/
//     var SEARCHURL = SER_URL + 'active/search';
//     let searchData = getQueryString('kw');
//     searchData = decodeURI(decodeURI(searchData));
//     // reloadDom();
//     /* 请求详情数据 */
//     $.ajax({
//         type: 'post',
//         url: SEARCHURL,
//         data: JSON.stringify({q: searchData}),
//         dataType: 'json',
//         contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
//         success: function (data) {
//             if (data.code == 200) {
//                 var result = data;
//                 //加载渲染
//
//                 var res = '';
//                 result.data.forEach(val => {
//                     res += '<div id="new_act_">'
//                     res += '<a href="activity.html?act_id=' + val.id + '">'
//                     res += '<img src="' + IMG_URL + val.actimg + '" alt="" act_id="' + val.id + '">'
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
//                 });
//
//                 $('#b2_l2').html('<div class="salc_top">搜索结果  共 ' + result.data.length + ' 条</div>' + res);
//
//
//                 if (result.result)
//                     console.log("pages: " + pages);
//                 var pages = Math.ceil(result.paginator.total / result.paginator.pagesize);
//                 window.localStorage.setItem('pageMax', pages);
//
//                 var html = '';
//                 html += '<a href="javascript:;" class="current">1</a>';
//                 html += '<div id="btnBox" style="display: inline-block;"></div>';
//                 for (var j = 2; j <= pages; j++) {
//                     html += '<a href="javascript:;" class="tcdNumber">' + j + '</a>'
//                 }
//                 html += '<a href="javascript:;" class="nextPage" id="next">下一页</a>';
//
//                 $('#l_num>ul').html(html);
//
//
//             } else {
//                 console.error(data.msg)
//             }
//         },
//         error: function (err) {
//             console.log(err);
//         }
//     });
//
//     class btnList {
//         constructor(btnBox, previous, next) {
//             /**
//              * @this {Element} btnBox   [按钮父元素]
//              * @this {Number}  page     [当前页]
//              * @this {Array}   btnList  [当前按钮集合]
//              * @this {Element} previous [上一页]
//              * @this {Element} next     [下一页]
//              * @this {Object}  listData [缓存请求数据]
//              * @this {Number} index    [当前元素于btnList的下标]
//              * @this {Boolean} nextFlag [判断下一页是否存在数据]
//              */
//             this.btnBox = btnBox;
//             this.page = 1;
//             this.btnList = null;
//             this.previous = previous;
//             this.next = next;
//             this.listData = new Map();
//             this.index = 0;
//             this.PageMax = window.localStorage.pageMax;
//             this.act_id = window.localStorage.act_id;
//         }
//
//         init() {
//             //console.log(this.act_id);
//             this.btnList = [].slice.call(this.btnBox.children);
//             this.register();
//         }
//
//         register() {
//             /* 注册点击事件 */
//             this.previous.addEventListener('click', () => {
//                 this.previousPage()
//             }, false);
//             this.next.addEventListener('click', () => {
//                 this.nextPage()
//             }, false);
//             this.btnBox.addEventListener('click', e => {
//                 this.handleClickBtn(e)
//             }, false);
//         }
//
//         previousPage() {
//             /* 上一页处理函数 */
//             if (this.page < 2) {
//                 return
//             }
//             if (this.index < 1) {
//                 this.btnList.forEach(item => {
//                     item.innerHTML = Number(item.innerHTML) - 1;
//                 })
//             }
//             this.page--;
//             this.index--;
//             if (this.index < 1) {
//                 this.index = 0;
//             }
//             let elm = this.btnList[this.index];
//             this.handleClick(elm);
//         }
//
//         nextPage() {
//             /* 下一页处理函数 */
//             if (this.page == this.PageMax) {
//                 alert('已经是最后一页了！');
//                 return
//             }
//             if (this.index >= this.btnList.length - 1) {
//                 this.btnList.forEach(item => {
//                     item.innerHTML = Number(item.innerHTML) + 1;
//                 })
//             }
//
//             this.page++;
//             this.index++;
//             if (this.index > this.btnList.length - 1) {
//                 this.index = this.btnList.length - 1;
//
//             }
//             let elm = this.btnList[this.index];
//             this.handleClick(elm);
//         }
//
//         handleClickBtn(e) {
//             /* btn处理函数 */
//             let target = e.target;
//             if (target.nodeName !== 'A') {
//                 return
//             }
//             let index = this.btnList.indexOf(target);
//             let page = target.innerHTML;
//             this.page = page;
//             this.index = index;
//             this.handleClick(target);
//         }
//
//         handleClick(elm) {
//             this.ajax();
//             /* 删除btn current样式*/
//             this.btnList.forEach(item => {
//                 item.classList.remove('current');
//             });
//             /* 为当前点击元素 添加current */
//             elm.classList.add('current');
//         }
//
//         ajax() {
//             $.ajax({
//                 type: 'post',
//                 url: SEARCHURL,
//                 data: JSON.stringify({
//                     //q: unescape(searchData.replace(/\\/g, "%")),
//                     q: searchData,
//                     page: this.page,
//                 }),
//                 dataType: 'json',
//                 contentType: 'application/json; charset=UTF-8',
//                 success: function (data) {
//                     if (data.code == 200) {
//                         var result = data;
//                         //加载渲染
//                         if (result.result)
//                             var res = '';
//                         result.data.forEach(val => {
//                             res += '<div id="new_act_">'
//                             res += '<a href="activity.html?act_id=' + val.id + '">'
//                             res += '<img src="' + IMG_URL + val.actimg + '" alt="" act_id="' + val.id + '">'
//                             res += '</a>'
//                             res += '<div id="new_content">'
//                             res += '<div id="n_tit" act_id="' + val.id + '">'
//                             res += '<a href="activity.html?act_id=' + val.id + '">' + val.title
//                             res += '</a></div>'
//                             res += '<div id="n_cont" act_id="' + val.id + '">'
//                             res += '<a href="activity.html?act_id=' + val.id + '"><p>' + val.content + '</p>'
//                             res += '</a></div>'
//                             res += '<div id="n_lt">'
//                             res += '<div id="n_lab">' + val.label + '</div>'
//                             res += '<div id="n_time">' + val.date + '</div>'
//                             res += '</div></div></div>'
//                         });
//
//                         $('.salc_content').html(res);
//
//                         $('.salc_top').html('搜索结果  共' + result.data.length + '条')
//                     } else {
//                         console.error(data.msg)
//                     }
//                 },
//                 error: function (err) {
//                     console.log(err);
//                 }
//             });
//
//
//         }
//     }
//
//     setTimeout(new btnList($('#btnBox')[0],
//         $('#previous')[0],
//         $('#next')[0]).init(), 2000);
// });
//
//


imgChange();
getFocus($('#l1 a'));

