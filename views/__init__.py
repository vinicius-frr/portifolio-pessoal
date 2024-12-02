from flask import Blueprint

# Criar um blueprint para agrupar todas as views
bp = Blueprint("main", __name__)

# Importa todas as views
from .auth_views import *
from .dashboard_views import *
# from .project_views import *
from .general_views import *

# O blueprint será registrado no app principal (em app.py)