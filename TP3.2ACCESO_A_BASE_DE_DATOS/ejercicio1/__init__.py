from flask import Flask, request
from config import Config
from .database import DatabaseConnection
def init_app():
    """Crea y configura la aplicacion Flask"""
    app = Flask(__name__, static_folder = Config.STATIC_FOLDER, template_folder = Config.TEMPLATE_FOLDER)
    app.config.from_object(Config)
   
    #Ejercio 1.1: Obtener un cliente.
    @app.route('/customers/<int:customer_id>', methods = ['GET'])
    def get_customer(customer_id):
        query = "SELECT customer_id, first_name, last_name, phone, email, city, street, state, zip_code FROM sales.customers WHERE customers_id = %s; "
        params = customer_id
        result = DatabaseConnection.fetch_one(query, params)
        if result is not None:
            return {
                "id": result[0],
                "nombre": result[1],
                "apellido": result[2],
                
            }, 200        
        return {'msg':"No se encontró el cliente"}, 404
   
    #Ejercio 1.2: Obtener el listado de clientes.
    @app.route('/customers', methods = ['GET'])
    def get_customers():
        query = "SELECT customer_id, total FROM sales.customers;"
        results = DatabaseConnection.fetch_all(query)
        customers = []
        for results in results:
            customers.append({ #corregir el result. no idea why it is yellow unu
                "id": result[0],
                "nombre": result[1],
                "apellido": result[2],
            })
        return customers, 200
    
    #Ejercicio 1.3: Registrar un cliente.
    @app.route('/customers', methods = ['POST'])
    def create_customer():#Pendiente: crear recursos en la applicación?
        query = "INSERT INTO sales.customers(first_name, last_name, email) VALUES (%s, %s, %s);"
        params = request.args.get('first_name', ''), request.args.get('last_name', ''), request.args.get('email', '')
        DatabaseConnection.execute_query(query, params)
        return{"msg": "Cliente añadido con éxito!"}, 201
   
    #Ejercicio 1.4: Modificar un clieinte.
    @app.route('/customers/<int:customer_id>', methods = ["PUT"])
    def update_customer(customer_id):
        query = "UPDATE sales.customers SET first_name = %s WHERE customers.customer_id = %s;"
        #query = "UPDATE sales.customers SET last_name = %s WHERE customers.customer_id = %s;"
        #query = "UPDATE sales.customers SET email = %s WHERE customers.customer_id = %s;"
        #query = "UPDATE sales.customers SET phone = %s WHERE customers.customer_id = %s;"
        params = request.args.get('first_name', ''), customer_id
        DatabaseConnection.execute_query(query, params)
        return{"msg": "Datos actualizados!"}, 200
   
    #Ejercicio 1.5: Eliminar un cliente.
    @app.route('/customers/<int:customer_id>', methods = ["DELETE"])
    def delete_customer(customer_id):
        query = "DELETE FROM sales.customers WHERE customers.customer_id = %s;"
        DatabaseConnection.execute_query(query, params) #otra vez amaillo (?
        return { "msg": "Cliente borrado con éxito!"}, 200
    
    #Ejercicio 2.1: Obtener un producto.
    @app.route('/products/<int:product_id>', methods = ['GET'])
    def get_product(product_id):
        return{}, 200
   
    #Ejercicio 2.2: Obtener un listado de productos.
    @app.route('/products', methods = ['GET']):
    def get_products():
        return{}, 200

    #Ejercicio 2.3: Registrar un producto.
    @app.route('/products', methods = ['POST'])
    def create_product()
        return {}, 201
    
    #Ejercicio 2.4: Modificar un producto.
    @app.route('/products/<int:product_id>', methods = ['PUT'])
    def update_product():
        return {}, 200
    
    #EJercicio 2.5: Eliminar un producto.
    @app.route('/products/<int:product_id>', methods = ['DELETE'])
    def delete_product(product_id):
        return{}, 204
    return app