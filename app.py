from urllib import request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/index')
def inicio():
    return render_template('index.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bolsos')
def bolsos():
    return render_template('bolsos.html')


@app.route('/mochilas')
def mochilas():
    return render_template('mochilas.html')


@app.route('/buy-bags')
def buy_bags():
    return render_template('buy-bags.html')


@app.route('/aboutus')
def aboutus_route():
    return render_template('aboutus.html')


@app.route('/contact')
def contact_route():
    return render_template('contact.html')


@app.route('/formulario')
def formulario():
    return render_template('formulario.html')


@app.route('/procesar-formulario', methods=['POST'])
def procesar_formulario():
    nombre = request.form['nombre']
    email = request.form['email']
    mensaje = request.form['mensaje']

    # Aquí puedes hacer lo que necesites con los datos del formulario

    return 'Formulario enviado con éxito!'


def obtener_valor(nombre_campo):
    """
    Función para obtener el valor de un campo en un formulario enviado por el método POST.

    Parámetros:
        - nombre_campo (str): El nombre del campo a obtener.

    Retorna:
        - str: El valor del campo especificado.
    """
    # Verificar si se envió el formulario por el método POST
    if request.method == 'POST':
        # Obtener el diccionario con los datos enviados por el formulario
        datos_formulario = request.form.to_dict()

        # Buscar el valor del campo especificado
        if nombre_campo in datos_formulario:
            return datos_formulario[nombre_campo]

    # Si no se envió el formulario por POST o el campo no existe, retornar None
    return None


@app.route('/enviar-correo', methods=['POST'])
def enviar_correo():
    if request.method == 'POST':
        # Configuración del servidor SMTP
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = '@gmail.com'
        smtp_password = '?'

        # Obtener los datos del formulario
        nombre = obtener_valor('nombre')
        email = obtener_valor('email')
        mensaje = obtener_valor('mensaje')

        # Crear el mensaje de correo electrónico
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = '@gmail.com' # Ingresa aquí el correo del destinatario
        msg['Subject'] = 'Nuevo mensaje de formulario'
        msg.attach(MIMEText(f'Nombre: {nombre}\nEmail: {email}\nMensaje: {mensaje}', 'plain'))

        # Iniciar sesión en el servidor SMTP y enviar el correo electrónico
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, '', msg.as_string())

        # Redirigir a la página de éxito
        return redirect(url_for('procesar_formulario'))

    else:
        return "Método no permitido"


if __name__ == '__main__':
    app.run(debug=True)
