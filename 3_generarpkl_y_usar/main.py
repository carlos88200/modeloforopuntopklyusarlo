# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 12:44:54 2025

@author: CARLOS.GONZALEZ
"""

from typing import Union
from pydantic import BaseModel
from preguntar import pregunta as pregclass 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Pregpeticion(BaseModel):
    pregunta: str


from fastapi.responses import HTMLResponse
    
@app.get("/")
def read_root():
    with open('prueba.html', 'r', encoding='utf-8') as d:
        contenido = d.read()
        return HTMLResponse(content=contenido, status_code=200)

@app.post("/pregunta")
def read_item(pregunta: Pregpeticion):
    pr = pregclass()
    respuesta = pr.preguntando(pregunta.pregunta)
         
    return respuesta


import pyodbc
import datetime
@app.post("/cargardatos")
def datos():
    try:
        es = r"W-BDCLDESA12\BD2"
        llaves = f"DRIVER={{SQL server}}; SERVER={es}; DATABASE=DGEE_SIST; UID=foro_ce24.owner; PWD=f0roce0wner&"
        cone = pyodbc.connect(llaves)
        cursor = cone.cursor()
        sentencia = """
        select pr.ID_PREGUNTA as FOLIO,ASUNTO,cat.CATEGORIA as CATEGORIA ,cuest.NOMBRE_CUEST as GRUPOOPERATIVO,FECHA,pr.ESTATUS_PREGUNTA as ESTADO, pr.TEXTO_PREGUNTA
        from pregunta pr, CUESTIONARIOS cuest, CATEGORIAS cat, pregunta_categoria resp
        where cuest.ID_TIPO_CUEST = pr.CUESTIONARIO
        and pr.ID_PREGUNTA = resp.ID_PREGUNTA
        and cat.ID_CATEGORIA = resp.ID_CATEGORIA
        """ 
        cursor.execute(sentencia)
        results = cursor.fetchall()
        lista = []
        fecha =""
        #print(results)

        for resul in results:
            #print("resultadostime",resul[4])
            fecha = f'{resul[4].day}/{resul[4].month}/{resul[4].year}' 
            #print(fecha)
            diccionario = {'ID_PREGUNTA': resul[0], 'ASUNTO': resul[1],'CATEGORIA':resul[2],'GRUPOOPERATIVO':resul[3], 'FECHA': fecha, 'ESTATUS_PREGUNTA': resul[5], 'TEXTO_PREGUNTA': resul[6] }
            #print(diccionario) 
            lista.append(diccionario)
            # print('Agregado')
        return lista
    except Exception as e:
        print(e)

# def datos():
#     try:
#         es = r"W-BDCLDESA12\BD2"
#         llaves = f"DRIVER={{SQL server}}; SERVER={es}; DATABASE=DGEE_SIST; UID=foro_ce24.owner; PWD=f0roce0wner&"
#         cone = pyodbc.connect(llaves)
#         cursor = cone.cursor()
#         cursor.execute("select TEXTO_PREGUNTA from pregunta")
#         results = cursor.fetchall()
#         preguntas = [{"TEXTO_PREGUNTA": row[0]} for row in results]
#         print(preguntas)
#         return preguntas

#     except Exception as e:
#         print(e)

