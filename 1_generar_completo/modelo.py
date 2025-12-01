# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 08:32:58 2025

@author: CARLOS.GONZALEZ


"""


from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

from langchain.schema import(
    AIMessage,
    HumanMessage,
    SystemMessage)
import pandas as pd 
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate



#from langchain_core.prompts import ChatPromptTemplate
#from langchain_ollama.llms import OllamaLLM

modelo = OllamaLLM(model = "llama3.2")


# from langchain_core.messages import(
#     AIMessage,
#     HumanMessage,
#     SystemMessage)


# import pandas as pd

documento = pd.read_excel(r"D:\carlos.gonzalez\Documents\documentosForo\Completo.xlsx")
TablaJson = ""

for index, row in documento.iterrows():
    # print(row['nombre de arcivo'])
    TablaJson += "{\n"+f"Nombre del articulo: {row['nombre de arcivo']},\n Texto del articulo: {row['texto']}"+ "}\n"
    
   

print(documento.info)



# from langchain.schema import Document
#from langchain_core.documents import Document

docs=[]
docs.append(Document(page_content=TablaJson))



# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_huggingface import HuggingFaceEmbeddings
#from langchain_huggingface import HuggingFaceEmbeddings




#from langchain.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLm-L6-v2")

#from langchain_community.vectorstores import FAISS


db = FAISS.from_documents(docs, embedding)


template = """
Tu deber es contestar la pregunta usando los articulos 

pregunta:
{pregunta}
"""

# from langchain.prompts import PromptTemplate
#from langchain_core.prompts import PromptTemplate


QA_promt = PromptTemplate(input_variables=["pregunta"] , template=template)

retriever = db.as_retriever(search_kwargs={"k":10})

# from langchain.chains import RetrievalQA
# from langchain_community.chains import RetrievalQA
# from langchain.chains import RetrievalQA
# from langchain_community.chains import RetrievalQA
# from langchain_community.chains.qa import RetrievalQA
# from langchain_community.chains import RetrievalQA
#from langchain.chains import RetrievalQA
#from langchain.chains import RetrievalQA
# from langchain.chains.retrieval_qa import RetrievalQA





qa = RetrievalQA.from_chain_type(
    llm=modelo,
    retriever=retriever,
    chain_type_kwargs={"prompt": QA_promt}
)



res = input("pregunta: ")
print(qa.run(res))



