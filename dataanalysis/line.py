# coding=utf-8

from pyecharts import Bar, Line

import random

attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]

v1 = [5, 20, 36, 10, 75, 90]

v2 = [10, 25, 8, 60, 20, 80]

bar = Bar("柱状图示例", height=720)

bar.add("商家A", attr, v1, is_stack=True)

bar.add("商家B", attr, v2, is_stack=True)

line = Line("折线图示例", title_top="50%")

attr = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

line.add(

"最高气温",

attr,

[11, 11, 15, 13, 12, 13, 10],

mark_point=["max", "min"],

mark_line=["average"],

)

line.add(

"最低气温",

attr,

[1, -2, 2, 5, 3, 2, 0],

mark_point=["max", "min"],

mark_line=["average"],

legend_top="50%",

)

bar.render(path="./html/bar.html")
line.render(path="./html/line.html")
