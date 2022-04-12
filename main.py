import logging
from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db import Phonenumbers
import sms

logging.basicConfig(
    # filename=Path('app.log'),
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
    )

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

valid_phonenumbers = Phonenumbers()

companyName = "Company Name Here"

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, 
        base_grant_url: str = "https://meraki.com", 
        user_continue_url: str = "google.com", 
        node_mac: str = "00:11:22:33:44", 
        client_ip: str = "10.0.0.1", 
        client_mac: str = "99:88:77:66:55"
        ):
    return templates.TemplateResponse(
        "index.html", {
            "request": request, 
            "baseGrantURL": base_grant_url,
            "userContinueURL": user_continue_url,
            "clientIP": client_ip,
            "clientMAC": client_mac,
            "nodeMAC": node_mac
            })

@app.post("/message/", response_class=HTMLResponse)
def send_message(request: Request, 
        number: str = Form(...), 
        base_grant_url: str = Form(...),
        user_continue_url: str = Form(...),
        node_mac: str = Form(...),
        client_ip: str = Form(...),
        client_mac: str = Form(...)
        ):
    # valid_phonenumbers = Phonenumbers(number)
    if not number.startswith("+1"):
        number = f'+1{number}'
    guest_verification = valid_phonenumbers.create_validate(number=number)
    if guest_verification:
        response = sms.send_SMS(
            to_number = number,
            message_content = f"{companyName} Guest WiFi code is {guest_verification['response']}"
        )
        return templates.TemplateResponse("validate.html", {"request": request, 
            "number": number,
            "baseGrantURL": base_grant_url,
            "userContinueURL": user_continue_url,
            "clientIP": client_ip,
            "clientMAC": client_mac,
            "nodeMAC": node_mac
            })
    else:
        return templates.TemplateResponse("failure.html", {"request": request, "response": "Please join Employee Wifi."})

@app.post("/validate/", response_class=HTMLResponse)
def send_message(request: Request, 
        auth: str = Form(...),
        number: str = Form(...), 
        base_grant_url: str = Form(...),
        user_continue_url: str = Form(...),
        node_mac: str = Form(...),
        client_ip: str = Form(...),
        client_mac: str = Form(...)
        ):

    if auth:
        guest_verification = valid_phonenumbers.verify(number=number, sms_code=auth)
        if guest_verification == True:
            # Here is where I need to redirect to the base_url
            url = f'{base_grant_url}?continue_url={user_continue_url}'
            logging.info(f'Successfully auth phone number: {number}')
            return RedirectResponse(url)
        else:
            logging.info(f'Failed to auth phone number: {number}')
            return templates.TemplateResponse("failure.html", {"request": request, "response": "Denied"})
    else:
        logging.info(f'Failed to gather auth code from phone number: {number}')
        return templates.TemplateResponse("failure.html", {"request": request, "response": "Denied"})
