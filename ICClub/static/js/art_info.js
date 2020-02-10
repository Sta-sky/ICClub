var article_id = getUrlParam('article');
token = window.localStorage.getItem('user_token');
// alert(article_id)
$.ajax({
    type: "get",
    dataType: 'json',
    headers: {'Authorization': token},
    url: SER_URL + 'v1/activ/article_info?article_id=' + article_id,
    contentType: 'application/json;charset=UTF-8',
    success: function (response) {
        if (response.code == 200) {
            var articleData = response.data
            // console.log('aaaaaaaaaaaa',articleData)
            // alert('Ajax 渲染了')
            // var i = 0;
            var html = ''
            html += '<div id="top"><p id="title">'+articleData.subject+'</p></div>'
            html += '<div id="num"><div class="click_nums">'+ articleData.updated_time + '</div>'
            html += '<div class="updated_time">浏览数:'+ articleData.click_nums + '</div></div>'
            html += '<hr>'
            html += '<div id="img"><img src="' +IMG_URL+ articleData.act_img + '" alt="" class="act_img" width="600px" height="320px"></div>'
            html += '<div id="paragraph">'
            for(var i=0;i<articleData.content.length;i++){
                html += '<p class="p">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + articleData.content[i] + '</p><br>'
            }
            html += '</div>'
        }
        // console.log('aaaaaaaaa')
        $('#art_info').html(html)
    },
    error: function (err) {
        console.log(err)
    }
})



// 从后端传回的数据
// 渲染函数
// var i=0;
// htmldata = null;
// function adminArticle() {
//     // articleHtml = none
//     $.ajax({
//         type: 'get',
//         contentType: 'application/json',
//         url: SER_URL + 'v1/activ/article',
//         success: function (response) {
//             if (response.code == 200) {
//                 articleData = response.data
//                 // console.log('aaaaaaaaaaaa',articleData)
//                 // alert('Ajax 渲染了')
//                 var i = 0;
//                 var html = ''
//                 html += '<div class="article">'
//                 html += '<span id="il">&lsaquo;</span>'
//                 html += '<a href="activity.html?uid='+articleData[i].user_id+'&article='+articleData[i].article_id+'"><img src="' +IMG_URL+ articleData[i].act_img + '" alt="" class="act_img" width="600px" height="320px"></a>'
//                 html += '<div class="tip"><p class="p1">热点</p>'
//                 html += '<a href="activity.html?uid='+articleData[i].user_id+'&article='+articleData[i].article_id+'"><div class="subject"><h3>' + articleData[i].subject + '</h3></div>'
//                 html += '<p style="table-layout: fixed" class="content">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + articleData[i].content + '</p></a>'
//                 html += '<div class="click_nums">浏览数:' + articleData[i].click_nums + '</div>'
//                 html += '<div class="updated_time">' + articleData[i].updated_time + '</div></div>'
//                 html += '<span id="ir">&rsaquo;</span>'
//                 html += '</div>'
//             }
//             // console.log('aaaaaaaaa')
//             $('#article').html(html)
//             // articleHtml = articleData
//             htmldata = articleData
//         },
//         error: function (err) {
//             console.log(err)
//         }
//     })
// }
// // console.log(htmldata)
// // 渲染函数
// function articleHtml(i){
//     var html = ''
//     html += '<div class="article">'
//     html += '<a href="activity.html?uid='+articleData[i].user_id+'&article='+articleData[i].article_id+'"><img src="'+IMG_URL+ articleData[i].act_img + '" alt="" class="act_img" width="600px" height="320px"></a>'
//     html += '<div class="tip"><p class="p1">热点</p>'
//     html += '<a href="activity.html?uid='+articleData[i].user_id+'&article='+articleData[i].article_id+'"><div class="subject"><h3>' + articleData[i].subject + '</h3></div>'
//     html += '<p style="table-layout: fixed" class="content">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + articleData[i].content + '</p></a>'
//     html += '<div class="click_nums">浏览数:' + articleData[i].click_nums + '</div>'
//     html += '<div class="updated_time">' + articleData[i].updated_time + '</div></div>'
//     html += '</div>'
//     return html
//     // 渲染页面
//     $('#article').html(html)
// }

// adminArticle()
// // var i = 0;
// // var articleData=new Array();
// // $('#article').html(articleHtml(i))

// // 点击左右屏切换
// //点击qi切屏
// $('#il').on('click',function(){
//     // console.log(articleHtml())
//     $('#article').fadeOut(500,function(){
//         if(i==0){
//             i=3;
//         }else{
//             i--;
//         }
//         $('#article').html(articleHtml(i)).fadeIn(500);
//     })
// });
// $('#ir').on('click',function(){
//     $('#article').fadeOut(500,function(){
//         if(i==3){
//             i=0;
//         }else{
//             i++;
//         }
//         $('#article').html(articleHtml(i)).fadeIn(500);
//     })
// });

// function rollRight(){
//         $('#article').fadeOut(500,function(){
//             if(i==3){
//                 i=0;
//             }else{
//                 i++;
//             }
//             $('#article').html(articleHtml(i)).fadeIn(500);
//         })
// }
// setInterval(rollRight,6000);

// $('#adminArticle').mouseover(function(){
// $('#il','#ir').css('color', '#ff5c2a')
// });
// $(document).ready(function(){
//     $("#adminArticle").mouseover(function(){
//       $('#il','#ir').css({ 'opacity': '0.8',
//       'transform': 'scale(1.1)',});
//     });
//     $("#adminArticle").mouseout(function(){
//       $('#il','#ir').css({'color': 'white',
//   'opacity': '0.5'});
//     });
//   });
// $('#il','#ir').css({
//     'color': '#ff5c2a',
    // 'opacity': '0.8',
    // 'transform': 'scale(1.1)',
// })
// // rollRight()

// var btnr=document.getElementById('#ir');
// btnr.onclick=function(){
//     $('#article').fadeOut(500,function(){
//         if(i==3){
//             i=0;
//         }else{
//             i++;
//         }
//         $('#article').html(articleHtml(i)).fadeIn(500);
//     })
// };
// btnr.click()
// setInterval(function(){
    // setTimeout(function(){
        // rollRight()
        // btnr.click()
    // },5000);
// },5000);

// setInterval(function(){
//     alert('点击一下');
// },3000)