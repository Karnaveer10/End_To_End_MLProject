from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# -------------------- APP SETUP --------------------

app = FastAPI()

# Tell FastAPI where HTML templates are stored
templates = Jinja2Templates(directory="templates")


# -------------------- HOME PAGE (REDIRECT) --------------------

@app.get("/", response_class=RedirectResponse)
async def home():
    """
    Redirect to the prediction form
    """
    return RedirectResponse(url="/predictdata")


# -------------------- PREDICTION FORM --------------------

@app.get("/predictdata", response_class=HTMLResponse)
async def show_form(request: Request):
    """
    Show the prediction form (home.html)
    """
    return templates.TemplateResponse(
        "home.html",
        {"request": request}
    )


# -------------------- FORM SUBMISSION --------------------

@app.post("/predictdata", response_class=HTMLResponse)
async def predict(
    request: Request,
    gender: str = Form(...),
    ethnicity: str = Form(...),
    parental_level_of_education: str = Form(...),
    lunch: str = Form(...),
    test_preparation_course: str = Form(...),
    writing_score: float = Form(...),
    reading_score: float = Form(...),
):
    """
    Handle form data, run prediction, show result
    """

    # 1. Convert form data into CustomData object
    data = CustomData(
        gender=gender,
        race_ethnicity=ethnicity,
        parental_level_of_education=parental_level_of_education,
        lunch=lunch,
        test_preparation_course=test_preparation_course,
        reading_score=writing_score,   # keeping your original mapping
        writing_score=reading_score,
    )

    # 2. Convert data to DataFrame
    input_df = data.get_data_as_data_frame()

    # 3. Make prediction
    model = PredictPipeline()
    prediction = model.predict(input_df)

    # 4. Show result on the same page
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "results": prediction[0]
        }
    )