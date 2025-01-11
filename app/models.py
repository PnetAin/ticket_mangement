from app import db

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='Open')
    saved = db.Column(db.Boolean, default=False)  # New column
    created_at = db.Column(db.DateTime, default=db.func.now())
