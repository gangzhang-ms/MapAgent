
import os
import requests
from datetime import datetime, timedelta

# 替换为您的高德地图 API 密钥
api_key = os.getenv("GAODE_MAP_API_KEY")

# 起点和终点
origin = '西藏南路地铁站'
destination = '紫星路999号'

today = datetime.today()

bus_xujiahui_1 = ("徐家汇地铁站", datetime(today.year, today.month, today.day, 9, 0, 0), datetime(today.year, today.month, today.day, 9, 35, 0))
bus_schedule= []
bus_schedule.append(bus_xujiahui_1)

# 获取起点和终点的经纬度
def get_location(address):
    url = f'https://restapi.amap.com/v3/geocode/geo?address={address}&key={api_key}&strategy=6&show_fields=duration'
    response = requests.get(url)
    data = response.json()
    if data['status'] == '1' and data['geocodes']:
        location = data['geocodes'][0]['location']
        return location
    else:
        raise Exception('Failed to get location')

# 获取公共交通出行方案
def get_transit_plan(origin, destination):
    origin_location = get_location(origin)
    destination_location = get_location(destination)
    url = f'https://restapi.amap.com/v3/direction/transit/integrated?origin={origin_location}&destination={destination_location}&city=上海&key={api_key}'
    response = requests.get(url)
    data = response.json()
    if data['status'] == '1' and data['route']:
        return data['route']
    else:
        raise Exception('Failed to get transit plan')

# 打印公共交通出行方案
def validate_transit_plan(route, departure_time, latest_arrival_time):
    if 'transits' not in route:
        return (False, [], -1, -1, -1)

    paths = []
    for transit in route['transits'][:3]:
        duration_minutes = int(transit['duration']) // 60
        arrival_time = departure_time + timedelta(minutes=duration_minutes)
        path = []
        for segment in transit['segments']:
            if 'walking' in segment and 'distance' in segment['walking'] and int(segment['walking']['distance']) > 0:
                path.append(f"步行 {segment['walking']['distance']} 米")
                for step in segment['walking']['steps']:
                    path.append(f"  - {step['instruction']}")
            if 'bus' in segment:
                for busline in segment['bus']['buslines']:
                    path.append(f"乘坐 {busline['name']} 从 {busline['departure_stop']['name']} 到 {busline['arrival_stop']['name']}")
        if arrival_time <= latest_arrival_time:
            paths.append((True, path, duration_minutes, arrival_time, int(float(transit['cost']))))
    return paths

# 示例调用
# route = get_transit_plan(origin, destination)
# print_transit_plan(route)

# 获取并打印出行方案
if __name__ == '__main__':
    paths = []
    departure_time = datetime(today.year, today.month, today.day, 8, 30, 0)
    route = get_transit_plan(origin, destination)
    canArrive, path, duration_minutes = validate_transit_plan(route, departure_time, datetime.now() + timedelta(hours=2))
    if canArrive:
        paths.append(path + "\n" + f"总时间: {duration_minutes} 分钟")
    for station, leave_time, arrive_time in bus_schedule:
        route = get_transit_plan(origin, station)
        canArrive, path, duration_minutes = validate_transit_plan(route, departure_time, leave_time)
        if canArrive:
            duration_minutes += int((arrive_time - leave_time).total_seconds()) // 60
            paths.append(path + "\n" + f"乘坐班车：{station}，出发时间: {leave_time.strftime('%H:%M')}，到达时间: {arrive_time.strftime('%H:%M')}" + "\n" + f"总时间: {duration_minutes} 分钟")
    if paths:
        for path in paths:
            print(path)