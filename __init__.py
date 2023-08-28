from flask import Flask 
from config import Config 
from flask import request
from .database import DatabaseConnection

def init_app(): 
	"""Crea y configura la aplicación Flask""" 
	app =Flask(__name__, static_folder = Config.STATIC_FOLDER, template_folder = Config.TEMPLATE_FOLDER) 
	app.config.from_object(Config) 
		
	@app.route('/')
	def hola():
		return 'hola'
	
	@app.route('/home')
	def home():
		return  ({'message':'Bienvenido a Academia!'}, 200, {'Content-Type':'application/json'})

	#ejercicio 1
	#1.1 obtener un cliente
	@app.route('/customers/<int:customer_id>', methods = ['GET'])
	def get_actor(customer_id):
		query= "SELECT customer_id, first_name, last_name, email, phone, street, city, state, zip_code  FROM customers WHERE customer_id = %s;"
		params = customer_id,
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


	#1.2 obtener el listado de clientes con filtro
	#campo=atributo 			(puede ser cualquier atributo de la tabla customers)
	#valor=nombre o numero 		(valor del que buscamos saber cuantas veces se repite) 
	#EJEMPLO:(city=Anaheim)--> http://127.0.0.1:5000/customers?campo=city&valor=Anaheim
	@app.route('/customers', methods = ['GET'])
	def get_actors(): 	
		campo=request.args.get('campo')
		valor=request.args.get('valor')
		query= f"SELECT customer_id, first_name, last_name, email, phone, street, city, state, zip_code FROM customers WHERE customers.{campo} = '{valor}';"
		
		if valor == "null" or valor == "NULL":
			#en caso de que la solicitud, valor sea igual a null
			query= f"SELECT customer_id, first_name, last_name, email, phone, street, city, state, zip_code FROM customers WHERE {campo} IS NULL;"	
		
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
		if UnboundLocalError or result is None:
			return {"msg": "No se encontro el cliente"}, 404
		
		return {"customers" : actors ,
				"total" : len(actors)
				},200
		
	"""
	#post 
	@app.route('/actors', methods = ['POST'])
	def create_actor():
		query= "INSERT INTO sakila.actor (first_name, last_name, last_update) VALUES (%s,%s,%s);"
		params = request.args.get('first_name', ''), request.args.get('last_name', ''), request.args.get('last_update', '')
		DatabaseConnection.execute_query(query, params)
		return {"msg": "Actor creado con éxito"}, 201

	
	
	#put
	@app.route('/actors/<int:actor_id>', methods = ['PUT'])
	def update_actor(actor_id):
		query= "UPDATE sakila.actor SET last_update = %s WHERE actor.actor_id = %s;"
		params = request.args.get('last_update', ''), actor_id
		DatabaseConnection.execute_query(query, params)
		return {"msg": "Datos del actor actualizados con éxito"}, 200
	
	#delete
	@app.route('/actors/<int:actor_id>', methods = ['DELETE'])
	def delete_actor(actor_id):
		query= "DELETE FROM sakila.actor WHERE actor.actor_id = %s;"
		params = actor_id,
		DatabaseConnection.execute_query(query, params)
		return {"msg": "Actor eliminado con éxito"}, 204
	"""
	return app
