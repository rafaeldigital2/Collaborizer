# -*- coding: utf-8 -*-
"""collaborizer.py

Developed by: Henrique Fernandes Rodrigues
              Rafael Jardim



# Bibliotecas
"""

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
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor

"""# Entradas

**Upload do CSV como alternativa**
"""


df = pd.read_csv("/data/Respostas.csv")

"""# Teste de Banchmark Novo

**Funções**
"""
criterios=["Goal","Product","Artefact","Geographical distribution","Shared space","Activity/Task","Shared task","Resource","Decision","Commitment/Motivation","Monitoring tasks","Problems solutions","Assistance in organization","Tasks definition","Planning change","Methodology", "Capacity","Team result","Coordinator role","Tools", "Team experience","Adaptability","Perception/Interpretation","Value", "Negotiation", "Information change", "Communication language", "Common sense", "Synchronism/Transmission way","Knowledge sharing","Transparency"]
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
  #total=0
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
     if(vecT[i]>3):
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


def formaTextoAvaliacaoPos(vetorTexto,min,max):
  textoPos=""
  for i in range(min,max):
    if(vetorTexto[i][1]>vetorTexto[i][2]):
      textoPos+=vetorTexto[i][0]+"<br />\n"
  return textoPos


def formaTextoAvaliacaoNeg(vetorTexto,min,max):
  textoNeg=""
  for i in range(min,max):
    if(vetorTexto[i][2]>vetorTexto[i][1] or vetorTexto[i][2]==vetorTexto[i][1]):
      textoNeg+=vetorTexto[i][0]+"<br />\n"
  return textoNeg

def textosCoopPos():
  return formaTextoAvaliacaoPos(calculaTodasPosNegText(),0,10)

def textosCoopNeg():
  return formaTextoAvaliacaoNeg(calculaTodasPosNegText(),0,10)

def textosCoordPos():
  return formaTextoAvaliacaoPos(calculaTodasPosNegText(),11,22)

def textosCoordNeg():
  return formaTextoAvaliacaoNeg(calculaTodasPosNegText(),11,22)

def textosComunicPos():
  return formaTextoAvaliacaoPos(calculaTodasPosNegText(),23,31)

def textosComunicNeg():
  return formaTextoAvaliacaoNeg(calculaTodasPosNegText(),23,31)


#formaTextoAvaliacaoPos(calculaTodasPosNegText())

#vec=df.iloc[:,2]
#vetor=mediasQuest(vec)

#REF
#https://medium.com/horadecodar/gr%C3%A1ficos-de-barra-com-matplotlib-85628bfc4351



constructos = ['Cooperation', 'Coordination', 'Communication','Colaboration']#labels
porcent = resultPercent()#valores

porcent.append(totalizadorMed())

# A label para o eixo Y
plt.ylabel('Percentage')

# A label para o eixo X
plt.xlabel('Constructors')

# O título do gráfico
plt.title('Average Result')




plt.bar(np.arange(len(constructos)),porcent, color=['blue', 'blue', 'blue', 'red'])#estrutura do gráfico

plt.xticks(np.arange(len(constructos)),constructos)
# Chamamos o método show() para mostrar o gráfico na tela
plt.savefig("/results/resultColab.png")
plt.show()



import seaborn as sns

house_df=df
f, ax = plt.subplots(figsize = (31, 31))
htmapimg=sns.heatmap(house_df.corr(), annot = True,  cmap="YlOrRd");
plotimg=htmapimg.get_figure()
plotimg.savefig("/results/correlation")

"""# Diverge Bar Chart"""

valores=calculaTodasPorcent()

d2=pd.DataFrame(columns=["criteria","positive", "negative"],data=valores)


dfpbars = d2
dfpbars.head()
# Preprocessing the dataset to extract only
# the necessary columns
categories = [
    'negative',
    'positive'
]

dfpbars.negative = dfpbars.negative * -1

  
# Creating a Figure
Diverging = go.Figure()
  

dfpbars=dfpbars.sort_values(by=['positive'],ascending=False)


col='positive'

Diverging.add_trace(go.Bar(x=dfpbars['positive'], y=dfpbars['criteria'], orientation='h', name=col, customdata=dfpbars[col], hovertemplate="%{y}: %{customdata}"))


col='negative'

Diverging.add_trace(go.Bar(x=dfpbars['negative'], y=dfpbars['criteria'], orientation='h', name='negative', customdata=dfpbars[col], hovertemplate="%{y}: %{x}"))

# Specifying the layout of the plot
image=Diverging.update_layout(barmode='overlay', height=700, width=700, yaxis_autorange='reversed', bargap=0.5, legend_orientation='h', legend_x=-1, legend_y=0)
image.write_image("/results/correlBars.png") 



#image.write_image("image.png")

"""# PDF REPORT"""

#Utilizado o reportlab
 
def create_pdf():
    pdf_file = '/results/report.pdf'


    can = canvas.Canvas(pdf_file)
    can.setFontSize(40)
    can.drawString(250, 550, "Collaborizer Report")
    can.setPageSize( landscape(letter) )
    can.setFontSize(30)
    can.drawString(100,200,"Collaborizer: the sizer of the agile collaboration ")
    can.setFontSize(18)
    can.drawString(100,100,"Developed by: Rafael Jardim; Henrique Rodrigues; Lidvaldo Santos; ")
    can.drawString(100,50,"Juliana França;  Adriana Vivacqua.")
    can.showPage()
    can.setFontSize(30)
    can.drawString(250, 550, "Score Achieved")
    can.drawImage('/results/resultColab.png',0,0)
    #can.SetPageSize()
    can.showPage()

    can.setFontSize(30)
    can.drawString(100, 550, "Variation of group agreement on each criteria")

    correlatImgResized=PIL.Image.open("/results/correlBars.png")
    imagemAlt=correlatImgResized.resize((700,500))
    imagemAlt.save("/results/correlBarsAlt.png")

    f = open('/results/correlBarsAlt.png', 'rb')
    
    
    
    can.drawImage('/results/correlBarsAlt.png',0,0)
    #can.SetPageSize()
    can.showPage()



    can.setFontSize(30)
    can.drawString(200, 550, "Correlation Between Criteria")

    correlatImgResized=PIL.Image.open("/results/correlation.png")
    imagemAlt=correlatImgResized.resize((700,500))
    imagemAlt.save("/results/correlateAlt.png")
    can.drawImage('/results/correlateAlt.png',0,0)
    can.showPage()


    

    


    #can.rect(5,5,width=100,height=100,stroke=1,fill=1)

    #Texto de avaliação da colaboração
   
    #Página Cooperação
    pergsPosNeg=calculaTodasPosNegText()
    textoPos0=textosCoopPos()
    textoNeg0=textosCoopNeg()

    can.setFontSize(30)
    can.drawString(90, 550, "Recomendations and Matchings for Cooperation")
    can.setFontSize(25)
    can.drawString(500, 450, "Matchings")
    can.drawString(100, 450, "Recomendations")

    can.setStrokeColorRGB(0,0,0)
    can.setFillColorRGB(0,128,0)
    #can.rect(0.1*cm,0.1*cm,width=14*cm,height=14*cm,stroke=1,fill=1)
    

    frame1 = Frame(14*cm, 0.1*cm, 14*cm, 14*cm, showBoundary=1)
    #can.drawString(400,450,textoPos)
    styles = getSampleStyleSheet()
    story = [Paragraph(textoPos0, ParagraphStyle('Body', fontName="Helvetica", fontSize=12, leading=28, spaceBefore=6))]
    story_inframe = KeepInFrame(14*cm, 14*cm, story)
    frame1.addFromList([story_inframe], can)


    can.setFillColorRGB(255,0,0)
    #can.rect(14*cm,0.1*cm,width=14*cm,height=14*cm,stroke=1,fill=1)
    
    frame2 = Frame(0.1*cm, 0.1*cm, 14*cm, 14*cm, showBoundary=1)
    #can.drawString(400,450,textoPos)
    styles = getSampleStyleSheet()
    story = [Paragraph(textoNeg0, ParagraphStyle('Body', fontName="Helvetica", fontSize=12, leading=28, spaceBefore=6))]
    story_inframe = KeepInFrame(14*cm, 14*cm, story)
    frame2.addFromList([story_inframe], can)

    can.showPage()
    #Página coordenação

    pergsPosNeg=calculaTodasPosNegText()
    textoPos1=textosCoordPos()
    textoNeg1=textosCoordNeg()

    can.setFontSize(30)
    can.drawString(80, 550, "Recomendations and Matchings for Coordination")
    can.setFontSize(25)
    can.drawString(500, 450, "Matchings")
    can.drawString(100, 450, "Recomendations")

    can.setStrokeColorRGB(0,0,0)
    can.setFillColorRGB(0,128,0)
    #can.rect(0.1*cm,0.1*cm,width=14*cm,height=14*cm,stroke=1,fill=1)
    
    frame3 = Frame(14*cm, 0.1*cm, 14*cm, 14*cm, showBoundary=1)
    #can.drawString(400,450,textoPos)
    styles = getSampleStyleSheet()
    story = [Paragraph(textoPos1,ParagraphStyle('Body', fontName="Helvetica", fontSize=12, leading=28, spaceBefore=6))]
    story_inframe = KeepInFrame(14*cm, 14*cm, story)
    frame3.addFromList([story_inframe], can)


    can.setFillColorRGB(255,0,0)
    #can.rect(14*cm,0.1*cm,width=14*cm,height=14*cm,stroke=1,fill=1)
    
    frame4 = Frame(0.1*cm, 0.1*cm, 14*cm, 14*cm, showBoundary=1)
    #can.drawString(400,450,textoPos)
    styles = getSampleStyleSheet()
    story = [Paragraph(textoNeg1, ParagraphStyle('Body', fontName="Helvetica", fontSize=12, leading=28, spaceBefore=6))]
    story_inframe = KeepInFrame(14*cm, 14*cm, story)
    frame4.addFromList([story_inframe], can)
    can.showPage()
    #Página comunicação

    pergsPosNeg=calculaTodasPosNegText()
    textoPos2=textosComunicPos()
    textoNeg2=textosComunicNeg()

    can.setFontSize(30)
    can.drawString(70, 550, "Recomendations and Matchings for Communication")
    can.setFontSize(25)
    can.drawString(500, 450, "Matchings")
    can.drawString(100, 450, "Recomendations")

    can.setStrokeColorRGB(0,0,0)
    can.setFillColorRGB(0,128,0)
    #can.rect(0.1*cm,0.1*cm,width=14*cm,height=14*cm,stroke=1,fill=1)
    
    frame5 = Frame(14*cm, 0.1*cm, 14*cm, 14*cm, showBoundary=1)
    #can.drawString(400,450,textoPos)
    styles = getSampleStyleSheet()
    story = [Paragraph(textoPos2, ParagraphStyle('Body', fontName="Helvetica", fontSize=12, leading=28, spaceBefore=6))]
    story_inframe = KeepInFrame(14*cm, 14*cm, story)
    frame5.addFromList([story_inframe], can)


    can.setFillColorRGB(255,0,0)
    #can.rect(14*cm,0.1*cm,width=14*cm,height=14*cm,stroke=1,fill=1)
    
    frame6 = Frame(0.1*cm, 0.1*cm, 14*cm, 14*cm, showBoundary=1)
    #can.drawString(400,450,textoPos)
    styles = getSampleStyleSheet()
    story = [Paragraph(textoNeg2, ParagraphStyle('Body', fontName="Helvetica", fontSize=12, leading=28, spaceBefore=6))]
    story_inframe = KeepInFrame(14*cm, 14*cm, story)
    frame6.addFromList([story_inframe], can)
    can.showPage()



    can.save()
create_pdf()
