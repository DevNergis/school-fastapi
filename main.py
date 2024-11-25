from fastapi import *
from pycomcigan import TimeTable


app = FastAPI()


@app.get("/")
async def main(grade: int, classnum: int):
    td = {'Monday': '', 'Tuesday': '', 'Wednesday': '', 'Thursday': '', 'Friday': ''}
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    # 시간표 가져오기
    # week_num: 0이면 이번주, 1이면 다음주
    timetable = TimeTable("근명고등학교", week_num=0)

    for i in range(0, 5):
        td[days[i]] = timetable.timetable[grade][classnum][i+1]

    return td
