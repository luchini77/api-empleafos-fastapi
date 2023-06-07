from fastapi import FastAPI, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List

from config.base_datos import sesion, motor, base
from schema.empleado import Empleado as EmpleadoSchema
from models.empleado import Empleado as EmpleadoModelo


app = FastAPI()
app.title = 'App de Empleados'
app.version = '1.0.1'

base.metadata.create_all(bind=motor)


#INICIO
@app.get('/', tags=['Inicio'])
def mensaje():
    return HTMLResponse('<h2>Titulo HTML desde FastApi</h2>')


#TODOS LOS EMPLEADOS
@app.get('/empleados', tags=['Empleados'], response_model=List[EmpleadoSchema], status_code=200)
def mostrar_empleados() -> List[EmpleadoSchema]:
    db = sesion()
    res = db.query(EmpleadoModelo).all()

    return JSONResponse(content=jsonable_encoder(res), status_code=200)


#AGREGAR UN EMPLEADO
@app.post('/empleados', tags=['Empleados'], response_model=dict, status_code=201)
def crea_empleado(empleado:EmpleadoSchema) -> dict:
    db = sesion()
    nuevo_empleado = EmpleadoModelo(**empleado.dict())
    db.add(nuevo_empleado)
    db.commit()

    return JSONResponse(content={'mensaje':'Empleado Creado'}, status_code=201)


#BUSCAR EMPLEADO POR ID
@app.get('/empleados/{id}', tags=['Empleados'], response_model=EmpleadoSchema, status_code=200)
def mostrar_empleado_id(id:int=Path(ge=1)) -> EmpleadoSchema:
    db = sesion()
    res = db.query(EmpleadoModelo).filter(EmpleadoModelo.id == id).first()

    if not res:
        return JSONResponse(content={'mensaje':'No se encontro empleado con ese ID'}, status_code=404)

    return JSONResponse(content=jsonable_encoder(res), status_code=200)


#BUSCAR EMPLEADOS POR ESPACIALIDAD
@app.get('/empleados/', tags=['Empleados'], response_model=List[EmpleadoSchema], status_code=200)
def mostrar_empleado_especialidad(especialidad:str=Query(min_length=4, max_length=20)) -> List[EmpleadoSchema]:
    db = sesion()
    res = db.query(EmpleadoModelo).filter(EmpleadoModelo.especialidad == especialidad).all()

    if not res:
        return JSONResponse(content={'mensaje':'No se encontro empleados con esa especialidad'}, status_code=404)

    return JSONResponse(content=jsonable_encoder(res), status_code=200)


#ACTUALIZAR INFORMACION DE EMPLEADOS
@app.put('/empleados/{id}', tags=['Empleados'], response_model=dict, status_code=200)
def actulizar_empleado(id:int, empleado:EmpleadoSchema) -> dict:
    db = sesion()
    res = db.query(EmpleadoModelo).filter(EmpleadoModelo.id == id).first()

    if not res:
        return JSONResponse(content={'mensaje':'No se encontro empleado con ese ID'}, status_code=404)

    res.nombre = empleado.nombre
    res.correo = empleado.correo
    res.telefono = empleado.telefono
    res.direccion = empleado.direccion
    res.fecha_ingreso = empleado.fecha_ingreso
    res.especialidad = empleado.especialidad

    db.commit()

    return JSONResponse(content={'mensaje':'Empleado Actualizado'}, status_code=200)


#ELIMINAR EMPLEADO
@app.delete('/empleados/{id}', tags=['Empleados'], response_model=dict, status_code=200)
def borrar_empleado(id:int) -> dict:
    db = sesion()
    res = db.query(EmpleadoModelo).filter(EmpleadoModelo.id == id).first()

    if not res:
        return JSONResponse(content={'mensaje':'No se encontro empleado con ese ID'}, status_code=404)
    
    db.delete(res)
    db.commit()

    return JSONResponse(content={'mensaje':'Empleado Eliminado'}, status_code=200)