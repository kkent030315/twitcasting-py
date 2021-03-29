import requests
from bs4 import BeautifulSoup
import time

TWCS_STREAM_SERVER_API_ENDPOINT = "https://twitcasting.tv/streamserver.php"
TWCS_FRONTEND_API_ENDPOINT = "https://frontendapi.twitcasting.tv"


def get_stream_detail(target: str, mode: str = "client"):
    params = {
        "target": target,
        "mode": "client",
    }

    response = requests.get(TWCS_STREAM_SERVER_API_ENDPOINT, params=params)

    if (response.status_code != 200):
        raise Exception(f"ERR: Http Failed with {response.status_code}")

    return response.json()

def get_video_id(target: str):
    detail = get_stream_detail(target=target)
    return detail["movie"]["id"]


def is_user_live(target: str):
    detail = get_stream_detail(target=target)
    return detail["movie"]["live"]


def get_hls_host(target: str):
    detail = get_stream_detail(target=target)
    
    hls = detail["hls"]

    host = hls["host"]
    protocol = hls["proto"]
    source = hls["source"]

    return {
        "host": host,
        "protocol": protocol,
        "source": source,
    }


def get_fmp4_sock_address(target: str):
    detail = get_stream_detail(target=target)

    fmp4 = detail["fmp4"]

    host = fmp4["host"]
    protocol = fmp4["proto"]

    return f"{protocol}://{host}"


def get_llfmp4_sock_address(target: str, server: str = "main"):
    detail = get_stream_detail(target=target)
    return detail["llfmp4"]["streams"][server]


def is_stream_clippable(movie_id: str):
    response = requests.get(f"{TWCS_FRONTEND_API_ENDPOINT}/clip/movies/{movie_id}/clippable")

    if (response.status_code != 200):
        raise Exception(f"ERR: Http Failed with {response.status_code}")

    res_json = response.json()

    return res_json["clippable"]


def get_live_stream_info(target: str, video_id: str):
    if not video_id:
        video_id = get_video_id(target=target)
    
    params = {
        "c": "movieinfo",
        "m": video_id
    }

    response = requests.get(
        f"https://twitcasting.tv/{target}/userajax.php",
        params=params
    )

    if (response.status_code != 200):
        raise Exception(f"ERR: Http Failed with {response.status_code}")

    res_json = response.json()

    return res_json


def get_live_title(target: str, video_id: str = ""):
    detail = get_live_stream_info(target=target, video_id=video_id)

    title_raw = detail["movietitle"]
    soup = BeautifulSoup(title_raw, "html.parser")

    for element in soup(["a"]):
        return element.get_text()


def get_live_duration(target: str, video_id: str = ""):
    detail = get_live_stream_info(target=target, video_id=video_id)
    return detail["duration"]


def generate_token(video_id: str):
    timestamp = int(time.time())

    data = {
        "movie_id": video_id,
    }

    response = requests.post(
        f"https://twitcasting.tv/happytoken.php?__n={timestamp}",
        data=data,
    )

    if (response.status_code != 200):
        raise Exception(f"ERR: Http Failed with {response.status_code}")

    res_json = response.json()

    return res_json["token"]


def get_live_viewer_status(token: str, video_id: str):
    params = {
        "token": token,
        "__n": int(time.time()),
    }

    response = requests.get(
        f"{TWCS_FRONTEND_API_ENDPOINT}/movies/{video_id}/status/viewer",
        params=params,
    )

    if (response.status_code != 200):
        raise Exception(f"ERR: Http Failed with {response.status_code}")

    res_json = response.json()

    return res_json