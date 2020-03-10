// ==UserScript==
// @name         XAUUSD-2-AUTD
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  伦敦金 和 上海金的 换算，注意一定要搭配 uBlock ，否则广告会阻挡
// @author       You
// @match        https://www.fx110.com/
// @grant        none
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

    document.ren
    var _new_div = document.createElement("div");
    _new_div.className = "contact";
    _new_div.style = "text-align: center;font-size: 40px;font-weight: 600;";
    _new_div.innerText = "上海金 " + _autd.toFixed(4);

    var _showDiv = $("div[class='dealer_search']");
    _showDiv.children("div[class='contact']").remove();
    _showDiv.append(_new_div);
}