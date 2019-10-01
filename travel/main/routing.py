import main
from flask import Blueprint


vm_routes = Blueprint('/controller', __name__)

vm_routes.add_url_rule(
    'tour/create_tour',
    'tour/create_tour',
    main.add_programtour,
    methods=['POST'],
)
vm_routes.add_url_rule(
    'tour',
    'tour',
    main.select_programtour,
    methods=['GET'],
)
vm_routes.add_url_rule(
    'tour/edit_tour',
    'tour/edit_tour',
    main.put_programtour,
    methods=['PUT'],
)
vm_routes.add_url_rule(
    'tour/delete_tour',
    'tour/delete_tour',
    main.delete_programtour,
    methods=['DELETE'],
)


