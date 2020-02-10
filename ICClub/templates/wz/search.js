//搜索跳转

$(function () {
    $('#search').click(function () {
        alert('ssss');
        var val = $('#input').val();
        if (val) {
            alert('dianjishijian    '+typeof val);
            window.location.href = 'notfound.html?kw=' + val;

        } else {
            alert('搜索为空,请重新输入')
        }
        // window.location.href = 'search_list.html?input=' + UTFTranslate.Change(val);
    });


    $('#input').on('keypress', function (event) {
        if (event.keyCode == 13) {
            $('#search').trigger('click')
        }
    });


});
// /**头部搜索按钮**/
// $('#search').on('click',  function () {
//     var kw = $('.input-kw').val();
//     var loc = 'activity.html';
//     if (kw) {
//         loc += '?kw=' + kw;
//     }
//     location.href = loc;
// })

function toUnicode(s) {
    return s.replace(/([\u4E00-\u9FA5]|[\uFE30-\uFFA0])/g, function (newStr) {
        return "\\u" + newStr.charCodeAt(0).toString(16);
    });
}