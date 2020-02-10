// 不要调用下面这两个
// SERIP = '176.209.104.17:8000'
SERIP = '127.0.0.1:8000';
// SERIP = '176.209.104.17:8000'
var STSIP = '176.209.104.17:7001';

// ================================================================
// 服务器地址（请求数据）
var SER_URL = 'http://' + SERIP + '/';
// websocket服务器地址 上传云 换8001
// var WEBSOCKET_URL = 'ws://' + SERIP + ':8001/';
var WEBSOCKET_URL = 'ws://' + SERIP + '/';


// 静态文件地址(请求网页)
var STS_URL = 'http://' + STSIP + '/templates/';

// 用户头像图片地址(请求图片)
// var IMG_URL = 'http://' + STSIP + '/static/images/userhead/';
var IMG_URL = 'http://' + STSIP + '/static/';
// 官方活动图片地址
// var OFF_URL = 'http://' + STSIP + '/static/images/official/';
var OFF_URL = 'http://' + STSIP + '/static/';
// 活动图片位置
// var ACTIMG_URL = 'http://' + STSIP + '/static/images/activity/';
var ACTIMG_URL = 'http://' + STSIP + '/static/';

// 地图检索region行政区域,限成都
var REGION = '成都市';
// 百度地图秘钥  文件导入需手动修改src属性的ak参数
var BAIDUSECRETKEY = 'GK8muKdwK0w3So6HW89F8KlHc5BKzdbL';
// 百度地图搜索接口
var BAIDUURL = 'http://api.map.baidu.com/place/v2/search';
// 静态文件常量
var LOCALLABELLIST = ['二次元', 'IT', '篮球', '足球', '游戏', '音乐', '旅游', '跑步', '相亲', '滑雪', '潜水', '爬山', '机车', '舞蹈']
