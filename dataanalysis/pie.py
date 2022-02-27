from pyecharts.charts import Pie
def piehtml():
    attr = ["人", "轿车", "公交车", "摩托车", "卡车", "自行车"]
    v1 = [11, 12, 13, 10, 10, 10]
    pie = Pie("类别检测结果")
    pie.add(
        "",
        attr,
        v1,
        is_label_show=True,
        is_more_utils=True
    )
    pie.render(path="./html/Bing1.html")
    return "./html/Bing1.html"

if __name__ == "__main__":
    piehtml()

