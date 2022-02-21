
from fastapi import FastAPI, Response, Form, Query
from pydantic import BaseModel


class Phone(BaseModel):
    phone: str


def phone_process(row_phone: str) -> str:
    clear_phone = ""
    for w in row_phone:
        if w.isdigit():
            clear_phone += w
    if (len(clear_phone) == 10 and clear_phone[0] == '9') or (
            len(clear_phone) == 11 and clear_phone[0] in ['8', '7']) or (
            (len(clear_phone) == 12 and clear_phone[0:2] in ['+7'])):
        clear_phone = clear_phone[-10:]
        return f"8 ({clear_phone[:3]}) {clear_phone[3:6]}-{clear_phone[6:8]}-{clear_phone[8:10]}"
    else:
        return clear_phone


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/unify_phone_from_json")
def get_clear_phone(phone: Phone):
    result = phone_process(phone.phone)
    return Response(content=result, media_type="text/html")


@app.post("/unify_phone_from_form")
def get_clear_phone(phone: str = Form(...)):
    result = phone_process(phone)
    return Response(content=result, media_type="text/html")


@app.get("/unify_phone_from_query")
def get_clear_phone(phone: str = Query(None)):
    result = phone_process(phone)
    return Response(content=result, media_type="text/html")
