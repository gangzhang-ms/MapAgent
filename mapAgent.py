from datetime import datetime, timedelta

from gaodeMap import get_transit_plan, validate_transit_plan
from llm import analyze, recommand
from constants import COMPANY_LOCATION
from model import SCHEDULES, travel_model
from model import plan

today = datetime.today()

class map_agent:
    def __init__(self):
        # Initialize the agent
        pass

    def accept(self, message) -> list[plan]:
        # Process the message and return a travel_model
        model = analyze(message)
        # get plans from map api
        plans = call_map_api(model)
        if model.destination == COMPANY_LOCATION:
            for schedule in SCHEDULES:
                # reset model and message
                model_with_bus = travel_model(model.departure, schedule.station, model.time)
                transfer_plans = self.accept(str(model_with_bus))
                for plan in transfer_plans:
                    if plan.arrival_time <= schedule.start__time:
                        plan.path.append(str(schedule))
                        plan.arrival_time = schedule.arrival_time
                        plans.append(plan)
        return plans


def call_map_api(model: travel_model) -> list[plan]:
    # call gaode map api
    route = get_transit_plan(model.departure, model.destination)
    plans = []
    for can_arrive, path, duration_minutes, arrive_time, cost in validate_transit_plan(route, model.time, model.latest_arrival_time):
        if can_arrive:
            plans.append(plan(path, duration_minutes, model.time, arrive_time, cost))
    return plans

agent = map_agent()
plans = agent.accept(f'早上9点05分，从西藏南路地铁站出发，到紫星路999号')
choice = recommand(plans)
print(choice)