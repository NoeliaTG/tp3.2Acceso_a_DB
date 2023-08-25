from flask import Flask, request
from config import Config
from .database import DatabaseConnection

def init_app():
    """Crea y configura la aplicacion Flask"""
    app = Flask(__name__, static_folder = Config.STATIC_FOLDER, template_folder = Config.TEMPLATE_FOLDER)
    app.config.from_object(Config)
    #Ejercio 1.1: Obtener un cliente.
    @app.route('/customers/<int:customer_id>', methods = ['GET'])
    def get_cliente(customer_id):
        query= "SELECT customer_id, first_name, last_name, email, phone, street, city, state, zip_code FROM sales.customers WHERE customer_id = %s;"
        params = customer_id,
        result = DatabaseConnection.fetch_one(query, params)
        if result is not None:
            return {
            "id": result[0],
            "nombre": result[1],
            "apellido": result[2],
            "email": result[3],
            "telefono": result[4],
            "calle": result[5],
            "estado": result[6],
            "codigo postal": result[7],
            }, 200
        return {"msg": "No se encontró el cliente"}, 404
        
    #Ejercio 1.2: Obtener el listado de clientes.
    @app.route('/customers/', methods = ['GET'])
    def get_clientes():
        query= "SELECT customer_id, first_name, last_name, email, phone, street, city, state, zip_code FROM sales.customers;"
        results = DatabaseConnection.fetch_all(query)
        clientes = []
        for result in results:
            clientes.append({
            "id": result[0],
            "nombre": result[1],
            "apellido": result[2],
            "email": result[3],
            "telefono": result[4],
            "calle": result[5],
            "estado": result[6],
            "codigo postal": result[7],
            })
        query2=
        return clientes, 200

    #Ejercicio 1.3: Registrar un cliente.
    @app.route('/customers', methods = ['POST'])
    def create_customer():
        query= "INSERT INTO sales.customers (first_name, last_name, email, phone) VALUES (%s,%s,%s,%s);"
        params = request.args.get('first_name', ''), request.args.get('last_name', ''), request.args.get('email', ''), request.args.get('phone', '')
        DatabaseConnection.execute_query(query, params)
        return {"msg": "Actor creado con éxito"}, 201

    #Ejercicio 1.4: Modificar un cliente.
    @app.route('/customers/<int:customer_id>', methods = ["PUT"])
    def update_customer(customer_id):
        query = "UPDATE sales.customers SET phone = %s WHERE customer_id=%s;"
        params = request.args.get('phone', ''), customer_id
        DatabaseConnection.execute_query(query, params)
        return {"msg": "Datos del cliente actualizados con exito"}, 200

    #Ejercicio 1.5: Eliminar un cliente.
    @app.route('/customers/<int:customer_id>', methods = ["DELETE"])
    def delete_customer(customer_id):
        query= "DELETE FROM sales.customer WHERE actor.actor_id = %s;"
        params = customer_id,
        DatabaseConnection.execute_query(query, params)

        return {"msg": "Actor eliminado con éxito"}, 204
    
    return app