# Marathi Font Setup Guide

## For Marathi Text to Display in PDF

You need to install `NotoSansDevanagari-Regular.ttf` font.

### Option 1: Download from Google Fonts (Recommended)

1. Visit: https://fonts.google.com/noto/specimen/Noto+Sans+Devanagari
2. Click "Download family" button
3. Extract the ZIP file
4. Find `NotoSansDevanagari-Regular.ttf`
5. Copy it to this folder: `main/fonts/NotoSansDevanagari-Regular.ttf`

### Option 2: Direct Download Links

- **Google Fonts CDN**: https://github.com/google/fonts/raw/main/ofl/notosansdevanagari/NotoSansDevanagari-Regular.ttf
- Download and save as `NotoSansDevanagari-Regular.ttf` in this folder

### Option 3: Install System-Wide (Windows)

1. Download `NotoSansDevanagari-Regular.ttf`
2. Right-click → Install
3. Copy to: `C:\Windows\Fonts\`

### Verify Installation

After placing the font file:

```bash
python manage.py runserver
# Visit: http://localhost:8000/api/members/pdf/1/
```

The PDF should display Marathi text correctly.

### If Font Not Found

- The PDF will still generate using Helvetica as fallback
- Marathi labels will show as empty boxes
- English content will display normally
- This is NOT an error - the PDF is working, just needs the font for proper rendering

### Font File Details

- **Filename**: `NotoSansDevanagari-Regular.ttf`
- **Size**: ~190 KB
- **Supports**: Devanagari script (Marathi, Hindi, Sanskrit, etc.)
- **License**: OFL (Open Font License)
