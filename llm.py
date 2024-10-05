from datetime import datetime
import requests
import os
from openai import AzureOpenAI
from model import travel_model
from model import plan

# Configuration
API_KEY = ""
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}

# Payload for the request
payload = {
  "messages": [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "You are an map assistant that helps people to travel. People will tell you their travel plan and you task is to extract any main elements from their plan following including departure place, departure time, target place and so on. You also need to find the most convenient way about people's travel plan."
        }
      ]
    }
  ]
}

endpoint = os.getenv("ENDPOINT_URL", "https://infea-m1ps365l-australiaeast.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o")

client = AzureOpenAI(
      azure_endpoint=endpoint,
      api_key=os.getenv("openAI_key", API_KEY),
      api_version="2024-05-01-preview",
  )

test_source = 'South Xizang Road'
test_target = 'No.999 Zixing Road'
test_time = '9:00 AM'
today = datetime.today()
time_format = '%Y-%m-%d %H:%M'

def analyze(message: str) -> travel_model:
    # call llm to analyze the message and return travel model
    # Send request
    try:
        req = message + f". Please find three fields with just value:'departure Place', 'departure time' and 'target place' for me. The value of 'daparture time' should follow the format of {time_format}. You can suppose today as the day of 'departure time'. Do not return any other information. For example: context: '早上7点40, 从西藏南路出发, 到紫星路999号'. We should return following response:西藏南路\n2023-10-03 07:40\n紫星路999号'"
        payload["messages"].append({"role": "user", "content": [{"type": "text", "text": req}]})
        response = client.chat.completions.create(model=deployment, messages=payload["messages"], temperature=1.0)
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")
    # Handle the response as needed (e.g., print or process)
    content = response.choices[0].message.content
    lines = content.split("\n")
    time = datetime.strptime(lines[1].strip(), time_format)
    setoff_time = datetime(today.year, today.month, today.day, time.hour, time.minute, time.second)
    return travel_model(lines[0].strip(), lines[2].strip(), setoff_time)

def recommand(plans: list[plan]):
    # recommend the best plan from plans
    message = '\n'.join([str(p) for p in plans])
    try:
        req = f"Please recommend only one best plan from the following plans:\n{message}.\n Each plan should follow the format of '出发时间', '到达时间','花费' and '详细路线'"
        payload["messages"].append({"role": "user", "content": [{"type": "text", "text": req}]})
        response = client.chat.completions.create(model=deployment, messages=payload["messages"], temperature=1.0)
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")
    # Handle the response as needed (e.g., print or process)
    content = response.choices[0].message.content
    return content


if __name__ == "__main__":
    model = analyze(f'Set off from: {test_source} at {test_time} and got to {test_target}')
    print(model)

