from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.config import settings
from app.services.creative_engine import creative_engine
from app.schemas import GenerationRequest
import os

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}

@app.post("/generate-creatives")
async def generate_creatives(
    logo: UploadFile = File(...),
    product_image: UploadFile = File(...),
    product_name: str = Form(...),
    product_description: str = Form(...),
    brand_tone: str = Form(...),
    num_variants: int = Form(10)
):
    try:
        request_data = GenerationRequest(
            product_name=product_name,
            product_description=product_description,
            brand_tone=brand_tone,
            num_variants=num_variants
        )
        
        zip_path = await creative_engine.process_request(logo, product_image, request_data)
        
        return FileResponse(
            path=zip_path, 
            filename=os.path.basename(zip_path),
            media_type='application/zip'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
