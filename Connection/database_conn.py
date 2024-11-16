from sqlalchemy import create_engine
from decouple import Config, RepositoryEnv
import os

# Definir la ruta al archivo .env
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(BASE_DIR, '../kafka/.env')  # Ajusta la ruta según tu estructura

# Cargar las configuraciones desde el archivo .env
config = Config(repository=RepositoryEnv(env_path))

# Crear el motor de conexión
engine = create_engine(
    f"postgresql+psycopg2://{config('USER_DB')}:{config('PASSWORD_DB')}@"
    f"{config('HOST_DB')}:{config('PORT_DB')}/{config('DATABASE_NAME')}"
)

def obtener_conexion():
    """
    Retorna el motor de conexión a la base de datos.
    """
    return engine
