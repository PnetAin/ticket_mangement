from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app import db
from app.models import Ticket

# Define the Blueprint first
tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/tickets', methods=['GET', 'POST'])
def manage_tickets():
    if request.method == 'POST':
        # Handle form submission
        title = request.form.get('title')
        description = request.form.get('description')
        notes = request.form.get('notes')

        # Automatically save the ticket upon creation
        new_ticket = Ticket(
            title=title,
            description=description,
            notes=notes,
            status="Open",
            saved=True  # Mark as saved
        )
        db.session.add(new_ticket)
        db.session.commit()

        # Redirect to the tickets page
        return redirect(url_for('tickets.manage_tickets'))

    # Display only unsaved tickets (if needed, you can remove this logic or handle drafts)
    tickets = Ticket.query.filter_by(saved=False).all()
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

@tickets_bp.route('/saved-tickets', methods=['GET'])
def saved_tickets():
    # Query tickets marked as saved
    tickets = Ticket.query.filter_by(saved=True).all()
    return render_template("saved_tickets.html", tickets=tickets)

@tickets_bp.route('/saved-ticket-ids', methods=['GET'])
def get_saved_ticket_ids():
    saved_tickets = Ticket.query.filter_by(saved=True).all()
    return jsonify([{"id": ticket.id, "title": ticket.title} for ticket in saved_tickets])

@tickets_bp.route('/tickets/<int:ticket_id>/edit', methods=['GET', 'POST'])
def edit_ticket(ticket_id):
    # Fetch the ticket from the database
    ticket = Ticket.query.get_or_404(ticket_id)

    if request.method == 'POST':
        # Update ticket fields with form data
        ticket.title = request.form.get('title')
        ticket.description = request.form.get('description')
        ticket.notes = request.form.get('notes')
        ticket.status = request.form.get('status', ticket.status)

        # Save changes to the database
        db.session.commit()
        return redirect(url_for('tickets.saved_tickets'))

    # Render the ticket edit page with the ticket data
    return render_template('edit_ticket.html', ticket=ticket)
