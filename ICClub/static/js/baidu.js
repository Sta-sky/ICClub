// 百度地图API功能
function showmap() {
    var searchresult = []
    var map = new BMap.Map("allmap");
    // var point = new BMap.Point(116, 40);
    map.centerAndZoom(REGION, 12);      // 初始化地图,用城市名设置地图中心点
    var mapsearch = new BMap.LocalSearch(
        map,
        {
            renderOptions: {
                map: map,
            },
            pageCapacity: 10,
        });

    // 把搜索结果放进数组,添加标注点击事件
    mapsearch.setMarkersSetCallback(function (arr) {
        $.each(arr, function (index, data) {
            // searchresult = mapsearch.getResults()
            searchresult.push(data)
            // var pos = new BMap.Marker(data.point)
            // 点击标注信息 把标注信息写入输入框
            data.marker.addEventListener('infowindowopen', function (e) {
                // 遍历结果 如果当前打开小窗口的point==结果中的point,显示address
                if (searchresult) {
                    var ep = e.currentTarget.point
                    $.each(searchresult, function (index, lpoint) {
                        if (ep.equals(lpoint.point)) {
                            $('#intext').val(lpoint.address + ' ' + lpoint.title);
                            return;
                        }
                    })
                }

            })
        })
    })


    map.addEventListener('click', function (e) {
            // 获取当前点击的地址  自动切换到当前地址为中心
            var points = new BMap.Point(e.point.lng, e.point.lat)
            map.panTo(points)
        }
    )

    // 检测地址是否在服务区
    function myFun(result) {
        var cityName = result.name;
        if (cityName !== '成都市') {
            alert('系统检测到您当前地址不在服务区内,如仍要继续操作,视为您已承担相应条文')
        }
    }

    var myCity = new BMap.LocalCity();
    myCity.get(myFun);

    // 地图搜索
    $('#qran').on('click', function () {
        var mess = $('#intext').val()
        mapsearch.search(mess)
    })


    // 确定提交
    $('#qdan').on('click', function () {
        // var mes = $('#intext').val()
        $('#addr').val($('#intext').val())
        $('#mapp').attr('style', 'display:none')
    })
}


// var geo = new BMap.GeolocationControl()


// 打开地图搜索
$('#mapsearch').on('click', function () {
    $('#mapp').removeAttr('style');
    showmap()
})


// 手写的 白写了 留作纪念
// var parameter = '?query=' + mess + '&region=' + REGION + '&output=json&ak=' + BAIDUSECRETKEY
// $.ajax({
//     url: BAIDUURL + parameter,
//     type: 'GET',
//     dataType: 'jsonp',
//     contentType: 'application/json',
//     success: function (response) {
//         if (response.status === 0) {
//             var data = response.results
//             console.log(data)
//             if (data) {
//                 var pot = data[0].location
//                 map.panTo(new BMap.Point(pot.lng, pot.lat))
//             } else {
//                 alert('查询无结果')
//             }
//         }
//     }
// })


// map.addEventListener("click", function (e) {
// $('#intext').val(points)
// var searchlist = mapsearch.getResults()
// var list = searchlist.Br
// console.log(searchlist)

// });


//     var searchlist = mapsearch.getResults()

//     }

// onSearchComplete: function(results) {
//     var arr = results.Br
//     console.log(arr)
//     $.each(arr,function (index,data) {
//         var marker = new BMap.Marker(data.point);
//     })
// }

// 三级列表
// {#<select name="select-city" id="province">#}
//              {#       <option value="provinces" id="provinces">四川省</option>#}
//              {#   </select>#}
//              {#   <select name="citys" id="city">#}
//              {#       <option value="citys" id="citys">成都市</option>#}
//              {#   </select>#}
//              {#   <select name="areas" id="area">#}
//              {#       <option value="e0" id="areas">请选择</option>#}
//              {#       <option value="e1">高新区</option>#}
//              {#       <option value="e2">金牛区</option>#}
//              {#       <option value="e3">锦江区</option>#}
//              {#       <option value="e4">青羊区</option>#}
//              {#       <option value="e5">温江区</option>#}
//              {#       <option value="e5">成华区</option>#}
//              {#       <option value="e5">郫都区</option>#}
//              {#       <option value="e5">双流区</option>#}
//              {#       <option value="e5">天府新区</option>#}
//              {#       <option value="e5">青白江区</option>#}
//              {#       <option value="e5">泉驿区</option>#}
//              {#   </select>#}