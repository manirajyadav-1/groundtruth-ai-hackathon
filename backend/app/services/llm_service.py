import json
import os
from typing import List
from PIL import Image
from app.schemas import CreativeSpec, AdCopy, CreativeCollection
from app.config import settings
from google import genai
from google.genai import types

class LLMService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        if not self.api_key:
            print("WARNING: GEMINI_API_KEY not found in environment variables.")
        self.client = genai.Client(api_key=self.api_key)

    async def generate_creative_specs(
        self, 
        product_name: str, 
        product_description: str, 
        brand_tone: str, 
        num_variants: int,
        product_image_path: str
    ) -> List[CreativeSpec]:
        
        print(f"Analyzing product image for {product_name}...")
        
        try:
            # Load image
            image = Image.open(product_image_path)
            
            prompt = f"""
            You are an elite creative director.
            Analyze the provided product image to understand the product details, aesthetics, and unique selling points.
            
            Context:
            - Product Name: {product_name}
            - Product Description: {product_description}
            - Brand Tone: {brand_tone}
            
            Your task is to generate {num_variants} unique creative concepts for a digital marketing campaign.
            For each concept, you must provide a detailed `image_prompt` that will be fed into an AI Image Generator (like Flux/Stable Diffusion) to create the final ad creative.
            
            The `image_prompt` must adhere to these Creative Requirements:
            1. Use the product as the main subject. Describe the product visually based on your analysis (color, shape, material) so the image generator can recreate it (or a close likeness).
            2. Incorporate the brand logo subtly if possible (e.g., "logo watermark in corner" or "branded packaging").
            3. Maintain a clean composition with strong visual hierarchy.
            4. Add a visually appealing background that fits the style (avoid clutter, use lighting/gradients).
            5. Match the Brand Tone:
               - If "{brand_tone}" implies Luxury -> soft lighting, dark backgrounds, metallic accents.
               - If "{brand_tone}" implies Minimal -> clean white/pastel backgrounds, simple layout.
               - If "{brand_tone}" implies Energetic -> vibrant colors, dynamic shapes, playful glow.
            6. Ensure the product looks sharp, clear, and professionally lit.
            7. Specify high-resolution, aesthetic, 4:5 aspect ratio style.
            
            For each variant, vary the following elements:
            - Background color & texture
            - Lighting style (e.g., cinematic, studio, natural, neon)
            - Camera angle or perspective (e.g., eye-level, low angle, top-down flat lay)
            - Color palette (aligned with brand tone)
            - Composition/layout style
            
            For each concept, provide:
            1. `image_prompt`: The detailed prompt for the image generator. Include all visual details, lighting, style, and quality boosters (e.g., "8k", "photorealistic").
            2. `caption`: A catchy social media caption with hashtags.
            3. `headline`: A punchy ad headline (max 10 words).
            4. `body`: Persuasive ad body copy (1-2 sentences).
            5. `cta`: A strong Call to Action.

            Return the response ONLY as a valid JSON array of objects. 
            Do not include markdown formatting like ```json ... ```.
            Format:
            [
              {{
                "image_prompt": "...",
                "caption": "...",
                "headline": "...",
                "body": "...",
                "cta": "..."
              }}
            ]
            """
            
            response = self.client.models.generate_content(
                model='gemini-2.5-flash', # Using a capable multimodal model
                contents=[prompt, image],
                config=types.GenerateContentConfig(
                    response_mime_type='application/json'
                )
            )
            
            # Parse JSON response
            try:
                raw_json = response.text
                # Clean up if markdown is present (just in case)
                if raw_json.startswith("```json"):
                    raw_json = raw_json[7:]
                if raw_json.endswith("```"):
                    raw_json = raw_json[:-3]
                    
                data = json.loads(raw_json)
                
                specs = []
                for i, item in enumerate(data):
                    specs.append(CreativeSpec(
                        id=i+1,
                        image_file=f"creative_{i+1:02d}.png",
                        image_prompt=item.get("image_prompt", ""),
                        caption=item.get("caption", ""),
                        ad_copy=AdCopy(
                            headline=item.get("headline", ""),
                            body=item.get("body", ""),
                            cta=item.get("cta", "")
                        )
                    ))
                
                # Ensure we have the requested number (or at least some)
                return specs[:num_variants]
                
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON from Gemini: {e}")
                print(f"Raw response: {response.text}")
                # Fallback to mock if parsing fails
                return self._get_mock_specs(num_variants, product_name, brand_tone)

        except Exception as e:
            print(f"Error calling Gemini: {e}")
            return self._get_mock_specs(num_variants, product_name, brand_tone)

    def _get_mock_specs(self, num_variants, product_name, brand_tone):
        print("Falling back to mock specs...")
        specs = []
        for i in range(num_variants):
            specs.append(CreativeSpec(
                id=i+1,
                image_file=f"creative_{i+1:02d}.png",
                image_prompt=f"Professional photo of {product_name}, {brand_tone} style, high quality, 4k",
                caption=f"Experience the best {product_name} today!",
                ad_copy=AdCopy(
                    headline=f"New {product_name}",
                    body=f"This is the best {product_name} you can find.",
                    cta="Shop Now"
                )
            ))
        return specs

llm_service = LLMService()
