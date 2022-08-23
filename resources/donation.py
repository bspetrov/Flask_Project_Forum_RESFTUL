from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.donation_manager import DonationManager
from schemas.requests.donation import DonationSchemaRequest
from utils.decorators import validate_schema


class DonationResource(Resource):
    @validate_schema(DonationSchemaRequest)
    @auth.login_required
    def post(self):
        data = request.get_json()
        forum_user = auth.current_user()
        full_name = f"{forum_user.first_name} {forum_user.last_name}"
        donation = DonationManager.issue_transaction(data["amount"], full_name, data["iban"], data["description"], forum_user.id)
        return donation
