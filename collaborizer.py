# -*- coding: utf-8 -*-
"""FerramentaNovoProcessamentoSurvey_alpha2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CHl5jZbZyqsxiqA77_issqdeywNxRIHz

# Bibliotecas
"""

#!pip install reportlab

#!pip install plotly>=4.0.0
#!wget https://github.com/plotly/orca/releases/download/v1.2.1/orca-1.2.1-x86_64.AppImage -O /usr/local/bin/orca
#!chmod +x /usr/local/bin/orca
#!apt-get install xvfb libgtk2.0-0 libgconf-2-4

import pandas as pd
import os 
#from google.colab import drive
#from google.colab import files
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
  
from reportlab.pdfgen import canvas
from PIL import Image
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, NextPageTemplate, KeepInFrame, Frame
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
import PIL.Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import HexColor

"""# Entradas

**Upload do CSV como alternativa**
"""


df = pd.read_csv("./dataset.csv")

"""# Teste de Banchmark Novo

**Funções**
"""

criterios=["Objetivo","Produto","Artefato","Distribuição geográfica","Espaço compartilhado","Atividade","Tarefa compartilhada","Recurso","Decisão","Comprometimento/Motivação","Monitoramento de tarefas","Solução de problemas","Auxílio em organização","Definição de tarefas","Alteração de planejamento","Metodologia", "Capacitação","Resultado do grupo","Atuação do coordenador","Ferramentas", "Experiência da equipe","Adaptabilidade","Percepção/Interpretação","Valor", "Negociação", "Troca de informação", "Linguagem de Comunicação", "Senso comum", "Sincronismo/Meio de transmissão","Compartilhamento de conhecimento","Transparência"]
def valDF(indexPartic, indexVals):#recupera valores do csv em relação a posição em tupla e coluna
  return df.iloc(0)[indexPartic][2+(1*indexVals)]#(num*indexVals) num refere ao espaçamento entre os valores úteis no csv


def valorPartic(partic):#valor resultado por participante
  totalPartic=0
  valsPartic=[]
  for i in range(0,31):
    totalPartic+=valDF(partic,i)
    
    
  totalPartic/=31*5
  totalPartic*=100
  return totalPartic

def valorCategoria(partic, valMin, valMax):
  totalCat=0
  numVals=0
  for i in range(valMin, valMax):
    totalCat+=valDF(partic,i)
    numVals+=1
  totalCat/=numVals
  return totalCat

def valCooperac(partic):
  return valorCategoria(partic,0,10)

def valCoord(partic):
  return valorCategoria(partic,10,22)

def valComunic(partic):
  return valorCategoria(partic,22,31)

def valorTotal():  #agrega o total de todos participantes realizando média aritmética

  valores=[]
  continua=True
  val=0
  medCoop=0
  medCoord=0
  medCom=0
  while(continua):
    
    try:
      medCoop+=valCooperac(val)
      medCoord+=valCoord(val)
      medCom+=valComunic(val)
      val+=1
      
    except IndexError as error:
      continua=False

  medCoop/=val
  valores.append(round(medCoop,3))
  medCoord/=val
  valores.append(round(medCoord,3))
  medCom/=val
  valores.append(round(medCom,3))
  #return round(total,3) # 3 casas decimais
  return valores #[cooperação, coordenação, comunicação]



def resultPercent():
  valores=valorTotal()
  for val in range(0,3):
    valores[val]=round(valores[val]/5*100,3)
  return valores


def totalizadorMed():
  valores=resultPercent()
  total=0
  for val in range(0,3):
    total+=valores[val]
  total/=3
  return round(total,3)

def mediasQuest(vec):
  soma=0
  for i in range(1, len(vec)):

    soma+=vec[i]
  soma/=len(vec)
  if(soma>2):
    cor='green'
  else:
    cor='red'
    soma*=-1
  vetor=[vec.name,soma,cor]
  return vetor 

def mediaTodasQuests():
  vetorTot=[]
  for i in range(1,32):
    vec=df.iloc[:,i]
    vetor=mediasQuest(vec)
    vetorTot.append(vetor)
  return vetorTot


def valsPosNeg(vec):
  pos=0
  neg=0
  for i in range(0, len(vec)):

    if(vec[i]>3):
      pos+=1
    else:
      neg+=1
  vetor=["",(pos/(pos+neg))*100,(neg/(pos+neg))*100]
  return vetor 



def calculaTodasPorcent():
  vetorTot=[]
  for i in range(2,32):
    vec=df.iloc[:,i]
    vetor=valsPosNeg(vec)
    vetor[0]=criterios[i-2]
    vetorTot.append(vetor)
  return vetorTot



def valoresPosNegText(vecT):
   posT=0
   negT=0
   for i in range(0, len(vecT)):

     if(vecT[i]>2):
       posT+=1
     if(vecT[i]<4):
       negT+=1

   vetorT=["",(posT),(negT)]
   return vetorT

def calculaTodasPosNegText():
  vetorTotT=[]
  for i in range(2,33):
    vecT=df.iloc[:,i]
    vetorT=valoresPosNegText(vecT)
    vetorT[0]=df.columns[i]
    vetorTotT.append(vetorT)
  return vetorTotT


def formaTextoAvaliacaoPos(vetorTexto):
  textoPos=""
  for i in range(0,len(vetorTexto)):
    if(vetorTexto[i][1]>vetorTexto[i][2]):
      textoPos+=vetorTexto[i][0]+"<br />\n"
  return textoPos


def formaTextoAvaliacaoNeg(vetorTexto):
  textoNeg=""
  for i in range(0,len(vetorTexto)):
    if(vetorTexto[i][2]>vetorTexto[i][1] or vetorTexto[i][2]==vetorTexto[i][1]):
      textoNeg+=vetorTexto[i][0]+"<br />\n"
  return textoNeg

formaTextoAvaliacaoPos(calculaTodasPosNegText())

vec=df.iloc[:,2]
vetor=mediasQuest(vec)

#REF
#https://medium.com/horadecodar/gr%C3%A1ficos-de-barra-com-matplotlib-85628bfc4351



constructos = ['Cooperação', 'Coordenação', 'Comunicação']#labels
porcent = resultPercent()#valores

plt.bar(constructos, porcent, color="blue")#estrutura do gráfico

# Aqui definimos as legendas de cada barra no eixo X
plt.xticks(constructos)

# A label para o eixo Y
plt.ylabel('Porcentagem')

# A label para o eixo X
plt.xlabel('Constructos')

# O título do gráfico
plt.title('Resultado das médias')



constructos = ['Fator de colaboração'] #labels
porcent = totalizadorMed() #valores

plt.bar(constructos, porcent, color="red") #estrutura do gráfico
 
# Chamamos o método show() para mostrar o gráfico na tela
plt.savefig("resultColab.png")
plt.show()

import numpy as np
import matplotlib.pyplot as plt


constructos = ['Fator de colaboração'] #labels
porcent = totalizadorMed() #valores

plt.bar(constructos, porcent, color="red") #estrutura do gráfico

# Aqui definimos as legendas de cada barra no eixo X
plt.xticks(constructos)

# A label para o eixo Y
plt.ylabel('Porcentagem')


# O título do gráfico
plt.title('Resultado das médias')
 
# Chamamos o método show() para mostrar o gráfico na tela
plt.show()

import seaborn as sns
#house_df = pd.read_csv('/kc-house-data.csv', encoding = 'ISO-8859-1')
house_df=df
f, ax = plt.subplots(figsize = (31, 31))
htmapimg=sns.heatmap(house_df.corr(), annot = True,  cmap="YlOrRd");
plotimg=htmapimg.get_figure()
plotimg.savefig("correlation")

"""# Diverge Bar Chart"""

valores=calculaTodasPorcent()

d2=pd.DataFrame(columns=["criterio","positivo", "negativo"],data=valores)
d2

dfpbars = d2
dfpbars.head()
# Preprocessing the dataset to extract only
# the necessary columns
categories = [
    'negative',
    'positive'
]

dfpbars.negativo = dfpbars.negativo * -1

  
# Creating a Figure
Diverging = go.Figure()
  

dfpbars=dfpbars.sort_values(by=['positivo'],ascending=False)


col='positivo'

Diverging.add_trace(go.Bar(x=dfpbars['positivo'], y=dfpbars['criterio'], orientation='h', name=col, customdata=dfpbars[col], hovertemplate="%{y}: %{customdata}"))


col='negativo'

Diverging.add_trace(go.Bar(x=dfpbars['negativo'], y=dfpbars['criterio'], orientation='h', name='negativo', customdata=dfpbars[col], hovertemplate="%{y}: %{x}"))

# Specifying the layout of the plot
image=Diverging.update_layout(barmode='overlay', height=700, width=700, yaxis_autorange='reversed', bargap=0.5, legend_orientation='h', legend_x=-1, legend_y=0)
image.write_image("correlBars.png") 



image.write_image("image.png")

"""# PDF REPORT"""


#Utilizado o reportlab
 
def create_pdf():
    pdf_file = 'report.pdf'
 
    can = canvas.Canvas(pdf_file)
    can.setFontSize(30)
    can.drawString(300, 550, "Collaborizer Report")
    can.setPageSize( landscape(letter) )
    can.setFontSize(30)
    can.drawString(100,500,"Collaborizer: the sizer of the agile collaboration ")
    can.setFontSize(18)
    can.drawString(100,450,"Developed by: Rafael Jardim; Henrique Rodrigues; Lidvaldo Santos; ")
    can.drawString(100,430,"Juliana França;  Adriana Vivacqua.")
    can.showPage()
    can.drawImage('./resultColab.png',0,0)
    can.showPage()
    f = open('./resultColab.png', 'rb')
    
    can.drawString(20, 800, "Second Page")
    correlatImgResized=PIL.Image.open("./correlation.png")
    imagemAlt=correlatImgResized.resize((800,600))
    imagemAlt.save("correlateAlt.png")
    can.drawImage('./correlateAlt.png',10,10)
    can.showPage()

    can.drawImage('./correlBars.png',0,0)
    can.showPage()

    pergsPosNeg=calculaTodasPosNegText()
    textoPos=formaTextoAvaliacaoPos(pergsPosNeg)
    textoNeg=formaTextoAvaliacaoNeg(pergsPosNeg)

    can.setFontSize(30)
    can.drawString(200, 550, "Positive and Negative Elements")
    can.setFontSize(25)
    can.drawString(200, 450, "Positive")
    can.drawString(500, 450, "Negative")

    can.setStrokeColorRGB(0,0,0)
    can.setFillColorRGB(0,128,0)
    can.rect(0.1*cm,0.1*cm,width=14*cm,height=14*cm,stroke=1,fill=1)
    
    frame1 = Frame(0.1*cm, 0.1*cm, 14*cm, 14*cm, showBoundary=1)

    styles = getSampleStyleSheet()
    story = [Paragraph(textoPos, styles['Normal'])]
    story_inframe = KeepInFrame(14*cm, 14*cm, story)
    frame1.addFromList([story_inframe], can)


    can.setFillColorRGB(255,0,0)
    can.rect(14*cm,0.1*cm,width=14*cm,height=14*cm,stroke=1,fill=1)
    
    frame1 = Frame(14*cm, 0.1*cm, 14*cm, 14*cm, showBoundary=1)

    styles = getSampleStyleSheet()
    story = [Paragraph(textoNeg, styles['Normal'])]
    story_inframe = KeepInFrame(14*cm, 14*cm, story)
    frame1.addFromList([story_inframe], can)



    can.save()
create_pdf()

