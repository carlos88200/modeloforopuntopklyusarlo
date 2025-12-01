import requests
import pandas
from tqdm import tqdm
# print(tqdm.__version__)
import time

inicip = time.time()






preguntas = pandas.read_csv(r"D:\carlos.gonzalez\Documents\documentosForo\3\pruebasmodelo\pregunta.csv", header=None, names=['preguntas'])

url = ' http://127.0.0.1:8000/pregunta'
respuestas =[]

for index, row in tqdm(preguntas.iterrows()):
    print('Contestandoo...')
    json = {'pregunta': row['preguntas']}
    respuesta = requests.post(url, json=json)
    print('respuesta....')
    respuestas.append(respuesta)

fin = time.time()

print(f'tiempo: {fin-inicip}')

Respuestas = []
r = ""
i = ""
for rep in respuestas:
    r = rep.content
    i = r.decode('utf-8')
    Respuestas.append(i)
    
    
preguntaslista = []
for index, row in preguntas.iterrows():
    preguntaslista.append(row['preguntas'])
    
 
dataframerespuestas = pandas.DataFrame(Respuestas, columns=['Respuesta'])
dataframepreguntas = pandas.DataFrame(preguntaslista, columns=['Pregunta'])
print(Respuestas)


dataframefinal = pandas.DataFrame(columns=['Preguntas', 'Respuestas'])

dataframefinal = pandas.concat([dataframepreguntas,dataframerespuestas], axis=1, ignore_index=True)

dataframefinal.columns=['Preguntas', 'Respuestas IA']

dataframefinal['Preguntas']=dataframefinal['Preguntas'].replace('<p>', '', regex=False)

dataframefinal.to_excel('rep.xlsx', index=False)

