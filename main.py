"""Fake user data

Usage example:

    python main.py --users=1 --users=2 --resources=todos

Testing:
    
    pytest main.py
"""
import json
import logging

import pytest
import requests
import typer

JSON_PLACEHOLDER_API = 'https://jsonplaceholder.typicode.com'

OUTPUT_PATH = "output.json"

LOGGING_LEVEL = "DEBUG"
LOGGING_PATH = "log.log"
LOGGING_FORMAT = '%(asctime)s; %(levelname)s %(message)s'


logging.basicConfig(level=LOGGING_LEVEL, filename=LOGGING_PATH, format=LOGGING_FORMAT)

app = typer.Typer()


def main_main(user_ids: list[str], resources: list[str]):
    logging.info("Starting")
    logging.info(f"user ids {len(user_ids)}")
    user_data = {}
    for user_id in user_ids:
        add_user_key_to_dict(user_data, user_id)
        for prop in resources:
            data = get_user_data(user_id, prop)
            user_data[user_id][prop] = data
    return user_data


def get_user_data(user_id: str, resource: list[str]):
    logging.info(f"Getting user data user_id: {user_id} resource, {resource})")
    params = {"userId": user_id}
    url = f'{JSON_PLACEHOLDER_API}/{resource}/'
    response = requests.get(url, params=params)
    data = response.json()
    logging.info(f"Data received {len(data)}")
    return data


def add_user_key_to_dict(d, user_id):
    d[user_id] = {}


def main(users: list[str] = typer.Option(None), resources: list[str] = typer.Option(None)):
    result = main_main(users, resources)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=4)


def test_add_user_key_to_dict():
    d = {}
    add_user_key_to_dict(d, "test_key")
    assert "test_key" in d


if __name__ == "__main__":
    typer.run(main)
