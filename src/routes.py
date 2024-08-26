from datetime import date
from typing import Union

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from schemas import PatientInput
from services import calculate_hcirc_percentile
from utils.error_handling_utils import http_exception_handler

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
@router.post(
    "/head-circumference", include_in_schema=False, response_class=HTMLResponse
)
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
        print(hcirc_percentile)

        return templates.TemplateResponse(
            "result/hcirc_result.html",
            {"request": request, "hcirc_percentile": hcirc_percentile},
            status_code=200,
        )

    except Exception as e:
        if isinstance(e, ValueError):
            # Extract and simplify the error message
            full_message = str(e).split("\n")[2]  # Get the main error message
            simplified_message = full_message.split("[")[
                0
            ].strip()  # Remove extra details
            raise HTTPException(
                status_code=422,
                detail=simplified_message,  # Use the simplified message for the user
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="There was an unexpected error processing your request. Please try again later or contact info@gatherfoundation.ch",
            )


# Return Result as JSON
@router.post("/api/v1/head-circumference", response_class=JSONResponse)
async def calculate_percentile_api(patient_input: PatientInput):
    # patient_input is already an instance of PatientInput
    normalized_data = patient_input.to_normalized()
    hcirc_percentile = calculate_hcirc_percentile(normalized_data)
    return JSONResponse(content={"hcirc_percentile": hcirc_percentile})
