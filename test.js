const $ = new Env("电信10000");
const notify = $.isNode() ? require('./sendNotify') : '';
message = ""

function getzqwzbody() {
    if ($request.url.match(/\/wapside.189.cn:9001\/jt-sign\/api\/home\/userCoinInfo/)||$request.url.match(/\/kandian.wkandian.com\/v5\/article\/detail.json/)) {
          bodyVal1 = $request.body
          console.log(encodeURIComponent(bodyVal1))
          bodyVal = encodeURIComponent(bodyVal1)
            console.log(bodyVal)}
}
