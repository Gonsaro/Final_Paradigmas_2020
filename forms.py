from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, RadioField, DecimalField
from wtforms.validators import Required, Length
#import Utilidades

#----------------Formulario para loguearse

class LoginForm(FlaskForm):
    usuario = StringField('Nombre de usuario', validators=[Required()])
    password = PasswordField('Contraseña', validators=[Required()])
    enviar = SubmitField('Ingresar')  

#----------------Formulario para registrarse

class RegistrarForm(LoginForm):
    password_check = PasswordField('Verificar Contraseña', validators=[Required()])
    enviar = SubmitField('Registrarse')

#----------------Formulario para busqueda de paises

class Busqueda(FlaskForm):
    Pais = StringField('Pais ')
    Buscar = SubmitField('Buscar')

#----------------Formulario para filtrar clientes por pais

class ClientesFiltroForm(FlaskForm):
    pais = StringField('País', render_kw={"placeholder":"para mejores resultados ingrese al menos 3 letras del país a consultar"})
    enviar = SubmitField('Filtrar')

#----------------Formulario para filtrar por edad

class FiltroEdad(FlaskForm):
    fecha = StringField('Edad', render_kw={"placeholder":"ingrese la fecha edad a consultar"})
    mostrar = StringField('Mostrar', render_kw={'type':'Hidden'}) 
    seleccionfecha = RadioField('Mostrar',
        choices=[
            ('j', 'menores de la edad seleccionada'), 
            ('i', 'misma edad que la seleccionada'), 
            ('v', 'mayores de la edad seleccionada')])
    enviar = SubmitField('Filtrar')

#----------------Formulario para filtrar por fecha

class FiltroFecha(FlaskForm):
    fecha = StringField('Fecha de Alta', render_kw={"placeholder":"ingrese la fecha que quiere consultar (formato AAAA-MM-DD)"})
    mostrar = StringField('Mostrar', render_kw={'type':'Hidden'}) 
    seleccionfecha = RadioField('Mostrar',
        choices=[
            ('a', 'anteriores a la fecha seleccionada'), 
            ('m', 'misma fecha que la seleccionada'), 
            ('p', 'posteriores a la fecha seleccionada')])
    enviar = SubmitField('Filtrar')

#----------------

class AltaNuevoCliente(FlaskForm):
    nombre = StringField('Nombre', render_kw={"placeholder":"Nombre(s) y Apellido(s)"}, validators=[Required()] )
    edad = IntegerField('Edad', render_kw={"placeholder":"edad del cliente"}, validators=[Required()])
    direccion = StringField('Dirección',render_kw={"placeholder":"dirección"}, validators=[Required()])
    pais = StringField('País', render_kw={"placeholder":"país"}, validators=[Required()])
    documento= StringField('Documento',render_kw={"placeholder":"documento"}, validators=[Required()])
    fechaalta = StringField('Fecha de Alta (AAAA-MM-DD)', render_kw={"placeholder":"formato AAAA-MM-DD"}, validators=[Required()])
    correo = StringField('Correo electrónico', render_kw={"placeholder":"correodelcliente@loquesea.loquesea"}, validators=[Required()])
    trabajo = StringField('Trabajo', render_kw={"placeholder":"trabajo"}, validators=[Required()])
    enviar = SubmitField('Agregar')

#----------------

class AltaNuevoProducto(FlaskForm):
    codigo = StringField('Código', render_kw={"placeholder":"Código del producto"}, validators=[Required()] )
    producto = StringField('Producto',render_kw={"placeholder":"Nombre del producto"}, validators=[Required()])
    cliente = StringField('Cliente',render_kw={"placeholder":"Nombre y apellido"}, validators=[Required()])
    cantidad = IntegerField('Cantidad', render_kw={"placeholder":"Cantidad de unidades"}, validators=[Required()])
    precio = DecimalField('Precio',render_kw={"placeholder":"Importe"}, validators=[Required()])
    enviar = SubmitField('Agregar')