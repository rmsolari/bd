#!/usr/bin/python3
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"var/www/bd/FlaskDB/flaskr/")
from __init__ import app as application
applicacion.secret_key='Add your secret key'

