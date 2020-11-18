
var user_id = GetUrlString('id');
token = window.localStorage.getItem('user_token');
//console.log(token);
$.ajax({
    type: 'get',
    headers: {'Authorization': token},
    contentType: 'application/json',
    url: SER_URL + 'users/home?id=' + user_id,
    success: function (response) {
        if (response.code == 200) {
            var data = response.data;
            document.getElementById('img').src =IMG_URL+ data.url;

            var res1 = '';
            res1 += '<span class="nick">' + data.nickname + '</span>';
            res1 += '<span class="credit_">信誉积分:' + data.credit + '</span>';
            res1 += '<span class="level_">LV' + data.level + '</span>';
            res1 += '<a href="user_update.html?id=' + user_id + '" id="personal_data">编辑个人资料</a>';
            $('.user_1').html(res1);

            hidden_display(data.is_self);

            var res2 = '';
            res2 += '<ul><li class="dt"> 动态 ' + data.participat_num + '</li>';
            res2 += '<li class="fans">粉丝 ' + data.likes + '</li>';
            res2 += '<li class="gz">关注 ' + data.likes + '</li>';
            res2 += '<li class="dl">登录 ' + data.logins_days + '</li>';
            res2 += '<li class="fq">发起 ' + data.sponson_num + '</li>';
            res2 += '<li class="cy">参与 ' + data.participat_num + '</li></ul>';
            $('.user_2').html(res2);

            var res3 = '';
            var interest = '';
            res3 += '<span class="s1">介绍 : ' + data.introduction + '</span>';
            for (var m = 0; m < data.interest.length; m++) {
                interest += data.interest[m]
            }
            res3 += '<span>爱好 : ' + interest + '</span>';

            res3 += '<span>性别 : ' + data.gender + '</span>';
            res3 += '<span>生日 : ' + data.birth + '</span>';
            res3 += '<span>城市 : ' + data.city + '</span>';
            $('.user_3').html(res3);

            var res4 = '<h2>发起的活动</h2>';
            if (data.tag.length == 0) {
                res4 += '<div class="no_active">你还没有创建任何活动哦!快点行动起来!!!</div>';
                $('#tz_l').html(res4);
            } else {

                for (var i = 0; i < data.tag.length; i++) {
                    res4 += '<div class="tz_l">';
                    res4 += '<ul>';
                    res4 += '<li class="l1">[ <a class="label" href=label.html?sub=' + encodeURI(encodeURI(data.tag[i])) + '>' + data.tag[i] + '</a> ] ' + '<a class="title" href="activity.html?act_id=' + data.act_id[i] + '">' + data.subject[i] + '</a></li>';
                    res4 += '<div><span>浏览 :' + data.click_num[i] + '   发帖 : ' + data.create_time[i] + '</span>';
                    res4 += '<span>回复 :' + data.click_num[i] + '   最新评论 : ' + data.update_time[i] + '</span>';
                    res4 += '</div></ul>';
                    res4 += '</div>';
                }
                $('#tz_l').html(res4);
            }

            var res5 = '<h2>参与的活动</h2>';
            if (data.tag_p.length == 0) {
                res5 += '<div class="no_active">点击主页快快参加活动吧</div>';
                $('#tz_r').html(res5);
            } else {
                for (var j = 0; j < data.tag_p.length; j++) {
                    res5 += '<div class="tz_r">';
                    res5 += '<ul>';
                    res5 += '<li class="l1">[ <a class="label" href=label.html?sub=' + encodeURI(encodeURI(data.tag_p[j])) + '>' + data.tag_p[j] + '</a> ] ' + '<a class="title" href="activity.html?act_id=' + data.act_id_p[j] + '">' + data.subject_p[j] + '</a></li>';
                    res5 += '<div><span>浏览 :' + data.click_num_p[j] + '   发帖 : ' + data.create_time_p[j] + '</span>';
                    res5 += '<span>回复 :' + data.collection[j] + '   最新评论 : ' + data.update_time_p[j] + '</span>';
                    res5 += '</div></ul>';
                    res5 += '</div>';
                }
                $('#tz_r').html(res5);
            }

        } else if (response.code === 10201){
            alert(response.message)
            window.location.href = 'login.html'
        }

    },
});

function hidden_display(data) {
    if (data != 'yes') document.getElementById('personal_data').style.display = 'none';
}