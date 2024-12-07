from email.message import EmailMessage
from Django_S4PBG6.settings import EMAIL_SENDER, GOOGLE_APP_PASSWORD
import ssl
import smtplib


def send_complete_signup_mail(to, name : str):
    subject="Inventario: Cuenta creada pendiente de aprobación"

    body = f"""
    <body style="
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    color: white;">
        <header style="
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            display: flex;
            width: 100%;
            height: 120px;
            justify-content: center;
            align-items: center;
            gap: 20px;
            background-color: black;">
            <img src="https://germaniaiquique.cl/wp-content/uploads/2024/05/Escudo-Cia.png" alt="" style="
            width: 50px;
            ">
            <h1 style="
            color: white;
            font-family: Arial, Helvetica, sans-serif;
            ">Cuenta creada a la espera de aprobación
            </h1>
        </header>
        <section style="
        display: flex;
        flex-direction: column;
        width: 100%;
        height: 100%;
        padding: 20px;
        background-color: rgb(32, 32, 32);
        ">
            <h3 style="
            margin-top: 30px;
            margin-bottom: 40px;
            ">¡Saludos, {name}!<strong></strong></h3>
            <p>Has creado tu cuenta con éxito en el sistema. Sin embargo, aún no puedes acceder a él, ya que tu solicitud debe ser aprobada por el administrador.

                Cuando tu cuenta esté aprobada, recibirás otro correo electrónico de confirmación para que puedas iniciar sesión.
            </p>
        </section>
    </body>
    """

    simple_body = f"""
    ¡Saludos, {name.capitalize()}!
    Has creado tu cuenta con éxito en el sistema. Sin embargo, aún no puedes acceder a él, ya que tu solicitud debe ser aprobada por el administrador. Cuando tu cuenta esté aprobada, recibirás otro correo electrónico de confirmación para que puedas iniciar sesión."""

    em = EmailMessage()
    em["From"] = EMAIL_SENDER
    em["To"] = to
    em["Subject"] = subject
    #em.add_alternative(body, subtype='html')
    em.set_content(simple_body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(EMAIL_SENDER, GOOGLE_APP_PASSWORD)
        smtp.sendmail(EMAIL_SENDER, to, em.as_string())


# Mensaje para informar de solicitud aprobada
def send_active_account_mail(to, name : str):
    subject = "Inventario: Cuenta aprobada con éxito"

    simple_body = f"""
    Bienvenido/a, {name.capitalize()}!
    Tu solicitud de creación de cuenta ha sido aprobada con éxito. Ya puedes ingresar al sistema."""

    em = EmailMessage()
    em["From"] = EMAIL_SENDER
    em["To"] = to
    em["Subject"] = subject
    #em.add_alternative(body, subtype='html')
    em.set_content(simple_body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(EMAIL_SENDER, GOOGLE_APP_PASSWORD)
        smtp.sendmail(EMAIL_SENDER, to, em.as_string())