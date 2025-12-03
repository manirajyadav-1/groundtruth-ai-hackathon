from pydantic import BaseModel
from typing import List, Optional

class AdCopy(BaseModel):
    headline: str
    body: str
    cta: str

class CreativeSpec(BaseModel):
    id: int
    image_file: str
    image_prompt: str
    caption: str
    ad_copy: AdCopy

class CreativeCollection(BaseModel):
    product_name: str
    brand_tone: str
    num_variants: int
    creatives: List[CreativeSpec]

class GenerationRequest(BaseModel):
    product_name: Optional[str] = None
    product_description: Optional[str] = None
    brand_tone: Optional[str] = None
    num_variants: int = 10
