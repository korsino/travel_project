from .app import app
from .main.routing import vm_routes as vm_route

def root_endpoint():
    return 'ยินดีต้อนรับ พอเพียงทัวรี่'

def init_routes():
    app.add_url_rule( '/',
                      'root_endpoint',
                      root_endpoint,
                      methods=['GET'],
                    )
    app.register_blueprint(vm_route, url_prefix="/")

