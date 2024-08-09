from fastapi import FastAPI
import uvicorn
from fastapi.responses import HTMLResponse, JSONResponse
from textSummarizer.pipeline.prediction import PredictionPipeline
from pydantic import BaseModel


class TextInput(BaseModel):
    text: str


app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def index():
    # Serve the index.html directly from the same directory as app.py
    with open("index.html") as f:
        return HTMLResponse(content=f.read())

@app.post("/predict")
async def predict_route(text: TextInput):
    try:
        obj = PredictionPipeline()
        summary = obj.predict(text.text)
        return JSONResponse({"summary": summary})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
