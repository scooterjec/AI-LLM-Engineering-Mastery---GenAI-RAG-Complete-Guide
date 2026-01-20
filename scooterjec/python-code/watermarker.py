from PIL import Image, ImageDraw, ImageFont
import os

def add_text_watermark_to_folder(
    input_dir, out_dir, watermark_text, position, font_size=30):
        # Create output dir if it doesn't exists
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        
        for filename in os.listdir(input_dir):
            if filename.lower().endswith((".jpg", ".jpeg", )):
                image_path = os.path.join(input_dir, filename)
                original = Image.open(image_path)
                width, height = original.size
                
                print(f"Image width {width}, height {height}")

                # Create ImageDraw Object
                draw = ImageDraw.Draw(original)
                
                # set up font
                font = ImageFont.truetype("super_nough.ttf", size=font_size)
                
                #Get the test dimensions
                text_width = font.getmask(watermark_text).getbbox()[2]
                text_height = font.getmask(watermark_text).getbbox()[3]
                print(f"Text width {text_width}, height {text_height}")
                
input_directory = "./input_dir"
output_directory = "./output_dir"
watermark = "Hello"

add_text_watermark_to_folder(input_dir=input_directory, out_dir=output_directory,watermark_text=watermark,position=(50,50))
