import folium


def changemap(num):
    if num==1:
        tiles = 'http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}'# 高德街道图
    elif num==2:
        tiles = 'http://webst02.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}'# 高德卫星图
    elif num==3:
        tiles='https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}' # google 卫星图
    else:
        tiles = 'https://mt.google.com/vt/lyrs=h&x={x}&y={y}&z={z}'  # google 地图
    return tiles


#第一参数为地图类型，第二参数为坐标值
def mapmain(num,location):
    maptitle = changemap(num)
    lacal = location
    Map = folium.Map(
            location=lacal,
            zoom_start=18,
            tiles=maptitle,
            # tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',# 高德街道图
            # tiles='http://webst02.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}', # 高德卫星图
            # tiles='https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', # google 卫星图
            # tiles='https://mt.google.com/vt/lyrs=h&x={x}&y={y}&z={z}', # google 地图
            attr='default'
    )
    folium.Marker(location=lacal, popup='<p style="color: green">this is beijing</p>').add_to(Map)
    Map.save('mapUI.html')
    return 'mapUI.html'


if __name__ == '__main__':
    map1 = mapmain(1,[16.222,23.25])