import os
from PIL import Image
from pathlib import Path

def optimize_image(input_path, output_path, max_size=(1200, 800), quality=85):
    """Resize and compress an image while maintaining aspect ratio."""
    with Image.open(input_path) as img:
        # Convert to RGB if necessary (for PNG with transparency)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        # Calculate new size maintaining aspect ratio
        ratio = min(max_size[0]/img.size[0], max_size[1]/img.size[1])
        new_size = (int(img.size[0]*ratio), int(img.size[1]*ratio))

        # Resize image
        img = img.resize(new_size, Image.Resampling.LANCZOS)

        # Save with compression
        img.save(output_path, quality=quality, optimize=True)

def main():
    # Create images directory if it doesn't exist
    images_dir = Path('images')
    images_dir.mkdir(exist_ok=True)

    # Process all images in the directory
    for img_path in images_dir.glob('*'):
        if img_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
            # Create optimized version
            optimized_path = img_path.parent / f"{img_path.stem}_optimized{img_path.suffix}"
            print(f"Optimizing {img_path.name}...")
            optimize_image(img_path, optimized_path)

            # Replace original with optimized version
            os.replace(optimized_path, img_path)
            print(f"Done: {img_path.name}")

if __name__ == '__main__':
    main()