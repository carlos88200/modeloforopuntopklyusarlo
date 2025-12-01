# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 09:40:12 2025

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








def proceso_entrada(pregunta):
    modelo = Ollama(model="llama3.2")
    
    #informacion 
    import pandas as pd
    documento = pd.read_excel(r"D:\carlos.gonzalez\Documents\documentosForo\3\Completo.xlsx")
    docs = []
    for index, row in documento.iterrows():
        texto = f"Nombre del articulo: {row['nombre de arcivo']}\nTexto del articulo: {row['texto']}"
        #docs.append(Document(page_content=texto, metadata={"index": index}))
        docs.append(Document(page_content=texto, metadata={"index": index}))
    #separar el documento en chunks
    # text_splitter = CharacterTextSplitter.from_ticktoken_encode(chuck_size= 750, chunk_overla=100)
    # text_splitter = RecursiveCharacterTextSplitter(chuck_size= 750, chunk_overla=100)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=750, chunk_overlap=100)

    doc_split = text_splitter.split_documents(docs)
    print('Guardando.....')
    
    #hacer embedding y guardar
    # embeddings = OllamaEmbeddings(model="llama3.2")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    
    
    #chroma
    # vectorestore = Chroma.from_documents(documents=doc_split, collection_name="rag_chroma",embedding = embeddings,)
    # print('Guardado')
    
    
    #fAISS
    
    
    # embedding_dim = len(embeddings.embed_query("hello world"))
    # index = faiss.IndexFlatL2(embedding_dim)
    
    # vector_store = FAISS(
    #     embedding_function=embeddings,
    #     index=index,
    #     docstore=InMemoryDocstore(),
    #     index_to_docstore_id={},
    # )
        
    # print('Guardando')
    # batch_size = 100  # Ajusta según memoria, 100 suele estar bien
    # # print("docSplit: ",doc_split)
    # for i in tqdm(range(0, len(doc_split), batch_size)):
    #     start = time.time()
    #     batch = doc_split[i:i+batch_size]
    #     vector_store.add_documents(batch)
    #     end = time.time()
    #     print(f"Batch {i//batch_size+1} guardado en {end-start:.2f} segundos")
        
      
        
      
        
      
    print("Preparando textos para embeddings...")
    all_texts = [doc.page_content for doc in doc_split]
    
    print(f"Total chunks a procesar: {len(all_texts)}")
    all_embeddings = []
    
    from tqdm import tqdm
    for i, text in enumerate(tqdm(all_texts, desc="Calculando embeddings")):
        # emb = embeddings.embed_query(text)
        emb = embeddings.embed_query(text)

        
        all_embeddings.append(emb)
        if (i + 1) % 50 == 0:
            print(f"  > Embeddings calculados para {i + 1} chunks")
    
    
    
    embedding_dim = len(all_embeddings[0])
    print(f"Dimensión del embedding: {embedding_dim}")
    
    print("Creando índice FAISS...")
    index = faiss.IndexFlatL2(embedding_dim) #creacion del indice vacio
    
    print("Agregando vectores al índice...")
    index.add(np.array(all_embeddings).astype('float32'))
    print(f"Vectores agregados: {index.ntotal}")
    
    print("Construyendo vector_store FAISS...")
    # def devoler(all_embeddings):
    #     return all_embeddings
    
    vector_store = FAISS(
        embedding_function=embeddings.embed_query,
        index=index,
        docstore=InMemoryDocstore({i: doc for i, doc in enumerate(doc_split)}),
        index_to_docstore_id={i: i for i in range(len(doc_split))},
    )
    print("Vector_store listo.")


        
        
        
        
        
        
        
    
    print('Guardado completado')
    print('Guardado')
    
    
    #otra forma sin guardar
    # #otra forma sin guardar
    # print("creando")
    # vector_store = FAISS.from_documents(doc_split, embeddings)
    # print("creado")
    
    with open('Datos.pkl', 'wb' ) as p:
        pickle.dump(vector_store, p)
        print("creado...")
        
if __name__ == '__main__':
    proceso_entrada("g")
    
    
   





