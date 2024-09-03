from datetime import date
from typing import Union

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from .models import Sex
from .schemas import AgeUnitEnum, HcircUnitEnum, PatientInput
from .services import calculate_hcirc_percentile, is_valid_age
from .types.message import Message
from .utils.rate_limiter import limiter

router = APIRouter()
templates = Jinja2Templates("src/templates")


############# ROOT ###############


# Root Route - Landing Page with Form
@router.get("/", response_class=HTMLResponse, include_in_schema=False)
@limiter.limit("100/minute")
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="layouts/main.html", context={"result": None}
    )


############# HEAD CIRCUMFERENCE ###############


@router.get("/show-dob", response_class=HTMLResponse, include_in_schema=False)
@limiter.limit("100/minute")
async def show_dob(request: Request):
    # Render the HTML for the Date of Birth input field
    return templates.TemplateResponse(
        request=request,
        name="forms/form_hcirc/input_dob.html",
    )


@router.get("/show-age", response_class=HTMLResponse, include_in_schema=False)
@limiter.limit("100/minute")
async def show_age(request: Request):
    # Render the HTML for the Age + Unit input field
    return templates.TemplateResponse(
        request=request,
        name="forms/form_hcirc/input_age.html",
    )


@router.post("/validate-age", response_class=HTMLResponse, include_in_schema=False)
@limiter.limit("100/minute")
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
            "forms/form_hcirc/input_dob.html"
            if age_unit == "dob"
            else "forms/form_hcirc/input_age.html"
        )

        return templates.TemplateResponse(
            request=request, name=template_name, context=context
        )

    except Exception as e:
        # Render the form with a generic error message and a placeholder result
        template_name = (
            "forms/form_hcirc/input_dob.html"
            if age_unit == "dob"
            else "forms/form_hcirc/input_age.html"
        )

        return templates.TemplateResponse(
            request=request,
            name=template_name,
            context={
                "message": Message(
                    category="error",
                    text="Something went wrong. Please try again later or contact info@gatherfoundation.ch",
                ),
            },
            status_code=500,
        )


# Display Result
@router.post(
    "/head-circumference", include_in_schema=False, response_class=HTMLResponse
)
@limiter.limit("100/minute")
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
            request=request,
            name="sections/hcirc/cards/card_result.html",
            context={
                "hcirc_percentile": hcirc_percentile,
                "message": None,
            },
        )

    except ValueError as e:
        # Render the form with an error message and a placeholder result
        return templates.TemplateResponse(
            request=request,
            name="sections/hcirc/cards/card_result.html",
            context={
                "hcirc_percentile": None,  # Placeholder to clear the result
                "message": Message(
                    category="error", text="Please check your input and try again."
                ),
            },
            status_code=422,
        )
    except Exception as e:
        # Render the form with a generic error message and a placeholder result
        return templates.TemplateResponse(
            request=request,
            name="sections/hcirc/cards/card_result.html",
            context={
                "hcirc_percentile": None,  # Placeholder to clear the result
                "message": Message(
                    category="error",
                    text="Something went wrong. Please try again later or contact info@gatherfoundation.ch",
                ),
            },
            status_code=500,
        )


# Return Result as JSON
@router.post("/api/v1/head-circumference", response_class=JSONResponse)
@limiter.limit("100/minute")
async def calculate_percentile_api(patient_input: PatientInput, request: Request):
    normalized_data = patient_input.to_normalized()
    hcirc_percentile = calculate_hcirc_percentile(normalized_data)
    return JSONResponse(content={"hcirc_percentile": hcirc_percentile})


############# OTHER ROUTES ###############


@router.get("/too-many-requests", response_class=HTMLResponse, include_in_schema=False)
async def too_many_requests(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="partials/error_429.html",
        status_code=429,
    )


@router.get("/legal", response_class=HTMLResponse, include_in_schema=False)
async def legal(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="clauses/legal.html",
        status_code=200,
    )
