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
vm_routes.add_url_rule(
    'register',
    'register_users',
    main.register_user,
    methods=['POST'],
)
vm_routes.add_url_rule(
    'users',
    'select_user',
    main.select_user,
    methods=['GET'],
)
vm_routes.add_url_rule(
    'allusers',
    'selectall_user',
    main.selectall_user,
    methods=['GET'],
)
vm_routes.add_url_rule(
    'users',
    'update_users',
    main.update_user,
    methods=['PUT'],
)
vm_routes.add_url_rule(
    'login',
    'login',
    main.login,
    methods=['GET'],
)



