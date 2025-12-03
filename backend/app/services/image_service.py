import os
import httpx
import urllib.parse
from PIL import Image
from io import BytesIO
from app.config import settings

class ImageService:
    def __init__(self):
        # Pollinations.ai usually works without a key, but we'll include the token if provided.
        pass

    async def generate_image(self, prompt: str, output_path: str, reference_image_path: str = None):
        print(f"Generating image for prompt: {prompt}")
        
        try:
            # Construct URL
            # https://enter.pollinations.ai/api/generate/image/{prompt}
            encoded_prompt = urllib.parse.quote(prompt)
            base_url = f"https://pollinations.ai/p/{encoded_prompt}" 
          
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
           
            
            params = {
                "model": "flux",
                "width": 1024,
                "height": 1024,
                "seed": 42,
                "nologo": "true"
            }
            
            # We'll use the robust public endpoint which redirects to the image
            final_url = f"https://pollinations.ai/p/{encoded_prompt}"
            
            
            async with httpx.AsyncClient() as client:
                response = await client.get(final_url, params=params, follow_redirects=True, timeout=60.0)
                
                if response.status_code == 200:
                    image_data = response.content
                    image = Image.open(BytesIO(image_data))
                    image.save(output_path)
                    print(f"Saved image to {output_path}")
                else:
                    print(f"Failed to generate image: {response.status_code} - {response.text}")
                    # Fallback
                    img = Image.new('RGB', (1024, 1024), color = (100, 255, 100))
                    img.save(output_path)

        except Exception as e:
            print(f"Error generating image: {e}")
            # Fallback
            img = Image.new('RGB', (1024, 1024), color = (255, 100, 100))
            img.save(output_path)

image_service = ImageService()
