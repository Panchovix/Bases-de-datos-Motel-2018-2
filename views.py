from app import app
from flask import render_template,request,redirect
from configuraciones import *

import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))
cur = conn.cursor()


@app.route('/')
@app.route('/index')
def index():
	sql ="""
	select id,nombre from categorias order by nombre
	"""
	print sql 
	cur.execute(sql)
	categorias  = cur.fetchall()
	sql ="""
	select id,titulo,resumen from posts
	"""
	print sql
	cur.execute(sql)
	posts  = cur.fetchall()
	return render_template("index.html",categorias=categorias,posts=posts)
#consultas agregadas
#Primera consulta, la cual selecciona el nombre y apellido de los clientes del recinto total
	sql ="""
	select clientes.nombre, clientes.apellido from clientes
	"""
	print sql
	cur.execute(sql)
	categorias = cur.fetchall()
#consulta 2, la cual suma la cantidad de consumos donde la habitación está pedida
	sql ="""
	select sum consumos.cantidad
	from consumos
	where estado_pedido = 1
	"""
	print sql
	cur.execute(sql)
	categorias = cur.fetchall()
#consulta 3, obtener el numero y el estado de la habitacion, del cliente llamado diego el cual ha pagado por un producto mayor a 2000 y
# a la vez está arrendando.
	sql = """
	select habitaciones.numero, habitaciones.estado
	from habitaciones, clientes, productos, arriendos
	where clientes.rut = arriendos.cliente_id
	and clientes.name = "Diego"
	and productos.precio > 2000
	and habitaciones.numero = arriendos.num_habitacion
	"""
	print sql
	cur.execute(sql)
	categorias = cur.fetchall()
#consulta 4, que calcula la suma de la multiplicación de los productos (su precio) por su cantidad, del total de productos
# y que exista al menos un stock actual
	sql = """
	select sum (consumos.cantidad * productos.precio)
	from consumos,productos
	where consumos.producto_id = productos.id
	and producto.stock_actual > 1
	"""
	print sql
	cur.execute(sql)
	categorias = cur.fetchall()
#consulta 5, la cual entrega el nombre, apellido y patente del cliente, que arrienda la habitación numero 10, el cual ha consumido
# más de 2 meriendas como productos, y que tiene una promoción actual de arriendo. Esta hay que corregir
	sql = """
	select clientes.nombre, clientes.apellido, clientes.patente
	from clientes, arriendos, habitaciones, consumos, productos
	where clientes.rut = arriendos.clientes_id
	and arriendos.num_habitacion = habitaciones.numero
	and habitaciones.estado = 1
	and arriendos.consumo_id = consumo_id
	and consumos.productos_id= productos_id
	and producto.nombre = "Merienda"
	and consumos.cantidad > 2
	and habitaciones.numero = 10
	and arriendos.promocion_id = 1
	"""
	print sql
	cur.execute(sql)
	categorias = cur.fetchall()
	
#consulta 6, habitaciones mas proximas a cumplir
	sql = """
	
	select num_habitacion 
	from arriendos
	order by desc hora_salida
	"""
	print sql
	cur.execute(sql)
	categorias = cur.fetchall()

#consulta 7, listado de habitaciones que esten por hacer
	sql = """
	
	
	select habitaciones.numero 
	from habitaciones, arrienda 
	where habitaciones.numero = arrienda.num_habitacion  
	and estado= limpieza;
	"""
	print sql
	cur.execute(sql)
	categorias = cur.fetchall()
	
#consulta 8 habitaciones disponibles para ocupar
	sql = """
	
	
	select habitaciones.numero 
	from habitaciones, arrienda 
	where habitaciones.numero = arrienda.num_habitacion  
	and estado= disponible;


	"""
	print sql
	cur.execute(sql)
	categorias = cur.fetchall()
	
	
	#consulta 9 lista de productos actuales
	sql = """
	
	
	
	select productos.nombre 
	from productos
	where stockactual>0 ;


	"""
	print sql
	cur.execute(sql)
	categorias = cur.fetchall()
	
	
		#consulta 10
	sql = """
	
	
	
	select productos.nombre 
	from productos
	where stockactual>0 ;


	"""
	print sql
	cur.execute(sql)
	categorias = cur.fetchall()
	
@app.route('/post/<post_id>', methods=['GET', 'POST'])
def post(post_id):
	if request.method == 'POST':
		comentario =  request.form['comentarios']
		print comentario
		sql = """ insert into comentarios  
		(post_id,usuario_id,creado,comentario) 
		values (%s,1,now(),'%s' ) """%(post_id,comentario)
		cur.execute(sql)
		conn.commit()

	sql ="""
	select id,titulo,texto from posts where id = %s
	"""%post_id
	print sql
	cur.execute(sql)
	post  = cur.fetchone()

	sql ="""
	select id,nombre from categorias,categorias_posts 
	where categorias_posts.categoria_id = categorias.id 
	and post_id = %s 
	"""%(post_id)
	print sql
	cur.execute(sql)
	categorias  = cur.fetchall()

	sql ="""
	select comentarios.id,nombre,apellido,comentario
	
	from usuarios,comentarios 
	where comentarios.usuario_id = usuarios.id 
	and post_id = %s order by id desc
	"""%(post_id)
	print sql
	cur.execute(sql)
	comentarios  = cur.fetchall()
	return render_template("post.html",post= post,categorias=categorias,comentarios= comentarios) 


@app.route('/comentario/<id>', methods=['GET', 'POST'])
def comentario(id):
	if request.method == 'POST':
		comentario =  request.form['comentarios']
		print comentario
		sql = """ update comentarios  set comentario = '%s'
		where id = %s """%(comentario,id)
		cur.execute(sql)
		conn.commit()


	sql ="""
	select comentarios.id,nombre,apellido,comentario
	
	from usuarios,comentarios 
	where comentarios.usuario_id = usuarios.id 
	and comentarios.id = %s order by id desc
	"""%(id)
	print sql
	cur.execute(sql)
	comentario  = cur.fetchone()
	return render_template("comentario.html",comentario= comentario) 


@app.route('/borrar/<id>', methods=['GET', 'POST'])
def borrar(id):


	sql ="""
		delete from comentarios where id = %s
	"""%(id)
	print sql
	cur.execute(sql)
	conn.commit()
	return  redirect(request.referrer)



