from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class VideoRequest(BaseModel):
    video_url: str
    topic: str

class VideoResponse(BaseModel):
    timestamp: str
    video_url: str
    topic: str

def extract_video_id(url: str) -> str:
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
        r'youtube\.com\/embed\/([^&\n?#]+)',
        r'youtube\.com\/v\/([^&\n?#]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError("Invalid YouTube URL")

def seconds_to_hms(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

@app.post("/ask", response_model=VideoResponse)
async def find_timestamp(request: VideoRequest):
    try:
        video_id = extract_video_id(request.video_url)
        
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        transcript_text = "\n".join([
            f"[{seconds_to_hms(entry['start'])}] {entry['text']}"
            for entry in transcript
        ])
        
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": {
                    "type": "object",
                    "properties": {
                        "timestamp": {
                            "type": "string",
                            "description": "HH:MM:SS format timestamp"
                        }
                    },
                    "required": ["timestamp"]
                }
            }
        )
        
        prompt = f"""Analyze this video transcript and find when the topic "{request.topic}" is first mentioned or discussed.

Transcript:
{transcript_text}

Return ONLY the timestamp in HH:MM:SS format when this topic appears. If the topic appears multiple times, return the FIRST occurrence."""

        response = model.generate_content(prompt)
        result = eval(response.text)
        
        return VideoResponse(
            timestamp=result["timestamp"],
            video_url=request.video_url,
            topic=request.topic
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "YouTube Timestamp Finder API"}
