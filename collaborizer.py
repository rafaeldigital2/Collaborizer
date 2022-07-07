# -*- coding: utf-8 -*-
"""collaborizer.py

Developed by: Henrique Rodrigues
              Rafael Jardim



# Bibliotecas
"""
#!pip install reportlab

#!pip install Pillow

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
import seaborn as sns
from reportlab.pdfgen import canvas
from PIL import Image
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, NextPageTemplate, KeepInFrame, Frame
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import PIL.Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import HexColor

"""# Entradas

**Upload do CSV como alternativa**
"""

#Executar comente em caso de atualização do csv
#uploaded = files.upload()

df = pd.read_csv("/data/Respostas.csv")

#df = pd.read_csv("/content/RespostasCLAC.csv")

#df

"""# Teste de Banchmark Novo

**Funções**
"""

#criterios=["Objetivo","Produto","Artefato","Distribuição geográfica","Espaço compartilhado","Atividade","Tarefa compartilhada","Recurso","Decisão","Comprometimento/Motivação","Monitoramento de tarefas","Solução de problemas","Auxílio em organização","Definição de tarefas","Alteração de planejamento","Metodologia", "Capacitação","Resultado do grupo","Atuação do coordenador","Ferramentas", "Experiência da equipe","Adaptabilidade","Percepção/Interpretação","Valor", "Negociação", "Troca de informação", "Linguagem de Comunicação", "Senso comum", "Sincronismo/Meio de transmissão","Compartilhamento de conhecimento","Transparência"]
criterios=["Goal","Product","Artefact","Geographical distribution","Shared space","Activity/Task","Shared task","Resource","Decision","Commitment/Motivation","Monitoring tasks","Problems solutions","Assistance in organization","Tasks definition","Planning change","Methodology", "Capacity","Team result","Coordinator role","Tools", "Team experience","Adaptability","Perception/Interpretation","Value", "Negotiation", "Information change", "Communication language", "Common sense", "Synchronism/Transmission way","Knowledge sharing","Transparency"]

negPhrases=["The participants did not understand the goal they were working toward.","The results achieved could have been more meaningful.","Additional solutions were not achieved.","Participants had difficulty getting their work done in a distributed environment.","Shared virtual space was compromised.","Activities were not organized appropriately.","Tasks were not fully shared.","The available resources were not well used throughout the project.","Decisions were not made with a focus on the objectives.","Participants showed little motivation and needed encouragement in carrying out the activities.","The tasks could have been better monitored.","Problems that occurred were not solved efficiently.","There could have been supporting to improve the self-organization of the participants.","The tasks were not clear and well-defined.","After planning the activities, it was difficult to make adjustments.","The methodology used needs to be revised.","The complementary instructions were insufficient.","The participants need engagement.","The absence of the manager impacted the project.","The available tools were not efficient.","The experience of the participants was not relevant to the project.","The participants needed more preparation to act in unexpected situations.","There was difficulty in interpreting messages.","The participants did not prioritize the project's actions.","The negotiations of the activities between the participants were not assertive.","The exchange of information between the participants needs to be improved.","The language used needs to be improved to improve comprehension and understanding.","The participants did not have a common understanding of the project.","Synchronous communications did not meet the participants' needs efficiently.","Knowledge sharing needs to be improved.","The information made available needed to be more precise and more accessible."]

posPhrases=["The participants worked towards a common goal.","Significant results were achieved.","Additional solutions were achieved.","Participants were able to work in distributed environments.","The shared virtual space was used successfully.","Activities were well planned and organized.","The activities were shared efficiently.","The available resources were well used throughout the project.","Decisions were made with a focus on the objectives.","The participants demonstrated motivation and engagement in the tasks.","The tasks were well monitored.","Problems that occurred were solved efficiently.","There was support for the self-organization of the participants.","The tasks were clear and well-defined.","After planning the activities, occasional adjustments were successfully made.","The methodology used was adequate.","The supplementary instructions were adequate.","The participants were engaged and productive.","The manager was efficient in resolving impediments.","The existing tools were helpful.","The experience of the participants was fundamental to the project.","The participants executed the unexpected situations with ability.","The interpretation of the messages was efficient.","The participants prioritized the actions of the project.","The negotiations of the activities among the participants were assertive.","The exchange of information between the participants was efficient.","The language used was appropriate and understandable.","The participants had a common understanding of the project.","Synchronous communications met the needs efficiently.","The participants shared knowledge efficiently.","The information provided was precise and accessible."]


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
  return round(total,2)

def mediasQuest(vec):
  soma=0
  for i in range(1, len(vec)):
    print(vec[i])
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
    print(vec[i])
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
     print(vecT[i])
     if(vecT[i]>3):
       posT+=1
     if(vecT[i]<4):
       negT+=1
     print(vecT[i])
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
      #textoPos+=vetorTexto[i][0]+"<br />\n"
      textoPos+=posPhrases[i]+"<br />\n"
  return textoPos


def formaTextoAvaliacaoNeg(vetorTexto,min,max):
  textoNeg=""
  for i in range(min,max):
    if(vetorTexto[i][2]>vetorTexto[i][1] or vetorTexto[i][2]==vetorTexto[i][1]):
      #textoNeg+=vetorTexto[i][0]+"<br />\n"
      textoNeg+=negPhrases[i]+"<br />\n"
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

vec=df.iloc[:,2]
vetor=mediasQuest(vec)

#REF
#https://medium.com/horadecodar/gr%C3%A1ficos-de-barra-com-matplotlib-85628bfc4351



constructos = ['Cooperação', 'Coordenação', 'Comunicação','Colaboração']#labels
porcent = resultPercent()#valores

porcent.append(totalizadorMed())
plt.bar(constructos, porcent, color="blue")#estrutura do gráfico

# A label para o eixo Y
plt.ylabel('Score')

# A label para o eixo X
plt.xlabel('')

# O título do gráfico
plt.title('Results')


bars=plt.bar(np.arange(len(constructos)),porcent, color=['#fdfd96', '#fdfd96', '#fdfd96', '#77dd77'])

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x()+0.2, yval + .006, yval)



plt.xticks(np.arange(len(constructos)),['Cooperation', 'Coordination', 'Communication','Collaboration'])

# Chamamos o método show() para mostrar o gráfico na tela
plt.savefig("/results/resultColab.png",  dpi=300)
plt.show()

porcent

dfCorr=df
for i in range(2, 33):
  print(dfCorr.columns[i])
  print(criterios[i-2])
  df.rename(columns = {dfCorr.columns[i] : criterios[i-2]}, inplace = True)

dfCorrCoop = df.iloc[:, 2:12]

sns.set(font_scale=1.4)

ax = plt.subplots(figsize = (25, 25))
htmapimg=sns.heatmap(dfCorrCoop.corr(), annot = True,  cmap="YlOrRd", fmt='.2f', 
                  annot_kws={"size": 20});
plotimg=htmapimg.get_figure()
plotimg.savefig("/results/correlationCoop")

dfCorrCoord = df.iloc[:, 12:24]
dfCorrCoord
sns.set(font_scale=1.4)

ax = plt.subplots(figsize = (27, 27))
htmapimg=sns.heatmap(dfCorrCoord.corr(), annot = True,  cmap="YlOrRd", fmt='.2f', 
                  annot_kws={"size": 18});
plotimg=htmapimg.get_figure()
plotimg.savefig("/results/correlationCoord")

dfCorrComm = df.iloc[:, 24:33]
dfCorrComm
sns.set(font_scale=1.3)
ax = plt.subplots(figsize = (27, 27))
htmapimg=sns.heatmap(dfCorrComm.corr(), annot = True,  cmap="YlOrRd", fmt='.2f', 
                  annot_kws={"size": 18})
#bottom, top = htmapimg.get_ylim()
#htmapimg.set_ylim(bottom + 5, top - 2)
plotimg=htmapimg.get_figure()
plotimg.savefig("/results/correlationComm")

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
print(col)



col='negative'

Diverging.add_trace(go.Bar(x=dfpbars['negative'], y=dfpbars['criteria'], orientation='h', name='negative', customdata=dfpbars[col], hovertemplate="%{y}: %{x}"))

# Specifying the layout of the plot
image=Diverging.update_layout(barmode='overlay', height=700, width=700, yaxis_autorange='reversed', bargap=0.5, legend_orientation='h', legend_x=0.3, legend_y=-0.05)

image.write_image("/results/correlBars.png") 



"""# PDF REPORT"""

#Utilizado o reportlab
 
def create_pdf():
    pdf_file = '/results/report.pdf'
 
    can = canvas.Canvas(pdf_file)
    
    can.setFontSize(80)
    can.drawString(500, 550, "Collaborizer Report")
    can.setPageSize( landscape(letter) )
    can.setFontSize(40)
    can.drawString(430,500,"Collaborizer: the sizer of the agile collaboration ")
    can.setFontSize(18)
    can.setPageSize((1600, 900))
   
    can.showPage()
    can.setFontSize(60)
    can.drawString(580, 820, "Score Achieved")

    colabImgResized=PIL.Image.open("/results/resultColab.png")
    imagemAlt=colabImgResized.resize((1000,820))
    imagemAlt.save("resultColabAlt.png")

    can.drawImage('resultColabAlt.png',300,0)
   
    can.showPage()


    can.setFontSize(60)
    can.drawString(300, 820, "Variation of Agreement on Each Criterion")

    correlatImgResized=PIL.Image.open("/results/correlBars.png")
    imagemAlt=correlatImgResized.resize((1000,800))
    imagemAlt.save("correlBarsAlt.png")

    f = open('correlBarsAlt.png', 'rb')
    
    
    
    can.drawImage('correlBarsAlt.png',300,0)

    can.showPage()


    #Cooperation Correlation
    can.setFontSize(60)
    can.drawString(250, 820, "Correlation Between Criteria in Cooperation")

    correlatImgResized=PIL.Image.open("/results/correlationCoop.png")
    imagemAlt=correlatImgResized.resize((1000,800))
    imagemAlt.save("correlateCoopAlt.png")
    can.drawImage('correlateCoopAlt.png',400,0)
    can.showPage()
    

    #Coordination Correlation
    can.setFontSize(60)
    can.drawString(250, 820, "Correlation Between Criteria in Coordination")

    correlatImgResized=PIL.Image.open("/results/correlationCoord.png")
    imagemAlt=correlatImgResized.resize((1000,800))
    imagemAlt.save("correlateCoordAlt.png")
    can.drawImage('correlateCoordAlt.png',400,0)
    can.showPage()
    #Communication Correlation
    can.setFontSize(60)
    can.drawString(220, 820, "Correlation Between Criteria in Communication")

    correlatImgResized=PIL.Image.open("/results/correlationComm.png")
    imagemAlt=correlatImgResized.resize((1000,800))
    imagemAlt.save("correlateCommAlt.png")
    can.drawImage('correlateCommAlt.png',400,0)
    can.showPage()

   
    
    
    #Texto de avaliação da colaboração
   
    #Página Cooperação
    pergsPosNeg=calculaTodasPosNegText()
    textoPos=textosCoopPos()
    textoNeg=textosCoopNeg()

    can.setFontSize(60)
    can.drawString(300, 820, "Warnings and Matchings for Cooperation")
    can.setFontSize(30)
    can.drawString(1100, 750, "Matchings")
    can.drawString(300, 750, "Warnings")

    can.setStrokeColorRGB(0,0,0)
    can.setFillColorRGB(0,128,0)


    frame1 = Frame(28.2*cm, 0.1*cm, 28.1*cm, 24*cm, showBoundary=1)

    styles = getSampleStyleSheet()
    story = [Paragraph(textoPos, ParagraphStyle('Body', fontName="Helvetica", fontSize=22, leading=28, spaceBefore=6))]
    story_inframe = KeepInFrame(28*cm, 24*cm, story)
    frame1.addFromList([story_inframe], can)


    can.setFillColorRGB(255,0,0)
 
    frame1 = Frame(0.1*cm, 0.1*cm, 28.1*cm, 24*cm, showBoundary=1)

    styles = getSampleStyleSheet()
    story = [Paragraph(textoNeg, ParagraphStyle('Body', fontName="Helvetica", fontSize=22, leading=28, spaceBefore=6))]
    story_inframe = KeepInFrame(28*cm, 24*cm, story)
    frame1.addFromList([story_inframe], can)

    can.showPage()

    #Página coordenação

    pergsPosNeg=calculaTodasPosNegText()
    textoPos=textosCoordPos()
    textoNeg=textosCoordNeg()

    can.setFontSize(60)
    can.drawString(280, 820, "Warnings and Matchings for Coordination")
    can.setFontSize(30)
    can.drawString(1100, 750, "Matchings")
    can.drawString(300, 750, "Warnings")

    can.setStrokeColorRGB(0,0,0)
    can.setFillColorRGB(0,128,0)

    frame1 = Frame(28.2*cm, 0.1*cm, 28.1*cm, 24*cm, showBoundary=1)

    styles = getSampleStyleSheet()
    story = [Paragraph(textoPos,ParagraphStyle('Body', fontName="Helvetica", fontSize=22, leading=28, spaceBefore=6))]
    story_inframe = KeepInFrame(28*cm, 24*cm, story)
    frame1.addFromList([story_inframe], can)


    can.setFillColorRGB(255,0,0)

    frame1 = Frame(0.1*cm, 0.1*cm, 28.1*cm, 24*cm, showBoundary=1)

    styles = getSampleStyleSheet()
    story = [Paragraph(textoNeg, ParagraphStyle('Body', fontName="Helvetica", fontSize=22, leading=28, spaceBefore=6))]
    story_inframe = KeepInFrame(28*cm, 24*cm, story)
    frame1.addFromList([story_inframe], can)
    can.showPage()

    #Página comunicação

    pergsPosNeg=calculaTodasPosNegText()
    textoPos=textosComunicPos()
    textoNeg=textosComunicNeg()

    can.setFontSize(60)
    can.drawString(250, 820, "Warnings and Matchings for Communication")
    can.setFontSize(30)
    can.drawString(1100, 750, "Matchings")
    can.drawString(300, 750, "Warnings")

    can.setStrokeColorRGB(0,0,0)
    can.setFillColorRGB(0,128,0)
   
    frame1 = Frame(28.2*cm, 0.1*cm, 28.1*cm, 24*cm, showBoundary=1)
    styles = getSampleStyleSheet()
    story = [Paragraph(textoPos, ParagraphStyle('Body', fontName="Helvetica", fontSize=22, leading=28, spaceBefore=6))]
    story_inframe = KeepInFrame(28*cm, 24*cm, story)
    frame1.addFromList([story_inframe], can)


    can.setFillColorRGB(255,0,0)
   
    frame1 = Frame(0.1*cm, 0.1*cm, 28.1*cm, 24*cm, showBoundary=1)
    styles = getSampleStyleSheet()
    story = [Paragraph(textoNeg, ParagraphStyle('Body', fontName="Helvetica", fontSize=22, leading=28, spaceBefore=6))]
    story_inframe = KeepInFrame(28*cm, 24*cm, story)
    frame1.addFromList([story_inframe], can)
    can.showPage()



    can.save()
create_pdf()
