from flask import Blueprint, request, jsonify, send_from_directory, current_app
from .models import Job
from .database import db

api = Blueprint('api', __name__)

@api.route('/jobs', methods=['POST'])
def create_job():
    data = request.get_json()
    job = Job(**data)
    db.session.add(job)
    db.session.commit()
    return jsonify({'message': 'Job created', 'job': data}), 201

@api.route('/jobs', methods=['GET'])
def list_jobs():
    query = Job.query

    # Filtering
    job_type = request.args.get('job_type')
    location = request.args.get('location')
    tag = request.args.get('tag')

    if job_type:
        query = query.filter(Job.job_type.ilike(f"%{job_type}%"))
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if tag:
        query = query.filter(Job.tags.ilike(f"%{tag}%"))

    # Sorting
    sort = request.args.get('sort', 'posting_date_desc')
    if sort == 'posting_date_asc':
        query = query.order_by(Job.id.asc())  # Use Job.posting_date.asc() if you have a posting_date field
    else:
        query = query.order_by(Job.id.desc())  # Default: newest first

    jobs = query.all()
    return jsonify([{
        'id': j.id,
        'title': j.title,
        'company': j.company,
        'location': j.location,
        'posted_date': j.posted_date.isoformat() if j.posted_date else None,
        'job_type': j.job_type,
        'tags': j.tags
    } for j in jobs]), 200

@api.route('/jobs/<int:id>', methods=['GET'])
def get_job(id):
    job = Job.query.get_or_404(id)
    return jsonify({
        'id': job.id,
        'title': job.title,
        'company': job.company,
        'location': job.location,
        'posted_date': job.posted_date.isoformat() if job.posted_date else None,
        'job_type': job.job_type,
        'tags': job.tags
    })


@api.route('/jobs/<int:id>', methods=['PUT', 'PATCH'])
def update_job(id):
    job = Job.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(job, key, value)
    db.session.commit()
    return jsonify({'message': 'Job updated'})

@api.route('/jobs/<int:id>', methods=['DELETE'])
def delete_job(id):
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    return jsonify({'message': 'Job deleted'})

@api.route('/')
def serve_index():
    return send_from_directory('../templates', 'index.html')

@api.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(current_app.static_folder, filename)
