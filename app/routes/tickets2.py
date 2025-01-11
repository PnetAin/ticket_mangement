from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models import Ticket

tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/tickets', methods=['GET', 'POST'])
def manage_tickets():
    if request.method == 'POST':
        data = request.json
        new_ticket = Ticket(
            title=data['title'],
            description=data.get('description'),
            notes=data.get('notes'),
            status=data.get('status', 'Open')
        )
        db.session.add(new_ticket)
        db.session.commit()
        return jsonify({"message": "Ticket created successfully"}), 201

    tickets = Ticket.query.all()
    return render_template("tickets.html", tickets=tickets)

@tickets_bp.route('/tickets/<int:ticket_id>', methods=['GET', 'PUT', 'DELETE'])
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if request.method == 'PUT':
        data = request.json
        ticket.title = data.get('title', ticket.title)
        ticket.description = data.get('description', ticket.description)
        ticket.notes = data.get('notes', ticket.notes)
        ticket.status = data.get('status', ticket.status)
        db.session.commit()
        return jsonify({"message": "Ticket updated successfully"})

    if request.method == 'DELETE':
        db.session.delete(ticket)
        db.session.commit()
        return jsonify({"message": "Ticket deleted successfully"})

    return jsonify({
        "id": ticket.id,
        "title": ticket.title,
        "description": ticket.description,
        "notes": ticket.notes,
        "status": ticket.status,
        "created_at": ticket.created_at
    })

@tickets_bp.route('/text-to-json', methods=['POST'])
def text_to_json():
    data = request.form.get('user_text')  # Get text input from form data
    if not data:
        return jsonify({"error": "No text provided"}), 400

    # Convert text to JSON structure
    json_data = {"text": data}

    return jsonify(json_data)    
