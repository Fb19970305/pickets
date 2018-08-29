# -*- coding: utf-8 -*-

import re
import requests
# pprint: 格式化输出
url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9063"
# 获取URL
response = requests.get(url)
# 正则提取中文字母和代号
stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
# indent:定义打印信息的缩进为4个空格
#pprint(dict(stations), indent=4)
stations = dict(stations)