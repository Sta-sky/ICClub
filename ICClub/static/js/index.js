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
                    msg += encodeURI(ACT_IMG_URL + element.imgurl) + '" alt=""></a>';
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


// 定义当前页标签
var tag = GetUrlString('sub')
var tags = encodeURI(encodeURI(tag))
// alert(tag)



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
                    res += '<img src="' + encodeURI(ACT_IMG_URL + val.imgurl) + '" alt="" act_id="' + val.act_id + '">';
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
imgChange()
getFocus($('#l1 a'));

