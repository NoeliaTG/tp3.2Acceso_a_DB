from flask import Flask 
from config import Config 
from flask import request
from .database import DatabaseConnection

def init_app(): 
	"""Crea y configura la aplicación Flask""" 
	app =Flask(__name__, static_folder = Config.STATIC_FOLDER, template_folder = Config.TEMPLATE_FOLDER) 
	app.config.from_object(Config) 
			
	@app.route('/')
	def home():
		return  "trabajo practico 3.2 Programacion II"

	#EJERCICIO 1
	#1.1 Obtener un cliente
	@app.route('/customers/<int:customer_id>', methods = ['GET'])
	def get_customer(customer_id):
		query= "SELECT customer_id, first_name, last_name, email, phone, street, city, state, zip_code  FROM customers WHERE customer_id = %s;"
		params = customer_id,
		DatabaseConnection.fetch_one("use sales;")
		result = DatabaseConnection.fetch_one(query, params)
		if result is not None:
			return {
					"id": result[0],
					"nombre": result[1], 
					"apellido": result[2],
					"email" : result[3],
					"phone" : result[4],
					"street" : result[5], 
					"city" : result[6],
					"state" : result[7],
					"zip_code" : result[8]
					}, 200
		return {"msg": "No se encontró el cliente"}, 404


	#1.2 Obtener el listado de clientes con filtro
		#campo=atributo 			(puede ser cualquier atributo de la tabla customers)
	    #valor=nombre o numero 		(valor del que buscamos saber cuantas veces se repite) 
	    #EJEMPLO:(city=Anaheim)--> http://127.0.0.1:5000/customers?campo=city&valor=Anaheim
	@app.route('/customers', methods = ['GET'])
	def get_customers(): 	
		campo=request.args.get('campo')
		valor=request.args.get('valor')
		query= f"SELECT customer_id, first_name, last_name, email, phone, street, city, state, zip_code FROM customers WHERE customers.{campo} = '{valor}';"
		
		if valor == "null" or valor == "NULL":
			#en caso de que la solicitud, valor sea igual a null
			query= f"SELECT customer_id, first_name, last_name, email, phone, street, city, state, zip_code FROM customers WHERE {campo} IS NULL;"	
		
		DatabaseConnection.fetch_one("use sales;")
		results = DatabaseConnection.fetch_all(query) 
		actors = [] 
		for result in results:
			actors.append({ "id": result[0],
		  					 "nombre": result[1], 
							 "apellido": result[2],
							 "email" : result[3],
							 "phone" : result[4],
							 "street" : result[5], 
							 "city" : result[6],
							 "state" : result[7],
							 "zip_code" : result[8]
							   })

		return {"customers" : actors ,
				"total" : len(actors)
				},200
		
	
	#1.3 Registar un cliente
	#EJEMPLO http://127.0.0.1:5000/customers/registrar?first_name=Fulanitos&last_name=Rodriguez&email=fulano@gmail.com
	@app.route('/customers/registrar', methods = ['GET','POST'])
	def create_customer():	
		query= "INSERT INTO sales.customers (first_name, last_name, email) VALUES (%s,%s,%s);"
		params = request.args.get('first_name', ''), request.args.get('last_name', ''), request.args.get('email', '')
		DatabaseConnection.fetch_one("use sales;")
		DatabaseConnection.execute_query(query, params)
		return {"msg": "Cliente creado con exito"}, 201
	
	#1.4 Modificar un cliente	
	#EJEMPLO (first_name=Fulano) http://127.0.0.1:5000/customers/modificar/100?campo=first_name&valor=Fulano
	@app.route('/customers/modificar/<int:customer_id>', methods = ['GET','PUT'])
	def update_customer(customer_id):
		campo=request.args.get('campo')
		valor=request.args.get('valor')
		query= f"UPDATE sales.customers SET customers.{campo} = '{valor}' WHERE customer_id= {customer_id};"
		DatabaseConnection.execute_query("use sales;")
		DatabaseConnection.execute_query(query)
		return {"msg": "Datos del cliente  actualizados con exito"}, 200
	

	#1.5 Eliminar un cliente
	@app.route('/customers/eliminar/<int:customer_id>', methods = ['DELETE','GET'])
	def delete_customer(customer_id):
		query= "DELETE FROM sales.customers WHERE customer_id = %s;"
		params = customer_id,
		DatabaseConnection.execute_query("use sales;")
		DatabaseConnection.fetch_one(query, params)
		return {"msg": "Cliente eliminado con éxito"}, 204
	
	
	#EJERCICIO 2
	#2.1 Obtener un producto.
	@app.route('/products/<int:product_id>', methods = ['GET'])
	def get_product(product_id):
		query= "SELECT product_id, product_name, model_year, list_price  FROM products WHERE product_id = %s;"
		params = product_id,
		DatabaseConnection.fetch_one("use production;")
		result = DatabaseConnection.fetch_one(query, params)
		if result is not None:
			#inner join con la tabla brands
			query="SELECT products.brand_id, brands.brand_name  FROM products INNER JOIN brands ON products.brand_id=brands.brand_id WHERE products.product_id=%s ;"
			params=product_id,
			result_brand=DatabaseConnection.fetch_one(query,params)
			
			#inner join con la tabla categories
			query="SELECT products.category_id, categories.category_name  FROM products INNER JOIN categories ON products.category_id=categories.category_id WHERE products.product_id=%s ;"
			result_category=DatabaseConnection.fetch_one(query,params)

			return {
				"brand":{
						"brand_id":result_brand[0],
						"brand_name":result_brand[1]
						},
				"category":{
						"category_id":result_category[0],
						"category_name":result_category[1]
						},
                "product_id": result[0],
                "product_name": result[1],
                "model_year": result[2],
                "list_price": result[3]  
                }, 200        
		return {'msg':"No se encontró el producto"}, 404
	

	#2.2 Obtener un listado de productos
	#EJEMPLO (brand_id,4)  http://127.0.0.1:5000/products?campo=brand_id&valor=4
	@app.route('/products', methods = ['GET'])
	def get_products(): 	
		campo=request.args.get('campo')
		valor=request.args.get('valor')
		
		#query selecciona los # FROM products INNER JOIN brands ON products.brand_id=brands.brand_id WHERE products.{campo}={valor};"
		query=f"SELECT product_id,product_name,list_price,model_year FROM products WHERE {campo}={valor};"
		DatabaseConnection.close_connection()
		DatabaseConnection.execute_query("use production;")
		result = DatabaseConnection.fetch_all(query) 
		
		query=f"SELECT products.brand_id, brands.brand_name  FROM products INNER JOIN brands ON products.brand_id=brands.brand_id WHERE products.{campo}={valor} ;"
		result_brand=DatabaseConnection.fetch_all(query)
		
		query=f"SELECT products.category_id, categories.category_name  FROM products INNER JOIN categories ON products.category_id=categories.category_id WHERE products.{campo}={valor} ;"
		result_category=DatabaseConnection.fetch_all(query)

		productos=[]
		if result is not None:
			for results in result:
				for resultsb in result_brand:
					for resultc in result_category:
						productos.append({
							"brand":{
							"brand_id":resultsb[0],
							"bran_name":resultsb[1]
							},
							"category":{
							"category_id":resultc[0],
							"category_name":resultc[1]
							},
							"product_id":results[0],
							"product_name":results[1],
							"list_price":results[2],
							"model_year":results[3]
							})
			return {"products":productos,
					"total":len(productos)},200
	
		return {'msg':"No se encontró el producto"}, 404


	#2.3 Registrar un producto
	#EJEMPLO http://127.0.0.1:5000/products/registrar?product_name=huevos_fritos&brand_id=4&category_id=2&model_year=2019&list_price=894.37
	@app.route('/products/registrar', methods = ['GET','POST'])
	def create_product():	
		query= "INSERT INTO production.products (product_name, brand_id, category_id, model_year, list_price) VALUES (%s,%s,%s,%s,%s);"
		params = request.args.get('product_name', ''), request.args.get('brand_id', ''), request.args.get('category_id', ''), request.args.get('model_year', ''), request.args.get('list_price', '')
		DatabaseConnection.fetch_one("use production;")
		DatabaseConnection.execute_query(query, params)
		DatabaseConnection.close_connection()
		return {"msg": "Producto creado con exito"}, 201
	
	
	#2.4 Modificar un cliente	
	#EJEMPLO (product_name=Pizza) http://127.0.0.1:5000/products/modificar/318?campo=product_name&valor=Pizza
	@app.route('/products/modificar/<int:product_id>', methods = ['GET','PUT'])
	def update_product(product_id):
		campo=request.args.get('campo')
		valor=request.args.get('valor')
		query= f"UPDATE production.products SET products.{campo} = '{valor}' WHERE product_id= {product_id};"
		DatabaseConnection.execute_query("use production;")
		DatabaseConnection.execute_query(query)
		DatabaseConnection.close_connection()
		return {"msg": "Datos del producto  actualizados con exito"}, 200
	
	
	#2.5 Eliminar un producto
	#EJEMPLO http://127.0.0.1:5000/products/eliminar/320
	@app.route('/products/eliminar/<int:product_id>', methods = ['DELETE','GET'])
	def delete_product(product_id):
		query= "DELETE FROM production.products WHERE product_id = %s;"
		params = product_id,
		DatabaseConnection.execute_query(query, params)
		DatabaseConnection.close_connection()
		return {"msg": "Producto eliminado con éxito"}, 204
	
	return app
