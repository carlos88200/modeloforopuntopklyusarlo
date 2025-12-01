# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 12:56:06 2025

@author: CARLOS.GONZALEZ
"""
from tqdm import tqdm
import time
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import pickle

from langchain_community.vectorstores import Chroma
# from langchain_community import embeddings
from langchain_ollama import OllamaEmbeddings 
# from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM as Ollama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
# from langchain.text_splitter import CharacterTextSplitter

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


#FAIS
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS





class pregunta:
    def __init__(self):
        pass
    
    def preguntando(self, pregunta):
        modelo = Ollama(model="llama3.2", streaming=True)
        with open(r"D:\carlos.gonzalez\Documents\documentosForo\3\Datos.pkl", "rb") as m:
           vector_store = pickle.load(m) 
        
        
        
        retiever = vector_store.as_retriever()
        docs = retiever.invoke(pregunta)
        print("\n--- Documentos recuperados ---")
        contardocs = 0
        for i, doc in enumerate(docs):
            #print(f"\n[Doc {i+1}]")
            #print(doc.page_content[:500])
            pass
        print('Retriveeeer')
        Template_rag = """respoden las preguntas usando unicamente la informacion del texto, tu respuesta debe de ser bien elaborada y no respuestas cortas
        {contexto}
        pregunta:{pregunta}"""
        promt_rag = ChatPromptTemplate.from_template(Template_rag)
        
        cadena = (
            {"contexto": retiever, "pregunta": RunnablePassthrough()}
            | promt_rag
            | modelo
            | StrOutputParser()
            )
        print("preguntandooooo....")
        respuesta = cadena.invoke(pregunta)
        for fragmento in respuesta:
            print(fragmento, end='', flush=True)
        #print('Respuesta: ', respuesta)
        return respuesta