from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from app import create_app, db
from app.models import Job
from datetime import datetime, timedelta
import time

def convert_posted_text_to_date(posted_text):
    """
    Converts '2d ago', '5h ago', etc. to an actual date object.
    """
    posted_text = posted_text.lower().strip()
    try:
        if "d ago" in posted_text:
            days = int(posted_text.split('d')[0])
            return datetime.today().date() - timedelta(days=days)
        elif "h ago" in posted_text or "m ago" in posted_text:
            return datetime.today().date()
        else:
            return datetime.today().date()
    except Exception as e:
        print(f"⚠️ Could not parse date from '{posted_text}':", e)
        return datetime.today().date()

# Flask app context setup
app = create_app()
app.app_context().push()

# Selenium setup
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

# Scrape page
url = 'https://www.actuarylist.com'
print(f"🌐 Opening: {url}")
driver.get(url)
time.sleep(5)
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# Extract job listings
jobs = soup.select('.Job_job-card__YgDAV')
print(f"📦 Found {len(jobs)} job listings")

for job in jobs:
    try:
        title_elem = job.select_one('.Job_job-card__position__ic1rc')
        company_elem = job.select_one('.Job_job-card__company__7T9qY')
        location_elem = job.select_one('.Job_job-card__location__bq7jX:not(.Job_job-card__location-remote__xAjPu)')
        posted_elem = job.select_one('.Job_job-card__posted-on__NCZaJ')

        # Extract locations to detect job type
        location_links = job.select('.Job_job-card__locations__x1exr a')
        location_texts = [link.get_text(strip=True).lower() for link in location_links]

        if any('remote' in loc for loc in location_texts):
            job_type = 'Remote'
        elif any('hybrid' in loc for loc in location_texts):
            job_type = 'Hybrid'
        else:
            job_type = 'Onsite'

        # Extract tags from the tags section
        tag_links = job.select('.Job_job-card__tags__zfriA a')
        tags = ', '.join(tag.get_text(strip=True) for tag in tag_links) if tag_links else 'N/A'

        title = title_elem.get_text(strip=True) if title_elem else 'N/A'
        company = company_elem.get_text(strip=True) if company_elem else 'N/A'
        location = location_elem.get_text(strip=True) if location_elem else 'N/A'
        posted_text = posted_elem.get_text(strip=True) if posted_elem else 'N/A'
        posted_date = convert_posted_text_to_date(posted_text)

        print(f"🔍 {title} @ {company} ({location}) — {posted_text} → {posted_date} — {job_type} | Tags: {tags}")

        # Check for duplicates
        existing = Job.query.filter_by(title=title, company=company, location=location).first()
        if not existing:
            new_job = Job(
                title=title,
                company=company,
                location=location,
                posted_date=posted_date,
                job_type=job_type,
                tags=tags
            )
            db.session.add(new_job)
            print(f"✅ Added: {title}")
        else:
            print(f"⏭️ Skipped (already exists): {title}")
    except Exception as e:
        print("⚠️ Error scraping a job:", e)

db.session.commit()
print("🚀 Done scraping and inserting jobs.")
