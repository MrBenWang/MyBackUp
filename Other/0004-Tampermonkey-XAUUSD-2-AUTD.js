// ==UserScript==
// @name         XAUUSD-2-AUTD
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  伦敦金 和 上海金的 换算，注意一定要搭配 uBlock ，否则广告会阻挡
// @author       You
// @match        https://www.fx110.com/
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function () {
    'use strict';
    setInterval(convertFun, 1500);
})();

function convertFun() {
    var _xau = parseFloat($("a[data-code='XAUUSD'] > div[class='currency'] > p:eq(1)").text());
    var _chn = parseFloat($("a[data-code='USDCNH'] > div[class='currency'] > p:eq(1)").text());
    var _ozt = 31.1034768;
    var _autd = _xau / _ozt * _chn;

    var _new_div = "<div class='contact' style='text-align: center;font-size: 35px;font-weight: 400;'>上海金 "
        + _autd.toFixed(2) +
        "<span style='color: red;'>(换)</span> / ";
    var _new_url = "https://hq.sinajs.cn/?_=" + new Date().getTime() + "/&list=nf_AU0";
    GM_xmlhttpRequest({
        url: _new_url,
        method: "GET",
        onload: function (dataStr) {
            //var hq_str_nf_AU2006="黄金2006,134412,371.660,373.260,368.760,0.000,369.400,369.440,369.420,0.000,376.080,12,31,187478.000,88177,沪,黄金,2020-03-10,1,,,,,,,,,371.840";
            try {
                var _data = dataStr.responseText.split("=")[1].split(",")[7]; // 当前均价

                _new_div += parseFloat(_data).toFixed(2) + "<span style='color: red;'>(主)</span>";
                var _showDiv = $("div[class='dealer_search']");
                _showDiv.children("div[class='contact']").remove();
                _showDiv.append(_new_div);
            }
            catch (err) {
                console.log(err);
            }
        }
    });
}