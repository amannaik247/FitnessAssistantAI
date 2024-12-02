# from langflow.load import run_flow_from_json
import requests
from typing import Optional
import os
import json
from dotenv import load_dotenv

load_dotenv(override=True)


BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "5b623b45-eef7-4b18-9d8f-4a05b7ed6132"
APPLICATION_TOKEN = os.getenv("LANGFLOW_TOKEN")
APPLICATION_TOKEN_2 = os.getenv("LANGFLOW_TOKEN_2")


def dict_to_string(obj, level=0):
    strings = []
    indent = "  " * level  # Indentation for nested levels

    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                nested_string = dict_to_string(value, level + 1)
                strings.append(f"{indent}{key}: {nested_string}")
            else:
                strings.append(f"{indent}{key}: {value}")
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            nested_string = dict_to_string(item, level + 1)
            strings.append(f"{indent}Item {idx + 1}: {nested_string}")
    else:
        strings.append(f"{indent}{obj}")

    return ", ".join(strings)


# ASK AI API CALL
def ask_ai(profile, question):
    TWEAKS = {
        "TextInput-Xc2ZC": {"input_value": question},
        "TextInput-aoN0l": {"input_value": dict_to_string(profile)},
    }

    return run_flow_askai(
        "", tweaks=TWEAKS, application_token=APPLICATION_TOKEN_2, endpoint="ask-ai"
    )


def run_flow_askai(
    message: str,
    endpoint: str,
    output_type: str = "chat",
    input_type: str = "chat",
    tweaks: Optional[dict] = None,
    application_token: Optional[str] = None,
) -> dict:

    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/ask-ai"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {
            "Authorization": "Bearer " + application_token,
            "Content-Type": "application/json",
        }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()["outputs"][0]["outputs"][0]["results"]["message"]["data"][
        "text"
    ]


# MACROS API CALL
def get_macros(profile, goals):
    TWEAKS = {
        "TextInput-PVTkj": {"input_value": ", ".join(goals)},
        "TextInput-ndMS5": {"input_value": dict_to_string(profile)},
    }
    return run_flow_macros("", tweaks=TWEAKS, application_token=APPLICATION_TOKEN)


def run_flow_macros(
    message: str,
    output_type: str = "chat",
    input_type: str = "chat",
    tweaks: Optional[dict] = None,
    application_token: Optional[str] = None,
) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/macros"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {
            "Authorization": "Bearer " + application_token,
            "Content-Type": "application/json",
        }
    response = requests.post(api_url, json=payload, headers=headers)
    return json.loads(
        response.json()["outputs"][0]["outputs"][0]["results"]["message"]["data"][
            "text"
        ]
    )


# result = get_macros("name: Aman, age:21, weight: 100kg, height: 180cm", "muscle gain")
# print(result)
