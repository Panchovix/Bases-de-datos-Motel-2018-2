from configuraciones import *
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))


cur = conn.cursor()
sql ="""DROP SCHEMA public CASCADE;
CREATE SCHEMA public;"""

cur.execute(sql)

sql ="""
CREATE TABLE clientes 
           (id serial PRIMARY KEY, nombre varchar(40), apellido varchar, patente varchar, creado timestamp, rut integer,  dv varchar(10) );
"""

cur.execute(sql)


sql ="""
CREATE TABLE arriendos
           (id serial PRIMARY KEY, hr_entrada varchar(40), hr_salida varchar(40), cliente_id varchar(40),num_habitacion integer, boleta_id varchar(40),consumos_id varchar(50));
"""

cur.execute(sql)

sql ="""
CREATE TABLE habitaciones 
           (id serial PRIMARY KEY, tipo varchar(40), numero integer, estado integer);
"""

cur.execute(sql)

sql ="""
CREATE TABLE  consumos
           (id serial PRIMARY KEY,cantidad integer, producto_id integer,total integer, estado_pedido integer, 
            creado timestamp);
"""

cur.execute(sql)

sql ="""
CREATE TABLE productos
           (id serial PRIMARY KEY, nombre varchar(140), stock_actual integer, cantidad_horas integer,precio integer, creado timestamp);
"""

cur.execute(sql)


conn.commit()
cur.close()
conn.close()
