var http = require('http');
var querystring = require('querystring');
const jsdom = require("jsdom");

var postHTML =
    '<html><head><meta charset="utf-8"><title>菜鸟教程 Node.js 实例</title></head>' +
    '<body>' +
    '<form method="post">' +
    'meta_content： <input name="content"><br>' +
    'js： <input name="js"><br>' +
    'ts： <input name="ts"><br>' +
    '<input type="submit">' +
    '</form>' +
    '</body></html>';





function get_cookie(content, res_js, res_ts) {
    var {JSDOM} = jsdom;
    var dom = new JSDOM("<!DOCTYPE html><p>Hello world</p><meta content="+content+">", {
        url: "http://jg.hbcic.net.cn/web/QyManage/QyList.aspx",
        referrer: "http://jg.hbcic.net.cn/web/QyManage/QyList.aspx",
        contentType: "text/html",
        userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        includeNodeLocations: true
    });

    window = dom.window;
    document = dom.window.document;
    navigator = dom.window.navigator;
    navigator['appCodeName'] = "Mozilla";
    navigator['appName'] = "Netscape";
    navigator['appVersion'] = "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36";
    navigator['cookieEnabled'] = true;
    navigator['hardwareConcurrency'] = 6;
    navigator['language'] = "zh-CN";
    navigator['languages'] = ["zh-CN", "zh"];
    navigator['platform'] = "Win32";
    navigator['product'] = "Gecko";
    navigator['productSub'] = "20030107";
    navigator['vendor'] = "Google Inc.";
    navigator['webkitPersistentStorage'] = {};
    navigator['webkitTemporaryStorage'] = {};
    navigator['userActivation'] = {'hasBeenActive': true,'isActive': false};
        eval(res_ts.toString("iso-8859-1"))
        window['$_ts'] = $_ts;
        eval(res_js)
        return document.cookie
}

http.createServer(function (req, res) {
    //暂存请求体信息
    var body = "";

    //请求链接
    console.log(req.url);

    //每当接收到请求体数据，累加到post中
    req.on('data', function (chunk) {
        body += chunk;  //一定要使用+=，如果body=chunk，因为请求favicon.ico，body会等于{}
        // console.log("chunk:",chunk);
    });

    //在end事件触发后，通过querystring.parse将post解析为真正的POST请求格式，然后向客户端返回。
    req.on('end', function () {
        // 解析参数
        body = querystring.parse(body);  //将一个字符串反序列化为一个对象
        // console.log("body:",body);

        // 设置响应头部信息及编码\<br><br>      res.writeHead(200, {'Content-Type': 'text/html; charset=utf8'});
        if(body.content && body.js) { // 输出提交的数据
            try {
                ret = get_cookie(body.content, body.js, body.ts)
                ret = ret.split(';')[1]
            }catch (e) {
                console.log(e.toString())
                ret=''
            }
            res.write(ret)
        } else {  // 输出表单
            res.write(postHTML);
        }
        res.end();
    });
}).listen(3000);