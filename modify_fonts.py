#!/usr/bin/env python3
from fontTools.ttLib import TTFont
import glob
import os

# Set your desired values
TYPO_ASCENT = 1945
TYPO_DESCENT = 470
HHEA_ASCENT = 1945
HHEA_DESCENT = 470

# Define directories and their formats
font_dirs = [
    ("./fonts/webfonts", "*.woff2"),
    ("./fonts/otf", "*.otf"),
    ("./fonts/ttf", "*.ttf"),
    ("./fonts/variable", "*.ttf"),
]

def modify_font_metrics(font_path):
    """Modify font metrics and save to modified subdirectory"""
    try:
        print(f"Processing {font_path}...")
        font = TTFont(font_path)
        
        # Modify OS/2 table
        if 'OS/2' in font:
            font['OS/2'].sTypoAscender = TYPO_ASCENT
            font['OS/2'].sTypoDescender = TYPO_DESCENT
        
        # Modify hhea table
        if 'hhea' in font:
            font['hhea'].ascent = HHEA_ASCENT
            font['hhea'].descent = HHEA_DESCENT
        
        # Create output path in 'modified' subdirectory
        dir_name = os.path.dirname(font_path)
        file_name = os.path.basename(font_path)
        output_dir = os.path.join(dir_name, "modified")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, file_name)
        
        # Save with appropriate flavor for woff2
        if font_path.endswith('.woff2'):
            font.flavor = 'woff2'
        
        font.save(output_path)
        font.close()
        print(f"✓ Saved to {output_path}")
        
    except Exception as e:
        print(f"✗ Error processing {font_path}: {e}")

# Process all directories
for directory, pattern in font_dirs:
    if os.path.exists(directory):
        print(f"\n=== Processing {directory} ===")
        font_files = glob.glob(os.path.join(directory, pattern))
        
        if not font_files:
            print(f"No {pattern} files found in {directory}")
            continue
            
        for font_path in font_files:
            modify_font_metrics(font_path)
    else:
        print(f"\n⚠ Directory not found: {directory}")

print("\n=== Done! ===")