from datetime import date
from typing import Union

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from models import Sex
from schemas import AgeUnitEnum, HcircUnitEnum, PatientInput
from services import calculate_hcirc_percentile, is_valid_age

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


@router.post("/validate-age", response_class=HTMLResponse, include_in_schema=False)
async def validate_age(
    request: Request,
    age_value: Union[float, date] = Form(None),
    age_unit: AgeUnitEnum = Form(...),
):

    try:
        has_error, context = is_valid_age(age_value, age_unit)
        context["request"] = request

        # Decide which template to render based on age_unit
        template_name = (
            "form/input_dob.html" if age_unit == "dob" else "form/input_age.html"
        )

        return templates.TemplateResponse(template_name, context)

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="There was an unexpected error processing your request. Please try again later or contact info@gatherfoundation.ch",
        )


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
        patient_input = PatientInput(
            age_unit=AgeUnitEnum(age_unit),
            age_value=age_value,
            sex=Sex(sex),
            hcirc_value=hcirc_value,
            hcirc_unit=HcircUnitEnum(hcirc_unit),
        )

        normalized_data = patient_input.to_normalized()
        hcirc_percentile = calculate_hcirc_percentile(normalized_data)

        return templates.TemplateResponse(
            "result/hcirc_result.html",
            {
                "request": request,
                "hcirc_percentile": hcirc_percentile,
                "error_message": None,
            },
        )

    except ValueError as e:
        # Render the form with an error message and a placeholder result
        return templates.TemplateResponse(
            "result/hcirc_result.html",
            {
                "request": request,
                "hcirc_percentile": None,  # Placeholder to clear the result
                "error_message": "Please check your input and try again.",
            },
            status_code=422,
        )
    except Exception as e:
        # Render the form with a generic error message and a placeholder result
        return templates.TemplateResponse(
            "result/hcirc_result.html",
            {
                "request": request,
                "hcirc_percentile": None,  # Placeholder to clear the result
                "error_message": "There was an unexpected error processing your request. Please try again later or contact info@gatherfoundation.ch",
            },
            status_code=500,
        )


# Return Result as JSON
@router.post("/api/v1/head-circumference", response_class=JSONResponse)
async def calculate_percentile_api(patient_input: PatientInput):
    normalized_data = patient_input.to_normalized()
    hcirc_percentile = calculate_hcirc_percentile(normalized_data)
    return JSONResponse(content={"hcirc_percentile": hcirc_percentile})
