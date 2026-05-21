from app.backend.jd_fetch import fetch_jd_text_from_url
import sys

url = 'https://nz.seek.com/job/92139178?ref=saved'
text = fetch_jd_text_from_url(url)
with open('scratch/jd_seek.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print(f"JD saved to scratch/jd_seek.txt. Length: {len(text)}")

