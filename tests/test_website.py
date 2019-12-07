import time
import datetime as dt
import multiprocessing
import pathlib
import shutil

import pytest
import requests

from serverclient import run_webserver

_ADDRESS = '127.0.0.1', 8000
_URL = f'http://{_ADDRESS[0]}:{_ADDRESS[1]}'
_ROOT = pathlib.Path(__file__).absolute().parent.parent
_DATA_DIR = _ROOT / 'data'


@pytest.fixture
def webserver():
    process = multiprocessing.Process(target=run_web)
    process.start()
    time.sleep(1)
    try:
        yield
    finally:
        process.terminate()
        process.join()


def run_web():
    run_webserver(_ADDRESS, _DATA_DIR)


def test_index(webserver):
    response = requests.get(_URL)
    for user_dir in _DATA_DIR.iterdir():
        assert f'user {user_dir.name}' in response.text


def test_user(webserver):
    for user_dir in _DATA_DIR.iterdir():
        response = requests.get(f'{_URL}/users/{user_dir.name}')
        for thought_file in user_dir.iterdir():
            datetime = dt.datetime.strptime(thought_file.stem,
                                            '%Y-%m-%d_%H-%M-%S')
            assert f'User {user_dir.name}' in response.text
            assert f'{datetime:%Y-%m-%d %H:%M:%S}' in response.text
            thought_file.read_text() in response.text


def test_dynamic(webserver):
    user_id = 0
    user_dir = _DATA_DIR / str(user_id)
    user_dir.mkdir()
    try:
        datetime = dt.datetime(2000, 1, 1, 12, 0, 0)
        thought = 'Hello, world!'
        thought_file = user_dir / f'{datetime:%Y-%m-%d_%H-%M-%S}.txt'
        thought_file.write_text(thought)
        response = requests.get(_URL)
        assert f'user {user_dir.name}' in response.text
        assert f'users/{user_dir.name}' in response.text
        response = requests.get(f'{_URL}/users/{user_id}')
        assert f'User {user_dir.name}' in response.text
        assert f'{datetime:%Y-%m-%d %H:%M:%S}' in response.text
        assert thought_file.read_text() in response.text
    finally:
        shutil.rmtree(user_dir)


def test_web(webserver):
    response = requests.get(_URL)
    for user_dir in _DATA_DIR.iterdir():
        assert f'user {user_dir.name}' in response.text
    for user_dir in _DATA_DIR.iterdir():
        response = requests.get(f'{_URL}/users/{user_dir.name}')
        assert f'User {user_dir.name}' in response.text
        for thought_file in user_dir.iterdir():
            assert thought_file.read_text() in response.text
