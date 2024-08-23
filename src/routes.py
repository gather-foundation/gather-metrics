from datetime import date
from typing import Union

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from schemas import NormalizedPatientData, PatientInput
from services import calculate_hcirc_percentile

router = APIRouter()
templates = Jinja2Templates("src/templates")

############# ROOT ###############


# Root Route - Landing Page with Form
@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("main.html", {"request": request, "result": None})


############# HEAD CIRCUMFERENCE ###############


# Display Result
@router.post("/head-circumference")
async def display_result(
    request: Request,
    age_unit: str = Form(...),
    age_value_float: Union[float, None] = Form(None),
    age_value_date: Union[date, None] = Form(None),
    sex: str = Form(...),
    hcirc_value: float = Form(...),
    hcirc_unit: str = Form(...),
):
    # Create PatientInput instance
    patient_input = PatientInput(
        age_unit=age_unit,
        age_value_float=age_value_float,
        age_value_date=age_value_date,
        sex=sex,
        hcirc_value=hcirc_value,
        hcirc_unit=hcirc_unit,
    )

    # Normalize the data
    normalized_data = patient_input.to_normalized()
    hcirc_percentile = calculate_hcirc_percentile(normalized_data)
    return templates.TemplateResponse(
        "hcirc_result.html",
        {"request": request, "hcirc_percentile": hcirc_percentile},
    )


# Return Result as JSON
@router.post("/api/v1/head-circumference", response_class=JSONResponse)
async def calculate_percentile_api(patient_input: NormalizedPatientData):
    hcirc_percentile = calculate_hcirc_percentile(patient_input)
    return JSONResponse(content={"hcirc_percentile": hcirc_percentile})
