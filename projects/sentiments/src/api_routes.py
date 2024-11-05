from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from sentiment_analysis import SentimentAnalysis, SentimentAnalysisResult
from error_handling import ErrorHandling

# Create an APIRouter instance
router = APIRouter()

# Define the Pydantic model for the sentiment analysis request
class TextAnalysisRequest(BaseModel):
    text: str

# Dependency to handle validation errors
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return await ErrorHandling.handle_validation_error(request, exc)

@router.post("/analyze-sentiment", response_model=SentimentAnalysisResult, dependencies=[Depends(validation_exception_handler)])
async def analyze_sentiment(text_analysis_request: TextAnalysisRequest):
    try:
        # Instantiate the SentimentAnalysis class
        sentiment_analyzer = SentimentAnalysis()
        # Perform sentiment analysis on the input text
        result = sentiment_analyzer.analyze(text_analysis_request.text)
        # Map the 'negative' and 'positive' values from the analysis to the corresponding fields in the model
        negative = result.get('negative', 0.0)
        positive = result.get('positive', 0.0)
        # Return the results in JSON format
        return SentimentAnalysisResult(negative=negative, positive=positive)
    except ValidationError as e:
        # Handle validation errors specifically
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        # Raise the HTTPException to be handled by the global exception handler
        raise e
    except Exception as e:
        # Raise a generic server error HTTPException
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail='An unexpected error occurred on the server.')
