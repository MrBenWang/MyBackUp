// ==UserScript==
// @name         RSA 翻译内容自动填充数据
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://lmsa.prod.cloud.lenovo.com/lmsa-web/lmsa/multilingual/edit.jhtml?*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=lenovo.com
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    // Your code here...
    var txtInput = $("<textarea id='txtMyInput' type='text' style='width: 600px;height: 80px;' />");
    txtInput.change(function () {
        $("#txtMyInput").val($("#txtMyInput").val().trimEnd()); //去掉最后的回车换行符
        console.log("去掉回車換行");
    });
    //txtInput.val("K1184	Please input your SN...	SNを入力してください...	Ingrese su sn ...	Wprowadź swój SN ...	Por favor, insira seu SN ...	Пожалуйста, введите свой SN ...	Si prega di inserire il tuo SN ...	请输入您的SN ...	Bitte geben Sie Ihre SN ... ein ...	Prosím, zadajte svoje SN ...	Молимо унесите своју сн ...	Vă rugăm să introduceți SN ...	Моля, въведете вашия SN ...	Zadejte prosím SN ...");

    var inputBtn = $("<input type='button' value='填 充' class='btn btn-primary' style='background-color:#E31D1A' />");
    inputBtn.click(inputData);

    $($("#editForm > table.table > tbody > tr:nth-child(1) > td")[0]).append(txtInput);
    $($("#editForm > table.table > tbody > tr:nth-child(1) > td")[0]).append(inputBtn);

    function inputData() {
        var _inputTxt = $("#txtMyInput").val();
        var tranlates = _inputTxt.split('\t');
        if (tranlates.length != 15) {
            alert("翻译内容的长度不对：" + tranlates.length)
            return;
        }


        if ($("#uniqueKey").val() == tranlates[0] && $("#content1").val() == tranlates[1]) {
            for (let index = tranlates.length; index > 1; index--) {
                $("#content" + index).val(tranlates[index]);
            }
        } else {
            const msg = `Key:[${$("#uniqueKey").val()}]和[${tranlates[0]}], content:[${$("#content1").val()}]和[${tranlates[1]}] 不匹配.`
            alert(msg)
        }
    }
})();