from sqlalchemy import Column, Integer, String

from config.base_datos import base


class Empleado(base):
    __tablename__='empleados'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    correo = Column(String)
    telefono = Column(String) 
    direccion = Column(String) 
    fecha_ingreso = Column(String)
    especialidad = Column(String)