from mapAgent import map_agent

agent = map_agent()
plans = agent.accept(f'早上9点05分，从西藏南路地铁站出发，到紫星路999号')
print(plans)