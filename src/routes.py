from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from schemas import NormalizedPatientData
from services import calculate_hcirc_percentile

router = APIRouter()
templates = Jinja2Templates("src/templates")

############# ROOT ###############


# Root Route - Landing Page with Form
@router.get("/")
async def root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


############# HEAD CIRCUMFERENCE ###############


# HTML Route - Display Result
@router.post("/head-circumference")
async def display_result(request: Request, patient_input: NormalizedPatientData):
    hcirc_percentile = calculate_hcirc_percentile(patient_input)
    return templates.TemplateResponse(
        "hcirc_result.html",
        {"request": request, "hcirc_percentile": hcirc_percentile},
    )


# API JSON Route - Return Result as JSON
@router.post("/api/v1/head-circumference")
async def calculate_percentile_api(patient_input: NormalizedPatientData):
    hcirc_percentile = calculate_hcirc_percentile(patient_input)
    return JSONResponse(content={"hcirc_percentile": hcirc_percentile})
