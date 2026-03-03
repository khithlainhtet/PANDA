# Copyright (c) 2026 khithlainhtet
# Licensed under the MIT License.
# This file is part of PANDAMusic


import os
import aiohttp
import traceback
from PIL import (Image, ImageDraw, ImageEnhance,
                 ImageFilter, ImageFont, ImageOps)
from PANDA import config
from PANDA.helpers import Track

class Thumbnail:
    def __init__(self):
        
        self.canvas_size = (1280, 720)
        self.fill = (255, 255, 255)
        
        
        self.font_main = ImageFont.truetype("PANDA/helpers/Raleway-Bold.ttf", 45)
        self.font_sub = ImageFont.truetype("PANDA/helpers/Inter-Light.ttf", 32)
        
        self.font_footer = ImageFont.truetype("PANDA/helpers/Inter-Light.ttf", 25)

    async def save_thumb(self, output_path: str, url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                with open(output_path, "wb") as f:
                    f.write(await resp.read())
            return output_path

    async def generate(self, song: Track) -> str:
        try:
            temp = f"cache/temp_{song.id}.jpg"
            output = f"cache/{song.id}.png"
            if os.path.exists(output):
                return output

            await self.save_thumb(temp, song.thumbnail)
            base_img = Image.open(temp).convert("RGBA")
            
            
            image = base_img.resize(self.canvas_size, Image.LANCZOS)
            
            
            image = image.filter(ImageFilter.GaussianBlur(radius=40))
            
            
            image = ImageEnhance.Color(image).enhance(0.7)
            
            
            image = ImageEnhance.Brightness(image).enhance(0.5)

            
            
            overlay = Image.new("RGBA", self.canvas_size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            for i in range(720):
                
                alpha = int((i / 720) ** 2 * 220) 
                draw.line([(0, i), (1280, i)], fill=(0, 0, 0, alpha))
            image = Image.alpha_composite(image, overlay)

            draw = ImageDraw.Draw(image)

            # 3. Floating Card Overlay (Mini Player Bar)
            
            bar_bg_color = (30, 30, 30, 190) 
            draw.rounded_rectangle([200, 480, 1080, 650], radius=35, fill=bar_bg_color)

            
            art_size = 400
            _art = base_img.resize((art_size, art_size), Image.LANCZOS)
            
            # Rounded Corners for Art
            art_mask = Image.new("L", (art_size, art_size), 0)
            ImageDraw.Draw(art_mask).rounded_rectangle((0, 0, art_size, art_size), radius=45, fill=255)
            _art.putalpha(art_mask)
            
            # ပုံကို Player Bar ရဲ့ အပေါ်မှာ တင်မယ်
            image.paste(_art, (440, 60), _art)

            # 5. Text Elements & Icons (Now Playing Area)
            # Now Playing Text
            np_text = "🎧Now Playing🎧"
            draw.text((250, 500), np_text, font=self.font_main, fill=self.fill)
            
            # Progress Bar (သီချင်း bar တန်းလေး)
            draw.rounded_rectangle([250, 560, 1030, 566], radius=3, fill=(90, 90, 90)) # Background bar
            draw.rounded_rectangle([250, 560, 650, 566], radius=3, fill=(255, 120, 120)) # Progress bar (ပန်းရောင်/နီရောင်လိုင်း)

            # Time Markers
            draw.text((250, 580), "0:45", font=self.font_sub, fill=(200, 200, 200))
            dur_w = draw.textlength(song.duration, font=self.font_sub)
            draw.text((1030 - dur_w, 580), song.duration, font=self.font_sub, fill=(200, 200, 200))

            # 6. Footer Text (Powered By)
            your_name = "HANTHAR999"
            footer_text = f"Made by {your_name} X MUSIC"
            f_w = draw.textlength(footer_text, font=self.font_footer)
            draw.text(((1280 - f_w) // 2, 680), footer_text, font=self.font_footer, fill=(200, 200, 200))

            # 7. Final Save
            image.save(output)
            os.remove(temp)
            return output
        except Exception:
            print(traceback.format_exc())
            return config.DEFAULT_THUMB
