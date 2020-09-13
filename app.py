import csv
import AccesoArchivo
import string
from datetime import datetime
from decimal import Decimal

from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap


from forms import LoginForm, RegistrarForm, Busqueda, ClientesFiltroForm, FiltroFecha, FiltroEdad, AltaNuevoCliente, AltaNuevoProducto


app = Flask(__name__) #variable predefinida de Python, que se establece en el nombre del módulo en el que se utiliza. Flask utiliza la ubicación del módulo pasado aquí como punto de partida cuando necesita cargar recursos asociados, como archivos de plantilla
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'you-will-never-guess'


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

#----------------carga en una lista el archivo de clientes y lo devuelve
def ListaCSV():
    with open('clientes.csv', 'r', encoding="UTF-8") as archivoclientes: #abre el archivo en solo lectura "r" y lo devuelve como lista
        leearch = csv.reader(archivoclientes)
        archlist= list(leearch)
    return archlist

#----------------carga en una lista el archivo de productos y lo devuelve
def ProdCSV():
    with open('ventas.csv', 'r', encoding="UTF-8") as archivoproductos:
        leearch = csv.reader(archivoproductos)
        archlist= list(leearch)
    return archlist

#----------------funciones para filtrar csv

def encabezado(tabla):
    return tabla[0]

def cuerpo(tabla):
    del tabla[0]
    return tabla   

def filtrado(tabla, que, dedonde):
    if que=='a': #anterior a la fecha seleccionada
        clientesfiltrados=filter(lambda x: x[5]<dedonde, tabla)
    elif que=='m': #misma fecha seleccionada
        clientesfiltrados=filter(lambda x: x[5]==dedonde, tabla)
    elif que=='p': #posteriores a la fecha seleccionada
        clientesfiltrados=filter(lambda x: x[5]>dedonde, tabla)  #filtra todo contra la columna 5 de fechas
    elif que=='j': #menores de la edad seleccionada
        clientesfiltrados=filter(lambda x: int(x[1])<int(dedonde), tabla)
    elif que=='i': #misma edad que la seleccionada
        clientesfiltrados=filter(lambda x: int(x[1])==int(dedonde), tabla)
    elif que=='v': #mayores de la edad seleccionada
        clientesfiltrados=filter(lambda x: int(x[1])>int(dedonde), tabla) #filtra contra columna 1 de edades
    elif que=='n':
        clientesfiltrados=filter(lambda x: x[3]==dedonde, tabla) #filtra contra paises
    return list(clientesfiltrados)


def listapaises(tabla, pais):
    listaprevia=list()
    for i in range(len(tabla)-1):
        aux=tabla[i][3]
        if (pais.lower() in aux.lower()):
            listaprevia.append(aux)
    return sorted(list(set(listaprevia)))  #devuelve la lista de paises ordenada

#----------------Rutas de direcciones

@app.route('/')
def index():
    return render_template('index.html', fecha_actual=datetime.utcnow())

#----------------Ingreso al sitio

@app.route('/ingresar', methods=['GET', 'POST']) #POST sirve para envia informacion al servidor con los formularios
def ingresar():

    if not 'username' in session:
        formulario = LoginForm()
        if formulario.validate_on_submit():   # Aca hago el POST si es True
            with open('usuarios.csv') as archivo: #.validate_on_submit() procesa la informacion
                archivo_csv = csv.reader(archivo)
                registro = next(archivo_csv)
                while registro:
                    if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:
                        print('postback success') 
                        flash('Bienvenido') #si se verifica TRUE devuelve esto
                        session['username'] = formulario.usuario.data
                        return render_template('ingresado.html')
                    registro = next(archivo_csv, None)
                else:
                    print('postback error')
                    flash('Revisá nombre de usuario y contraseña') ##si se verifica FALSE devuelve esto
                    return redirect(url_for('ingresar'))
        return render_template('login.html', formulario=formulario)
    else:
        return index()

#----------------Registrar usuario

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    formulario = RegistrarForm()
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data:
            if AccesoArchivo.ValidarUsuarioNuevo(formulario.usuario.data):               
                with open('usuarios.csv', 'a+', newline='') as archivo:
                    archivo_csv = csv.writer(archivo)
                    registro = [formulario.usuario.data, formulario.password.data]
                    archivo_csv.writerow(registro)
                flash('Usuario creado correctamente')
                return redirect(url_for('ingresar'))
            else:
                flash("Usuario previamente registrado")
        else:
            flash('Las passwords no concuerdan')
    return render_template('registrar.html', form=formulario)

#----------------redireccionamiento

@app.route('/secret', methods=['GET'])
def secreto():
    if 'username' in session:
        return render_template('private.html', username=session['username'])
    else:
        return render_template('sin_permiso.html')

#----------------archivo de clientes

@app.route('/clientes', methods=['GET'])
def clientes():
    if 'username' in session:
        tabla=ListaCSV()
        cabeza=encabezado(tabla)
        cli=cuerpo(tabla)
        cantcli=len(tabla)
        return render_template('clientes.html', cantidad=cantcli, listacli=cli, encabezado=cabeza, totfil="totales") 
    else:
        return redirect(url_for('registrar'))

#----------------Manejo de error 404

@app.errorhandler(404)
def no_encontrado(e):
    return render_template('404.html'), 404

#----------------Manejo de error 500

@app.errorhandler(500)
def error_interno(e):
    return render_template('500.html'), 500

#----------------About

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

#----------------Filtros por pais

@app.route('/filt-pais', methods=['GET', 'POST'])
def filtpais():
    if 'username' in session:
        formulario=ClientesFiltroForm()
        if formulario.validate_on_submit():
            clientesafiltrar=ListaCSV()
            cabeza=encabezado(clientesafiltrar)
            tabladeclientesafiltrar=cuerpo(clientesafiltrar)
            opciones=listapaises(tabladeclientesafiltrar, formulario.pais.data)
            return render_template('selepais.html', opciones=opciones)
        return render_template('ffecha.html', formulario=formulario, filtro="fecha")
    else:
        return redirect(url_for('ingresar'))

@app.route('/filt-pais/pais/<pais>', methods=['GET'])
def filtrarpais(pais):
    if 'username' in session:
        clientesafiltrar=ListaCSV()
        cabeza=encabezado(clientesafiltrar)
        tabladeclientesafiltrar=cuerpo(clientesafiltrar)
        tablafiltrada=filtrado(tabladeclientesafiltrar, 'n', pais)
        cantcli=len(tablafiltrada)
        return render_template('clientes.html', cantidad=cantcli, listacli=tablafiltrada, encabezado=cabeza, totfil="filtrados")
    else:
        return redirect(url_for('ingresar'))

#----------------Lista de productos

@app.route('/productos', methods=['GET'])
def productos():
    if 'username' in session:
        tabla=ProdCSV()
        cabeza=encabezado(tabla)
        pro=cuerpo(tabla)
        cantpro=len(tabla)
        return render_template('productos.html', cantidad=cantpro, listapro=pro, encabezado=cabeza, totfil="totales") 
    else:
        return redirect(url_for('registrar'))

#----------------filtro por edad

@app.route('/filt-edad', methods=['GET', 'POST'])
def filtedad():
    if 'username' in session:
        formulario=FiltroEdad()
        if formulario.validate_on_submit():
            clientesafiltrar=ListaCSV()
            cabeza=encabezado(clientesafiltrar)
            tabladeclientesafiltrar=cuerpo(clientesafiltrar)
            tablafiltrada=filtrado(tabladeclientesafiltrar, formulario.seleccionfecha.data, formulario.fecha.data)
            cantcli=len(tablafiltrada)
            return render_template('clientes.html', cantidad=cantcli, listacli=tablafiltrada, encabezado=cabeza, totfil="filtrados") 
        return render_template('ffecha.html', formulario=formulario, filtro="edad")
    else:
        return redirect(url_for('ingresar'))

#----------------filtro por fecha

@app.route('/filt-fecha', methods=['GET', 'POST'])
def filtfecha():
    if 'username' in session:
        formulario=FiltroFecha()
        if formulario.validate_on_submit():
            clientesafiltrar=ListaCSV()
            cabeza=encabezado(clientesafiltrar)
            tabladeclientesafiltrar=cuerpo(clientesafiltrar)
            tablafiltrada=filtrado(tabladeclientesafiltrar, formulario.seleccionfecha.data, formulario.fecha.data)
            cantcli=len(tablafiltrada)
            return render_template('clientes.html', cantidad=cantcli, listacli=tablafiltrada, encabezado=cabeza, totfil="filtrados") 
        return render_template('ffecha.html', formulario=formulario, filtro="fecha")
    else:
        return redirect(url_for('ingresar'))

#----------------alta de nuevo cliente

@app.route('/altacliente', methods=['GET', 'POST'])
def altacliente():
    if 'username' in session:
        formulario=AltaNuevoCliente()
        if formulario.validate_on_submit():
            with open('clientes.csv', 'a+', newline='', encoding='utf-8') as archivo:
                archclientes_csv= csv.writer(archivo)
                registro=[formulario.nombre.data, str(formulario.edad.data), formulario.direccion.data, formulario.pais.data, formulario.documento.data, formulario.fechaalta.data, formulario.correo.data, formulario.trabajo.data]
                archclientes_csv.writerow(registro)
            flash('Cliente agregado')
            return redirect(url_for('clientes'))
        return render_template('altaclientes.html', form=formulario)
    else:
        return redirect(url_for('registrar'))

#----------------alta de nuevo producto

@app.route('/altaproducto', methods=['GET', 'POST'])
def altaproducto():
    if 'username' in session:
        formulario=AltaNuevoProducto()
        if formulario.validate_on_submit():
            with open('ventas.csv', 'a+', newline='', encoding='utf-8') as archivo:
                archproductos_csv= csv.writer(archivo)
                registro=[formulario.codigo.data, formulario.producto.data, formulario.cliente.data, str(formulario.cantidad.data), str(formulario.precio.data)]
                archproductos_csv.writerow(registro)
            flash('Producto agregado')
            return redirect(url_for('productos'))
        return render_template('altaproductos.html', form=formulario)
    else:
        return redirect(url_for('registrar'))

#----------------desloguearse

@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template('logged_out.html')
    else:
        return redirect(url_for('index'))

#----------------

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)