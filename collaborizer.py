# -*- coding: utf-8 -*-
"""Collaborizer.ipynb

Developed by:
Rafael Jardim
Henrique Rodrigues

"""
"""# Bibliotecas"""


import pandas as pd
import os 
from google.colab import drive
from google.colab import files

"""# Entradas"""

#importa arquivo csv do Google Drive
#arquivo csv obtido da planilha gsheet gerado pelo Google Forms
#https://docs.google.com/forms/d/e/1FAIpQLScadrUDBkBDNez6eZTQAqBQzM4_vJ-A-uKYhKFMaWxlL_4lYQ/viewform?usp=sf_link
#O CSV
#https://drive.google.com/file/d/14V-IkMOhKD3GUyhIoHvKMWd2XkXJkBNf/view?usp=sharing
drive.mount('/content/drive')
df = pd.read_csv('/content/drive/MyDrive/Respostas.csv')

"""**Upload do CSV como alternativa**"""

#Executar comente em caso de atualização do csv
uploaded = files.upload()

df = pd.read_csv("/content/Avaliação da Colaboração Modelo 3C - PPGI - UFRJ .csv")

df = pd.read_csv("/content/Respostas.csv")

#visualização dos dados para checagem
df

"""# UMUX

**Funções**
"""

def valDF(indexPartic, indexVals):#recupera valores do csv em relação a posição em tupla e coluna
  return df.iloc(0)[indexPartic][2+(1*indexVals)]#(num*indexVals) num refere ao espaçamento entre os valores úteis no csv
  
def even(valor):#tratamento do valor par
  valorFinal=7-valor
  return valorFinal

def odd(valor):#tratamento do valor ímpar
  valorFinal=valor-1
  return valorFinal

def valorPartic(partic):#valor resultado por participante
  totalPartic=0
  for i in range(0,4):
    valor=valDF(partic,i)
    if(valor%2==0):
      totalPartic+=even(valor)
    else:
      totalPartic+=odd(valor)

  totalPartic/=24
  totalPartic*=100
  return totalPartic

def valorTotal():  #agrega o total de todos participantes realizando méida aritmética
  total=0
  continua=True
  val=0
  while(continua):
    try:
      total+=valorPartic(val)
      val+=1
    except IndexError as error:
      continua=False
  total/=val
  return round(total,3) # 3 casas decimais

valDF(0,0)

"""**Resultado Teste**"""

valorTotal()

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

vetor[0]

criterios[0]

vec=df.iloc[:,2]
vetor=mediasQuest(vec)

df.iloc[:,2]

vec[0]

mediaTodasQuests()

calculaTodasPorcent()

valorTotal()

resultPercent()

#REF
#https://medium.com/horadecodar/gr%C3%A1ficos-de-barra-com-matplotlib-85628bfc4351
import numpy as np
import matplotlib.pyplot as plt


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

# A label para o eixo X
#plt.xlabel('')

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

htmapimg.get_figure()

"""# Diverge Bar Chart"""

valores=calculaTodasPorcent()

valores

len(valores[:][0])

d2=pd.DataFrame(columns={"criteri","positivo", "negativ"},data=valores)
d2

d2

valores=mediaTodasQuests()
  
#for i in range(32):
    # Colour of bar chart is set to red if the sales 
    # is < 60000 and green otherwise
    
    
  
# Sort values from lowest to highest
d2.sort_values('val', inplace=True)
  
# Resets initial index in Dataframe to None
d2.reset_index(inplace=True)
  
# Draw plot
plt.figure(figsize=(28, 20), dpi=80)
  
# Plotting the horizontal lines
plt.hlines(y=d2.index, xmin=0, xmax=d2.val,
           color=d2.cor, alpha=0.4, linewidth=5)
  
# Decorations
# Setting the labels of x-axis and y-axis
plt.gca().set(ylabel='Quarter', xlabel='Sales')
  
# Setting Date to y-axis
plt.yticks(d2.index, d2.frase, fontsize=12)
  
# Title of Bar Chart
plt.title('Diverging Bars Chart Example', fontdict={
          'size': 20})
  
# Optional grid layout
plt.grid(linestyle='--', alpha=0.5)
  
# Displaying the Diverging Bar Chart
plt.show()

vec=df.iloc[:,2]

vec.name

vetor=[]

len(vec)

vec.iloc(0)[1]

df

df.columns[:]

!pip install -U kaleido

import pandas as pd
import plotly.graph_objects as go
  
  
df = d2
df.head()
  
# Preprocessing the dataset to extract only
# the necessary columns
categories = [
    'negative',
    'positive'
]
  
# Construct a pivot table with the column
# 'airline' as the index and the sentiments
# as the columns

  
# Include the sentiments - negative, neutral
# and positive
#gfg = gfg[categories]
  
# Representing negative sentiment with negative
# numbers
df.negativ = df.negativ * -1

  
# Creating a Figure
Diverging = go.Figure()
  
# Iterating over the columns
#for col in df.columns[1:]:
col='positivo'
# Adding a trace and specifying the parameters
# for negative sentiment
Diverging.add_trace(go.Bar(x=df['positivo'], y=df['criteri'], orientation='h', name=col, customdata=df[col], hovertemplate="%{y}: %{customdata}"))
print(col)

#for col in df.columns[1:]:
col='negativ'
# Adding a trace and specifying the parameters
# for negative sentiment
Diverging.add_trace(go.Bar(x=df['negativ'], y=df['criteri'], orientation='h', name='negativ', customdata=df[col], hovertemplate="%{y}: %{x}"))
#print(col)

#for col in df.columns:
  
    # Adding a trace and specifying the parameters
    # for positive and neutral sentiment
    #Diverging.add_trace(go.Bar(x=df[col], y=df.index, orientation='h', name=col, hovertemplate="%{x}: %{x}"))
  
# Specifying the layout of the plot
image=Diverging.update_layout(barmode='overlay', height=700, width=700, yaxis_autorange='reversed', bargap=0.5, legend_orientation='h', legend_x=1, legend_y=0)
#Diverging.update_layout(barmode='overlay', height=700, width=700, yaxis_autorange='reversed', bargap=0.5, legend_orientation='h', legend_x=1, legend_y=0)
#image.write_image("yourfile.png") 
#image.write_image("yourfile.png")

image

image.write_image("image.png")

"""# PDF REPORT"""

!pip install fpdf

import os
import shutil
import numpy as np
import pandas as pd
import calendar
from datetime import datetime
from fpdf import FPDF

import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297
        
    def header(self):
        # Custom logo and positioning
        # Create an `assets` folder and put any wide and short image inside
        # Name the image `logo.png`
        #self.image('assets/logo.png', 10, 8, 33)
        self.set_font('Arial', 'B', 11)
        self.cell(self.WIDTH - 80)
        self.cell(60, 1, 'Sales report', 0, 0, 'R')
        self.ln(20)
        
    def footer(self):
        # Page numbers in the footer
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def page_body(self, images):
        # Determine how many plots there are per page and set positions
        # and margins accordingly
        if len(images) == 3:
            self.image(images[0], 15, 25, self.WIDTH - 30)
            self.image(images[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
            self.image(images[2], 15, self.WIDTH / 2 + 90, self.WIDTH - 30)
        elif len(images) == 2:
            self.image(images[0], 15, 25, self.WIDTH - 30)
            self.image(images[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
        else:
            self.image(images[0], 15, 25, self.WIDTH - 30)
            
    def print_page(self, images):
        # Generates the report
        self.add_page()
        self.page_body(images)

PLOT_DIR = 'plots'

def construct():
    # Delete folder if exists and create it again
    try:
        shutil.rmtree(PLOT_DIR)
        os.mkdir(PLOT_DIR)
    except FileNotFoundError:
        os.mkdir(PLOT_DIR)
        
    # Iterate over all months in 2020 except January
    for i in range(2, 13):
        # Save visualization
        plot(data=generate_sales_data(month=i), filename=f'{PLOT_DIR}/{i}.png')
        
    # Construct data shown in document
    counter = 0
    pages_data = []
    temp = []
    # Get all plots
    files = os.listdir(PLOT_DIR)
    # Sort them by month - a bit tricky because the file names are strings
    files = sorted(os.listdir(PLOT_DIR), key=lambda x: int(x.split('.')[0]))
    # Iterate over all created visualization
    for fname in files:
        # We want 3 per page
        if counter == 3:
            pages_data.append(temp)
            temp = []
            counter = 0

        temp.append(f'{PLOT_DIR}/{fname}')
        counter += 1

    return [*pages_data, temp]



def plot(data: pd.DataFrame, filename: str) -> None:
    plt.figure(figsize=(12, 4))
    plt.grid(color='#F2F2F2', alpha=1, zorder=0)
    plt.plot(data['Date'], data['ItemsSold'], color='#087E8B', lw=3, zorder=5)
    plt.title(f'Sales 2020/{data["Date"].dt.month[0]}', fontsize=17)
    plt.xlabel('Period', fontsize=13)
    plt.xticks(fontsize=9)
    plt.ylabel('Number of items sold', fontsize=13)
    plt.yticks(fontsize=9)
    plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()
    return
              
# Test
december = generate_sales_data(month=12)
plot(data=december, filename='december.png')

plots_per_page = construct()
plots_per_page

pdf = PDF()
img=htmapimg.get_figure()
img.savefig("out.png")
pdf.print_page("out.png")
    
pdf.output('SalesRepot.pdf', 'F')



"""# Report test 2"""

!pip install reportlab

from reportlab.pdfgen import canvas
from PIL import Image
 
def create_pdf():
    pdf_file = 'multipage.pdf'
 
    can = canvas.Canvas(pdf_file)
    
    can.drawString(350, 550, "Collaborizer Report")
    can.setPageSize( landscape(letter) )
   
    can.drawCentredString(100,100,"TESTE")
    can.drawString(100,500,"Collaborizer: the sizer of the agile collaboration ")
    can.drawString(100,450,"\n Developed by: Rafael Jardim; Henrique Rodrigues; Lidvaldo Santos; Juliana França;  Adriana Vivacqua.")
    can.drawImage('/content/resultColab.png',0,0)
    #can.SetPageSize()
    can.showPage()
    f = open('/content/resultColab.png', 'rb')
    
    #can.append( Image(f,width=8*cm,height=6*cm) )
    #can.ap
    can.drawString(20, 800, "Second Page")
    correlatImgResized=Image.open("/content/correlation.png")
    imagemAlt=correlatImgResized.resize((800,600))
    imagemAlt.save("correlateAlt.png")
    can.drawImage('/content/correlateAlt.png',10,10)
    can.showPage()

    can.drawImage('/content/newplot.png',0,0)
    #can.SetPageSize()
    can.showPage()
 
    can.save()
create_pdf()

valores[0][0]="a"

d2=pd.DataFrame(columns={"cor","frase","val"},data=valores)

from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, NextPageTemplate
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm




data = [{"a": 1, "b": 2}, {"c": 3, "d":4}]

def create_pdf():
   
    story = []
    
    # Initialise the simple document template
    doc = SimpleDocTemplate("report.pdf",
                            page_size=landscape(A4),
                            bottomMargin=.4 * inch,
                            topMargin=.4 * inch,
                            rightMargin=.8 * inch,
                            leftMargin=.8 * inch)
    

    
    story.append(NextPageTemplate('landscape'))
    # set the font style
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    for count, d in enumerate(data, 1):
        p_count = Paragraph(f" Data: {count} ")
        story.append(Spacer(1, 12))
        story.append(p_count)
        for k, v in d.items():
            # extract and add key value pairs to PDF
            p = Paragraph(k + " : " + str(v), styleN)
            story.append(p)
            story.append(Spacer(1, 2))
    # build PDF using the data

    f = open('/content/resultColab.png', 'rb')

    story.append( Image(f,width=8*cm,height=6*cm) )

    f1 = open('/content/correlation.png', 'rb')

    story.append( Image(f1,width=20*cm,height=20*cm) )
    
    
    
    doc.build(story)

create_pdf()

df



import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import seaborn as sns
#sns.set()
#%matplotlib notebook
#plt.style.use('classic')

class_list = ['test1','test2','test3','test4','test5','test6','test7']
data = pd.DataFrame(data=zip(class_list,average_length,num_entries),columns=['Class','Lens','Nums'])
data.set_index('Class', inplace=True)

font_color = '#525252'
hfont = {'fontname':'Calibri'}
#facecolor = '#eaeaf2'
color_red = '#fd625e'
color_blue = '#01b8aa'
index = data.index
column0 = data['Lens']
column1 = data['Nums']
title0 = "Title 1"
title1 = 'Title 2'

fig, axes = plt.subplots(figsize=(10,5), facecolor=facecolor, ncols=2,sharey=True)
fig.tight_layout()

axes[0].barh(index, column0, align='center', color=color_red, zorder=10)
axes[0].set_title(title0, fontsize=18, pad=15, color=color_red, **hfont)
axes[1].barh(index, column1, align='center', color=color_blue, zorder=10)
axes[1].set_title(title1, fontsize=18, pad=15, color=color_blue, **hfont)


# If you have positive numbers and want to invert the x-axis of the left plot
axes[0].invert_xaxis() 


# To show data from highest to lowest
plt.gca().invert_yaxis()

axes[0].set(yticks=data.index, yticklabels=data.index)
axes[0].yaxis.tick_left()
axes[0].tick_params(axis='y', colors='white') # tick color

axes[1].set_xticklabels(['0','20', '40', '60', '80', '100', '120'])


for label in (axes[0].get_xticklabels() + axes[0].get_yticklabels()):
    label.set(fontsize=13, color=font_color, **hfont)
for label in (axes[1].get_xticklabels() + axes[1].get_yticklabels()):
    label.set(fontsize=13, color=font_color, **hfont)
    
plt.subplots_adjust(wspace=0, top=0.85, bottom=0.1, left=0.18, right=0.95)
plt.show()