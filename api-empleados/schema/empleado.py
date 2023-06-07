from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Empleado(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(min_length=4, max_length=10)
    correo: str 
    telefono: str 
    direccion: str 
    fecha_ingreso: str
    especialidad: str 

    class Config:
        schema_extra = {
            'example':{
                'nombre':'Kuky',
                'correo':'kuky@gmail.com',
                'telefono':'12345678',
                'direccion':'graneros',
                'fecha_ingreso':datetime.now(),
                'especialidad':'instrumentista'
            }
        }