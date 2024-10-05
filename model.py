from datetime import datetime, timedelta
from constants import COMPANY_LOCATION

today = datetime.today()

class travel_model:
    def __init__(self, departure, destination, time: datetime, latest_arrival_time: datetime = datetime.now() + timedelta(hours=2)):
        self.departure = departure  
        self.destination = destination
        self.time = time
        self.latest_arrival_time = latest_arrival_time
    
    def __str__(self):
        return f"时间：{str(self.time)}， 出发地:{self.departure}, 目的地:{self.destination}."
    
class transfer_schedule:
    def __init__(self, station, start_time, arrival_time, name): 
        self.station = station
        self.start__time = start_time
        self.arrival_time = arrival_time
        self.name = name

    def __str__(self):
        return f"在{self.station} 换乘 {self.name} {self.start__time.strftime('%H:%M')} 班次, 于{self.arrival_time.strftime('%H:%M')}到达{COMPANY_LOCATION}。"

SCHEDULES = [transfer_schedule("徐家汇地铁站", datetime(today.year, today.month, today.day, 9, 30, 0), datetime(today.year, today.month, today.day, 10, 5, 0), "Route1"),
            transfer_schedule("芦恒路地铁站", datetime(today.year, today.month, today.day, 8, 8, 0), datetime(today.year, today.month, today.day, 9, 00, 0), "Route2")]

class plan:
    def __init__(self, path:list[str], duration, departure_time, arrival_time, cost=0):
        self.path = path
        self.duration = duration
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.cost = cost

    def __str__(self):
        return "\n".join(self.path) + "\n" + f" 出发时间:{self.departure_time}, 到达时间: {self.arrival_time}, " + f" 花费: {self.cost} 元"