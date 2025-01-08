import datetime as dt
import json
import os
import re

import feedparser
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse
from pycomcigan import TimeTable
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/timetable")
async def main(grade: int, classnum: int):
    td = {"Monday": "", "Tuesday": "", "Wednesday": "", "Thursday": "", "Friday": ""}
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    timetable = TimeTable("근명고등학교", week_num=0)

    for i in range(0, 5):
        td[days[i]] = timetable.timetable[grade][classnum][i + 1]

    return td


@app.get("/mealimg")
async def mealimg():
    today_str = dt.datetime.now().strftime("%Y-%m-%d")
    data = {}
    if os.path.exists("mealimg.json"):
        with open("mealimg.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    if today_str in data:
        return PlainTextResponse(data[today_str])

    img_url: str
    rss_url = "https://kmh-h.goeay.kr/kmh-h/na/ntt/selectRssFeed.do?mi=5589&bbsId=2405"
    date_now = dt.datetime.now()
    date_kor = f"{date_now.month}월{date_now.day}일"
    rss_data = feedparser.parse(rss_url)["entries"]
    count = 0

    # debug
    # date_kor = "1월7일"

    # noinspection PyTypeChecker
    for i in rss_data:
        if re.search(r"^\[메뉴사진].*$", i["title"]) and count == 0:
            url = i["link"].replace("/kmh-h/na/ntt/kmh-h/na/ntt/", "/kmh-h/na/ntt/")
            response = requests.get(url)
            html = BeautifulSoup(response.text, "html.parser")
            try:
                # noinspection PyUnresolvedReferences
                img_url = (
                    "https://kmh-h.goeay.kr" + html.find("img", alt=date_kor)["src"]
                )
                data[today_str] = img_url
                with open("mealimg.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False)
                count += 1
            except TypeError:
                return JSONResponse(
                    status_code=404,
                    content={"message": "이미지 URL을 찾을 수 없습니다."},
                )
            return PlainTextResponse(img_url)
