from .database import db
from datetime import date

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    posted_date = db.Column(db.Date, default=date.today)  # actual date
    job_type = db.Column(db.String(50))
    tags = db.Column(db.String(255))
