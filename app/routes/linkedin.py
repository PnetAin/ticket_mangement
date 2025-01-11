from flask import Blueprint, request, jsonify
from app.utils.linkedin_api import publish_linkedin_post
from app.models import Ticket

linkedin_bp = Blueprint('linkedin', __name__)

@linkedin_bp.route('/linkedin/post', methods=['POST'])
def create_linkedin_post():
    ticket_id = request.json.get('ticket_id')
    ticket = Ticket.query.get_or_404(ticket_id)

    # Draft content based on ticket notes
    content = f"Resolved Issue: {ticket.title}\n\n{ticket.notes}"
    response = publish_linkedin_post("your_access_token", content)
    return jsonify(response)
