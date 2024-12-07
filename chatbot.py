import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import YoutubeLoader

api_key = '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'
os.environ['GROQ_API_KEY'] = api_key

chat = ChatGroq(model='llama-3.1-70b-versatile')

def resposta_bot(mensagens, documento):
  mensagem_system = '''voce é um bot que responde o usuario de acordo com as necessidades dele: {informacoes}'''
  mensagens_modelo = [('system', mensagem_system)]
  mensagens_modelo += mensagens
  template = ChatPromptTemplate.from_messages(mensagens_modelo)
  chain = template | chat
  return chain.invoke({'informacoes': documento}).content


def carrega_site():
  url_site = input('Digite a url do site: ')
  loader = WebBaseLoader(url_site)
  lista_documentos = loader.load()
  documento = ''
  for doc in lista_documentos:
    documento += doc.page_content
  return documento

def carrega_youtube():
  url_youtube = input('Digite a url do vídeo: ')
  loader = YoutubeLoader.from_youtube_url(url_youtube,language=['pt'])
  lista_documentos = loader.load()
  documento = ''
  for doc in lista_documentos:
    documento += doc.page_content
  return documento

print('Bem-vindo ao AsimoBot')

texto_selecao = '''Digite 1 se você quiser conversar com um site
Digite 2 se você quiser conversar com um vídeo de youtube '''

while True:
  selecao = input(texto_selecao)
  if selecao == '1':
    documento = carrega_site()
    break
  if selecao == '2':
    documento = carrega_youtube()
    break
  print('Digite um valor entre 1 e 2')

mensagens = []
while True:
  pergunta = input('Usuario: ')
  if pergunta.lower() == 'x':
    break
  mensagens.append(('user', pergunta))
  resposta = resposta_bot(mensagens, documento)
  mensagens.append(('assistant', resposta))
  print(f'Bot: {resposta}')

print('Muito obrigado por usar o Bot')
