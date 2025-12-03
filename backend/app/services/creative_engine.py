import os
import json
import asyncio
from typing import List
from fastapi import UploadFile
from app.schemas import GenerationRequest, CreativeCollection
from app.services.llm_service import llm_service
from app.services.image_service import image_service
from app.utils.file_utils import save_upload_file, create_zip_archive, cleanup_temp_files
from app.config import settings

class CreativeEngine:
    async def process_request(
        self,
        logo: UploadFile,
        product_image: UploadFile,
        request_data: GenerationRequest
    ) -> str:
        """
        Orchestrates the creative generation process.
        Returns the path to the generated ZIP file.
        """
        
        # 1. Save uploaded files
        logo_path = await save_upload_file(logo)
        product_image_path = await save_upload_file(product_image)
        
        temp_files = [logo_path, product_image_path]
        
        try:
            # 2. Call LLM for creative specs
            specs = await llm_service.generate_creative_specs(
                product_name=request_data.product_name,
                product_description=request_data.product_description,
                brand_tone=request_data.brand_tone,
                num_variants=request_data.num_variants,
                product_image_path=product_image_path
            )
            
            # 3. Generate Images
            # Create a unique folder for this batch
            batch_id = os.path.basename(logo_path).split('.')[0] # simple unique id from temp file
            batch_dir = os.path.join(settings.OUTPUT_DIR, batch_id)
            os.makedirs(batch_dir, exist_ok=True)
            
            tasks = []
            for spec in specs:
                output_image_path = os.path.join(batch_dir, spec.image_file)
                # We use product image as reference
                tasks.append(image_service.generate_image(
                    prompt=spec.image_prompt,
                    output_path=output_image_path,
                    reference_image_path=product_image_path
                ))
            
            await asyncio.gather(*tasks)
            
            # 4. Create Metadata
            collection = CreativeCollection(
                product_name=request_data.product_name or "",
                brand_tone=request_data.brand_tone or "",
                num_variants=request_data.num_variants,
                creatives=specs
            )
            
            metadata_path = os.path.join(batch_dir, "metadata.json")
            with open(metadata_path, "w") as f:
                f.write(collection.model_dump_json(indent=2))
                
            # 5. Zip it up
            zip_filename = f"creatives_{batch_id}.zip"
            zip_path = create_zip_archive(batch_dir, zip_filename)
            
            return zip_path
            
        finally:
            cleanup_temp_files(temp_files)

creative_engine = CreativeEngine()
