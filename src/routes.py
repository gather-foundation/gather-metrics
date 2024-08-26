from datetime import date
from typing import Union

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from schemas import NormalizedPatientData, PatientInput
from services import calculate_hcirc_percentile

router = APIRouter()
templates = Jinja2Templates("src/templates")


############# ROOT ###############


# Root Route - Landing Page with Form
@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root(request: Request):
    return templates.TemplateResponse("main.html", {"request": request, "result": None})


############# HEAD CIRCUMFERENCE ###############


@router.get("/show-dob", response_class=HTMLResponse, include_in_schema=False)
async def show_dob(request: Request):
    # Render the HTML for the Date of Birth input field
    return templates.TemplateResponse("form/input_dob.html", {"request": request})


@router.get("/show-age", response_class=HTMLResponse, include_in_schema=False)
async def show_age(request: Request):
    # Render the HTML for the Age + Unit input field
    return templates.TemplateResponse("form/input_age.html", {"request": request})


# Display Result
@router.post("/head-circumference", include_in_schema=False)
async def display_result(
    request: Request,
    age_unit: str = Form(...),
    age_value: Union[date, float] = Form(...),
    sex: str = Form(...),
    hcirc_value: float = Form(...),
    hcirc_unit: str = Form(...),
):
    try:
        # Create PatientInput instance
        patient_input = PatientInput(
            age_unit=age_unit,
            age_value=age_value,
            sex=sex,
            hcirc_value=hcirc_value,
            hcirc_unit=hcirc_unit,
        )

        # Normalize the data
        normalized_data = patient_input.to_normalized()
        hcirc_percentile = calculate_hcirc_percentile(normalized_data)

        # Assume a successful response returns a results partial
        return templates.TemplateResponse(
            "hcirc_result.html",
            {"request": request, "hcirc_percentile": hcirc_percentile},
        )
    except Exception as e:
        # Return the error partial if there's an error
        return templates.TemplateResponse(
            "shared/error_banner.html",
            {"request": request, "error_message": str(e)},
            status_code=400,
        )


# Return Result as JSON
@router.post("/api/v1/head-circumference", response_class=JSONResponse)
async def calculate_percentile_api(patient_input: PatientInput):
    # patient_input is already an instance of PatientInput
    normalized_data = patient_input.to_normalized()
    hcirc_percentile = calculate_hcirc_percentile(normalized_data)
    return JSONResponse(content={"hcirc_percentile": hcirc_percentile})
