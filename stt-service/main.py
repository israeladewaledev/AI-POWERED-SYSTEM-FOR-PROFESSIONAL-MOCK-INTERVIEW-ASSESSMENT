import os
from fastapi import FastAPI, UploadFile, File
from faster_whisper import WhisperModel
import uvicorn
import shutil
import tempfile

app = FastAPI()

# Initialize Whisper model (using "tiny" or "base" for faster CPU performance)
model_size = "base"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp_file:
        shutil.copyfileobj(file.file, tmp_file)
        tmp_path = tmp_file.name

    try:
        # Transcribe audio
        segments, info = model.transcribe(tmp_path, beam_size=5)
        text = " ".join([segment.text for segment in segments])
        
        return {"text": text.strip()}
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
