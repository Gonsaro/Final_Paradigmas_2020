# -*- encoding: utf-8 -*-
import csv

def AbrirArchivoCSV(strArchivo):
	
	#Función para abrir archivos csv, se utiliza para la ruta como parametro,
	#tomando como directorio raiz la ubicacion del archivo "AccesoArchivo.py"
	#	strArchivo 		==>	el archivo que deseo abrir

	#devuelve los registros en un listado de diccionario
	
	try:
		r = []
		with open(strArchivo, 'r', encoding='utf-8') as archivo2:
			archivo_csv = csv.DictReader(archivo2)
			#lon = len(archivo_csv)
			#if lon > 0:
			for item in archivo_csv:
				r.append(item)
	except FileNotFoundError as ex:
		raise Exception('No se encontró el archivo')
	except Exception as e:
		raise Exception('Problema al procesar el archivo. ' + strArchivo)	

	return r

"""def GuardarRegistroCSV(strArchivo, registro):
	
	#Función para agregar un registro en archivos csv, se para la ruta como parametro,
	#tomando como directorio raiz la ubicacion del archivo 'AccesoArchivo.py'
	#	strArchivo 		==> 	el archivo donde deseo agregar el registro
	#	registro 		==> 	registro que deseo guardar en el archivo

	#devuelve un estado de insericion de registro siendo True cuando se inserto y False cuando no
	#devuelve el mensaje correspondiente al esstado de la insercion del registro
	
	print('GuardarRegistroCSV')
	print(registro)
	r = True
	mensaje = "Se registró la venta exitosamente."
	inicio = len(AbrirArchivoCSV(strArchivo))
	fin = 0
	try:
		with open(strArchivo, 'a+') as archivo:
			archivo_csv = csv.writer(archivo)
			archivo_csv.writerow(registro)
		
		fin = len(AbrirArchivoCSV(strArchivo))
		if inicio == fin:
			r = False
			mensaje = "No fue posible registrar la operación, vuelva a intentarlo en breve."
	except Exception as e:
		mensaje = 'Error inesperado al guardar el registro, ' + str(e)

	return r, mensaje"""

def ValidarUsuarioNuevo(strUsuario):
	#Función para validar si el usuario existe
	#	strUsuario ==> el usuario que deseo validar
	#devuelve true si el usuario no fue habido y false si ya se encuentra en el archivo
	try:
		r = True
		listado = []
		usuarios = AbrirArchivoCSV('usuarios.csv')
		for item in usuarios:
			if strUsuario == item['Usuario']:
				r = False
				break
	except Exception as e:
		raise Exception('Problemas al validar el usuario.')

	return r

"""def SugerirElementoArchivo(strPedido, strCampoEspecificado, strArchivo):
	
	#Función que me devuelve un listado de sugerencias segun el campo especificado
	#	strPedido 				==> 	el string que deseo encontrar
	#	strCampoEspecificado 	==> 	el campo donde deseo que se encuentre el string que envio de busqueda
	#	strArchivo 				==> 	el archivo donde deseo buscar el dato

	#devuelve un listado con los resultados de busqueda
	resultado = []
	Listado = AbrirArchivoCSV(strArchivo)
	for item in Listado:
			if strPedido in item[strCampoEspecificado]:
				listado.append(item)

	return resultado"""