# api/funciones_auxiliares.py

import html
import bleach  
# import bcrypt 
import datetime
from werkzeug.http import http_date
from flask import session

def sanitize_input(user_input):
    """
    Sanitiza la entrada de los usuarios para evitar inyecciones XSS.
    """
    escaped_input = html.escape(user_input)  # Escapa caracteres especiales en HTML
    return bleach.clean(escaped_input)  # Limpia cualquier HTML no permitido
    
#def cipher_password(password):
  #hashAndSalt = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(10));
  #return hashAndSalt
#def compare_password(password_hash,password):
   #if password_hash is None:
      #return False
   #try:
      #return bcrypt.checkpw(password,password_hash)
   #except:
      #return False


def prepare_response_extra_headers(include_security_headers):

    response_extra_headers = {
        # always
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
        'Last-Modified': http_date(datetime.datetime.now()),
        'Server':''
    }
    if include_security_headers:
        response_security_headers = {
            # X-Frame-Options: page can only be shown in an iframe of the same site
            'X-Frame-Options': 'SAMEORIGIN',
            # ensure all app communication is sent over HTTPS
            'Strict-Transport-Security': 'max-age=63072000; includeSubdomains',
            # instructs the browser not to override the response content type
            'X-Content-Type-Options': 'nosniff',
            # enable browser cross-site scripting (XSS) filter
            'X-XSS-Protection': '1; mode=block'
        }
        response_extra_headers.update(response_security_headers)

    return response_extra_headers

    
# Manejo de sesiones
def create_session(usuario, perfil):
    session["usuario"] = usuario
    session["perfil"] = perfil

def delete_session():
    session.clear()

def validar_session_normal():
    try:
        if session.get("usuario") and session["usuario"] != "":
            return True
        else:
            return False
    except:
        return False

def validar_session_admin():
    try:
        if session.get("usuario") and session["usuario"] != "" and session.get("perfil") == "admin":
            return True
        else:
            return False
    except:
        return False
