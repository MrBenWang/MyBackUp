import json
"""
测试使用，
"""

aa = '{"errorcode": 0, "errormsg": "OK", "tags": [{"tag_name": "\\u00e5\\u008d\\u00a1\\u00e9\\u0080\\u009a", "tag_confidence": 18}, {"tag_name": "\\u00e6\\u0088\\u00aa\\u00e5\\u009b\\u00be", "tag_confidence": 24}, {"tag_name": "\\u00e6\\u0096\\u0087\\u00e6\\u009c\\u00ac", "tag_confidence": 27}], "faces": []}'
bb = json.loads(aa)
stest22 = bb["tags"][0]["tag_name"].encode('ISO-8859-1').decode("utf8")
cc = max(bb["tags"], key=lambda item: item['tag_confidence'])
print(stest22)