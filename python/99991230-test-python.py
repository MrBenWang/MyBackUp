from functools import reduce
"""
测试使用，
"""

print(
    reduce(lambda x, y: str(x.value or "") + str(y["value"] or ""),
           ({
               "value": None
           }, {
               "value": None
           })))
