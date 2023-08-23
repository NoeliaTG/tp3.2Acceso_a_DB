from flask import Flask
from config import Config
def init_app():
    """Crea y configura la aplicacion Flask"""
    app = Flask(__name__, static_folder = Config.STATIC_FOLDER, template_folder = Config.TEMPLATE_FOLDER)
    app.config.from_object(Config)
    #Ejercio 1.1: Obtener un cliente.
    @app.route('/customers/<int:customer_id>')
    def cliente():            
        return 'Bienvenidx!'
    #Ejercio 1.2: Obtener el listado de clientes.
    @app.route('/customers', methods = ['GET'])
    def listado_clientes():
        return""
    #Ejercicio 1.3: Registrar un cliente.
    @app.route('/customers', methods = ['POST'])
    def aniadir_a_lista():
        return""
    #Ejercicio 1.4: Modificar un clieinte.
    @app.route('/customers/<int:customer_id>', methods = ["PUT"])
    def modificar_cliente():
        return""
    #Ejercicio 1.5: Eliminar un cliente.
    @app.route('/customers/<int:customer_id>', methods = ["DELETE"])
    def delete_customer():
        return""
    
    return app