# -*- coding: utf-8 -*-
# __Author__: Hong

"""火车票查询工具

Usage:
    tickets [-gdtkz] <from> <to> <date>

注意：Usage为固定词汇，其他报错。

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 大同 2016-08-28
    tickets -t 北京 大同 2016-08-28
"""
from docopt import docopt
from requests import request
import prettytable
import colorama
import json
from pprint import pprint
from parse_station import stations
import requests
import prettytable


def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]

def cli():
    """command-line interface"""

    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']

    url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&" \
          "leftTicketDTO.to_station={}&purpose_codes=ADULT".format(date, from_station, to_station)
    r = requests.get(url, verify=False)
    available_trains = r.json()['data']['result']
    TrainsCollection(available_trains).pretty_print()

class TrainsCollection:
    header = '车次 车站 时间 历时 二等座 软卧 硬卧 硬座 无座'.split()
    def __init__(self, available_trains):
        self.available_trains = available_trains
    def pretty_print(self):
        pt = prettytable.PrettyTable()
        pt.field_names = self.header
        for raw_train in self.available_trains:
            raw_train = raw_train.split("|")
            checi = raw_train[3]
            chezhan = get_key(stations, raw_train[6])[0] + '\n' + get_key(stations, raw_train[7])[0]
            shijian = raw_train[8] + "\n" + raw_train[9]
            shijian_list = raw_train[10].split(":")
            lishi = ""
            if int(shijian_list[0]) > 0:
                lishi = str(int(shijian_list[0])) + "小时"
            lishi = lishi + shijian_list[1] + "分钟"

            erdengzuo = raw_train[30] if len(raw_train[30]) != 0 else "-"
            ruanwo = raw_train[23] if len(raw_train[23]) != 0 else "-"
            yingwo = raw_train[28] if len(raw_train[28]) != 0 else "-"
            yingzuo = raw_train[29] if len(raw_train[29]) != 0 else "-"
            wuzuo = raw_train[26] if len(raw_train[26]) != 0 else "-"

            train = [
                checi,
                chezhan,
                shijian,
                lishi,
                erdengzuo,
                ruanwo,
                yingwo,
                yingzuo,
                wuzuo,
            ]
            pt.add_row(train)
        print(pt)
if __name__ == '__main__':
    cli()
