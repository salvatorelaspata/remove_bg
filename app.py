from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import io
from PIL import Image
from rembg import remove

app = FastAPI()

@app.post("/convert")
async def remove_background(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(
            status_code=400, detail="Il file deve essere un'immagine JPG o PNG."
        )
    try:
        contents = await file.read()
        # Apri l'immagine
        input_image = Image.open(io.BytesIO(contents))
        # Rimuovi lo sfondo
        output_image = remove(input_image)
        # Salva l'output in un buffer
        output = io.BytesIO()
        output_image.save(output, format="PNG")
        output.seek(0)
        return StreamingResponse(output, media_type="image/png")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Errore durante la rimozione dello sfondo: {e}"
        )


@app.get("/")
async def read_root():
    return {"welcome": "Remove Background API"}


@app.get("/{path:path}")
async def read_path(path: str):
    raise HTTPException(status_code=404, detail="Route not found for path: " + path)
