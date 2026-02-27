import os
import json
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, conint
from openai import OpenAI
from dotenv import load_dotenv


class CommentIn(BaseModel):
    comment: str = Field(..., min_length=1, description="Customer comment to analyze")


class SentimentOut(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    rating: conint(ge=1, le=5)  # type: ignore[valid-type]


load_dotenv()  # Load environment variables from a local .env file if present

app = FastAPI(title="Structured Sentiment API")


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Server misconfiguration: OPENAI_API_KEY is not set.",
        )
    return OpenAI(api_key=api_key)


STRUCTURED_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "sentiment_response",
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "sentiment": {
                    "type": "string",
                    "enum": ["positive", "negative", "neutral"],
                    "description": "Overall sentiment of the comment",
                },
                "rating": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 5,
                    "description": "Sentiment intensity (5=highly positive, 1=highly negative)",
                },
            },
            "required": ["sentiment", "rating"],
        },
        "strict": True,
    },
}


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": 'POST /comment with JSON {"comment": "This product is amazing!"}',
    }


@app.post("/comment", response_model=SentimentOut)
async def analyze_comment(payload: CommentIn):
    comment = (payload.comment or "").strip()
    if not comment:
        raise HTTPException(status_code=400, detail="Field 'comment' must be a non-empty string")

    client = get_client()

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict sentiment analysis service. Determine the overall sentiment (positive, negative, neutral) and an intensity rating from 1-5 (5=highly positive, 1=highly negative).",
                },
                {
                    "role": "user",
                    "content": f'Comment: "{comment}"',
                },
            ],
            response_format=STRUCTURED_SCHEMA,
        )

        # Extract the structured JSON response
        message = resp.choices[0].message
        if not message.content:
            raise HTTPException(status_code=502, detail="LLM returned empty response")

        # Parse and validate against our Pydantic response model
        data = json.loads(message.content)
        result = SentimentOut(**data)

        return JSONResponse(content=result.dict())

    except HTTPException:
        raise
    except Exception as e:
        # Graceful error for upstream/SDK issues
        raise HTTPException(status_code=502, detail=f"Upstream AI failure: {e}")
