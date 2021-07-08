#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 11:10:36 2020

@author: appanna and hasnaa
"""


# Get today's date (datetime library). 
from datetime import date
import datetime
today=date.today().strftime('%d/%m/%Y')
print(today)

#Display a welcome message with both today’s date and explanations on your software.
print("Welcome to our app where you can enter the department name and find the stats of COVID patients in hospitals of the region as on today's date:", today,
      "\nThe stats which are accumulated (summed) for the month are:\n"
      "The accumulation of new admissions to the hospital ('acc_hosp') \n"
      "The accumulation of new intensive care admissions ('acc_intcare')\n"
      "The accumulation of home returns ('acc_home_returns') \n"
      "The accumulation of deaths ('acc_deaths') ")

#Let the user enter the (French) department or region (input).
dpt = input("Please enter the department:\n")
url = "https://data.opendatasoft.com/api/records/1.0/search/?dataset=donnees-hospitalieres-covid-19-dep-france%40public&rows=10000&facet=date&facet=countrycode_iso_3166_1_alpha3&facet=region_min&facet=nom_dep_min&facet=sex&refine.sex=Tous&refine.nom_dep_min=" + dpt
#print(url)

#Download the previous dataset in JSon format (requests library).
import requests
r = requests.get(url)
#print(r)
#print(r.json())



#Display the correctly formatted data set on the screen (with line breaks and indentations).
import json
raw_json = r.json()
#print(json.dumps(raw_json, indent=4, sort_keys=True))
#print(raw_json)

#Create a subfolder called “data” without error if it already exists.
import os
try:
    os.makedirs('data')
except Exception: #If folder already exists then there is an error. We can override this.
    pass


#Save data as a JSon file on the hard disk drive, in the “data” folder that you created previously.
json_data_formatted = json.dumps(raw_json, indent=4, sort_keys=True)
#print(json_data_formatted)
file = open("data/f_json.json",'w')
#file = open("/Users/appanna/Desktop/Uni Lasalle/Lectures/Jérome/Project_10_Dec/data/f_json.json",'w')
file.writelines(json_data_formatted) 
file.close()

#Once the dataset has been downloaded, extract and display information from the “description” part on the screen (refer to the description section).

#Construct new dictionary from list of dictionaries
records=raw_json['records']
dict_fields={}
list_recs=[]
for rec in records:# rec is a dict; records is a list
    for key,val in rec['fields'].items():
        if key=='date':  
            key1=key
            val1=val        
        if key=='day_hosp_new':  
            key2=key
            val2=val
        if key=='day_intcare_new':  
            key3=key
            val3=val
        if key=='day_out_new':  
            key4=key
            val4=val
        if key=='day_death_new':  
            key5=key
            val5=val
        if key=='day_hosp':  
            key6=key
            val6=val
        if key=='day_intcare':  
            key7=key
            val7=val
        if key=='tot_death':  
            key8=key
            val8=val
        if key=='tot_out':  
            key9=key
            val9=val
    dict_fields = {key1:val1,key2:val2,key3:val3,key4:val4,key5:val5,key6:val6,key7:val7,key8:val8,key9:val9}
    list_recs.append(dict_fields)


#Convert dictionary to dataframe
import pandas as pd
df=pd.DataFrame(list_recs)

#Create a month column
df['Month'] = pd.DatetimeIndex(df['date']).month
df['Year'] = pd.DatetimeIndex(df['date']).year
import calendar
df['Month_name'] = df['Month'].apply(lambda x: calendar.month_name[x])
df['Month_abb'] = df['Month'].apply(lambda x: calendar.month_abbr[x])
df= df.sort_values('date') #Sort the rows by date
#print(df)



#Rename the columns as per the description
df1=df.rename(columns = {'day_hosp_new':'acc_hosp','day_intcare_new':'acc_intcare','day_out_new':'acc_home_returns',
                            'day_death_new':'acc_deaths'})



#Groupby
disp=df1.groupby(['Year','Month_name'], sort=False).agg({
                         'acc_hosp': 'sum', 
                         'acc_intcare':'sum', 
                         'acc_home_returns':'sum', 
                         'acc_deaths':'sum'
                          })
disp.reset_index(inplace=True)
disp.to_csv('data/f_csv.csv') #save to csv



#Display the information:
time=datetime.datetime.now().strftime("%H:%M")

mess1="Hello,the time is "+time+ " on "+today+". The department chosen is: "+dpt+ "\nThe details are as follows:"
print(mess1)
print(disp)

#Additional information: Average occupency of patients hospitalised,int_care
disp_add=df.groupby(['Year','Month_name'], sort=False).agg({
                     'day_hosp': 'mean', 
                     'day_intcare':'mean', 
                      })
disp_add.reset_index(inplace=True)
disp_add.round(1).to_csv("data/faddi_csv.csv") #save to csv
disp_add=disp_add.round(1)

mess2="Described below is the average number of pateints per day who were hospitalized or in intensive care for the different months:"
addi=input("Would you like some additional information? yes/no\n")
while addi != 'yes' and addi != "no":
    addi=input("Would you like some additional information? yes/no\n")
if addi == "yes":
    print(mess2)
    print(disp_add)

    
#else:
    #print("Thank you for using the app!")

continue1= input("Now we will see barcharts for the monthly accumulated stats. Hit enter to continue!")



# display charts
    
#plot
import matplotlib.pyplot as plt

#For plots use abbreviated month name
plot_df=df1.groupby(['Year','Month_abb'], sort=False).agg({
                         'acc_hosp': 'sum', 
                         'acc_intcare':'sum', 
                         'acc_home_returns':'sum', 
                         'acc_deaths':'sum'
                          })
plot_df.reset_index(inplace=True)
#plot_df

x = plot_df['Month_abb'] # List of abscissas
height = plot_df['acc_hosp']# List of ordinates
width = 0.8 # bars widths
plt.title("Accumulated hospital admissions")
plt.bar(x, height, width, color='orange')  
plt.savefig('data/images/c1.png',bbox_inches='tight')
plt.show()


x = plot_df['Month_abb'] # List of abscissas
height = plot_df['acc_intcare']# List of ordinates
width = 0.8 # bars widths
plt.title("Accumulated intensive care admissions")
plt.bar(x, height, width, color='r')  
plt.savefig('data/images/c2.png',bbox_inches='tight')
plt.show()

x = plot_df['Month_abb'] # List of abscissas
height = plot_df['acc_home_returns']# List of ordinates
width = 0.8 # bars widths
plt.title("Accumulated home returns")
plt.bar(x, height, width, color='g') 
plt.savefig('data/images/c3.png',bbox_inches='tight') 
plt.show()

x = plot_df['Month_abb'] # List of abscissas
height = plot_df['acc_deaths']# List of ordinates
width = 0.8 # bars widths
plt.title("Accumulated deaths")
plt.bar(x, height, width, color='yellow')  
plt.savefig('data/images/c4.png',bbox_inches='tight')
plt.show()


#Charts with descriptive stats
### Mean of 7 day accumulations of patit stats
continue2= input("Charts below are for descriptive stats indicating the mean of 7 day accumulations in patient numbers. Hit enter to continue! ")

df2= df1.copy()
df2['wkmean_hosp']=df2['acc_hosp'].rolling(7).sum()
df2['wkmean_intcare']=df2['acc_intcare'].rolling(7).sum()
df2['wkmean_home_returns']=df2['acc_home_returns'].rolling(7).sum()
df2['wkmean_deaths']=df2['acc_deaths'].rolling(7).sum()

plot_df2=df2.groupby(['Year','Month_abb'], sort=False).agg({
        'wkmean_hosp': 'mean',
        'wkmean_intcare' : 'mean',
        'wkmean_home_returns' : 'mean',
        'wkmean_deaths':'mean'
        })
plot_df2.reset_index(inplace=True)


x = plot_df2['Month_abb'] # List of abscissas
height = plot_df2['wkmean_hosp']# List of ordinates
width = 0.8 # bars widths
plt.title("Mean weekly (sum of 7 days) hospital admissions")
plt.bar(x, height, width, color='orange')  
plt.savefig('data/images/m1.png',bbox_inches='tight')
plt.show()


x = plot_df2['Month_abb'] # List of abscissas
height = plot_df2['wkmean_intcare']# List of ordinates
width = 0.8 # bars widths
plt.title("Mean weekly (sum of 7 days) intensive care admissions")
plt.bar(x, height, width, color='red')  
plt.savefig('data/images/m2.png',bbox_inches='tight')
plt.show()

x = plot_df2['Month_abb'] # List of abscissas
height = plot_df2['wkmean_home_returns']# List of ordinates
width = 0.8 # bars widths
plt.title("Mean weekly (sum of 7 days) home returns")
plt.bar(x, height, width, color='g') 
plt.savefig('data/images/m3.png',bbox_inches='tight') 
plt.show()

x = plot_df2['Month_abb'] # List of abscissas
height = plot_df2['wkmean_deaths']# List of ordinates
width = 0.8 # bars widths
plt.title("Mean weekly (sum of 7 days) deaths")
plt.bar(x, height, width, color='yellow')  
plt.savefig('data/images/m4.png',bbox_inches='tight')
plt.show()


continue3= input("Next we will display the word clouds based on the number of patients per month for the different stats. Hit enter to continue!\n")
#Display a wordcloud
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

#For acc_hosp
#Generate the word string 
#For acc_hosp
word_string = ""
for ind,row in disp.iterrows():
    word_string += (row['Month_name']+" ")*row['acc_hosp']

wordcloud = WordCloud(max_words=100,    
                      stopwords= STOPWORDS,
                      collocations=False,
                      color_func=lambda *args, **kwargs: "orange",
                      background_color='white',
                      width=1200,     
                      height=1000).generate(word_string)
plt.title("Accumulated hospital admissions")
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
wordcloud.to_file("data/images/w1.png")

#For acc_intcare
word_string = ""
for ind,row in disp.iterrows():
    word_string += (row['Month_name']+" ")*row['acc_intcare']
wordcloud = WordCloud(max_words=100,    
                      stopwords= STOPWORDS,
                      collocations=False,
                      color_func=lambda *args, **kwargs: "red",
                      background_color='white',
                      width=1200,     
                      height=1000).generate(word_string)
plt.title("Accumulated intensive care admissions")
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
wordcloud.to_file("data/images/w2.png")

#For acc_home_returns
word_string = ""
for ind,row in disp.iterrows():
    word_string += (row['Month_name']+" ")*row['acc_home_returns']
wordcloud = WordCloud(max_words=100,    
                      stopwords= STOPWORDS,
                      collocations=False,
                      color_func=lambda *args, **kwargs: "green",
                      background_color='white',
                      width=1200,     
                      height=1000).generate(word_string)
plt.title("Accumulated home returns")
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
wordcloud.to_file("data/images/w3.png")

#For acc_deaths
word_string = ""
for ind,row in disp.iterrows():
    word_string += (row['Month_name']+" ")*row['acc_deaths']
wordcloud = WordCloud(max_words=100,    
                      stopwords= STOPWORDS,
                      collocations=False,
                      color_func=lambda *args, **kwargs: "yellow",
                      background_color='white',
                      width=1200,     
                      height=1000).generate(word_string)
plt.title("Accumulated deaths")
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
wordcloud.to_file("data/images/w4.png")


##Dynamic Word cloud with  personalized stop words
print("Now we will print dynamic user input based word clouds:\n")
#Create a list of user inputs
again='yes' #initialise repeating code block
ext=1 #initialise image save extension number
while again == 'yes':
    user_stop_words=[]
    input_word=''
    while input_word != 'end':
        input_word=input("Enter your stopwords and type 'end' when done:\n")
        if input_word != 'end':
            user_stop_words+=[input_word]   
    print("The stop words you entered are: ",user_stop_words)
    
    sel_col=input("Select your column for the word cloud from 'acc_hosp','acc_intcare','acc_home_returns','acc_deaths':\n")
    #disp[['Month_name',sel_col]]
    stop_words = user_stop_words + list(STOPWORDS) #append user generated list of stop words
    
    sel_color=input("Select color for the word cloud: black, red, orange, blue, yellow, green..\n")    
        
    word_string = ""
    for ind,row in disp[['Month_name',sel_col]].iterrows():
        word_string += (row['Month_name']+" ")*row[sel_col]
    wordcloud = WordCloud(max_words=100,    
                          stopwords= stop_words,
                          collocations=False,
                          color_func=lambda *args, **kwargs: sel_color,
                          background_color='white',
                          width=1200,     
                          height=1000).generate(word_string)
    plt.title(sel_col)
    plt.axis('off')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.show()
    
    save_wc_dy=input("Type 'yes' if you would like to save the wordcloud as an image. Else hit enter to continue!\n" )
    
    if save_wc_dy=='yes':  
        wordcloud.to_file("data/images/dyn_WC_"+str(ext)+".png")
        ext+=1
        print("The dynamic wordcloud is saved as 'dyn_WC_number' in the location /data/images" )
    
    again=input("If you want to run the worcloud generator again type 'yes', else hit enter to continue! ")


#Generate a multipage pdf
from matplotlib.backends.backend_pdf import PdfPages
with PdfPages('multipage_pdf.pdf') as pdf:    
    x = plot_df['Month_abb'] # List of abscissas
    height = plot_df['acc_hosp']# List of ordinates
    width = 0.8 # bars widths
    plt.title("Accumulated hospital admissions") 
    plt.bar(x, height, width, color='orange')  
    pdf.savefig()  # saves the current figure into a pdf page
    plt.close()
    
    word_string = ""
    for ind,row in disp.iterrows():
        word_string += (row['Month_name']+" ")*row['acc_hosp']
    
    wordcloud = WordCloud(max_words=100,    
                          stopwords= STOPWORDS,
                          collocations=False,
                          color_func=lambda *args, **kwargs: "orange",
                          background_color='white',
                          width=1200,     
                          height=1000).generate(word_string)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    pdf.savefig()  # saves the current figure into a pdf page
    plt.close()

   
    x = plot_df['Month_abb'] # List of abscissas
    height = plot_df['acc_home_returns']# List of ordinates
    width = 0.8 # bars widths
    plt.title("Accumulated home returns")
    plt.bar(x, height, width, color='g')  
    pdf.savefig()  # saves the current figure into a pdf page
    plt.close()
    
    word_string = ""
    for ind,row in disp.iterrows():
        word_string += (row['Month_name']+" ")*row['acc_home_returns']
    
    wordcloud = WordCloud(max_words=100,    
                          stopwords= STOPWORDS,
                          collocations=False,
                          color_func=lambda *args, **kwargs: "green",
                          background_color='white',
                          width=1200,     
                          height=1000).generate(word_string)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    pdf.savefig()  # saves the current figure into a pdf page
    plt.close()
    
    x = plot_df['Month_abb'] # List of abscissas 
    height = plot_df['acc_intcare']# List of ordinates
    width = 0.8 # bars widths
    plt.title("Accumulated intensive care admissions")
    plt.bar(x, height, width, color='r')  
    pdf.savefig()  # saves the current figure into a pdf page
    plt.close()
    
    word_string = ""
    for ind,row in disp.iterrows():
        word_string += (row['Month_name']+" ")*row['acc_intcare']
    
    wordcloud = WordCloud(max_words=100,    
                          stopwords= STOPWORDS,
                          collocations=False,
                          color_func=lambda *args, **kwargs: "red",
                          background_color='white',
                          width=1200,     
                          height=1000).generate(word_string)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    pdf.savefig()  # saves the current figure into a pdf page
    plt.close()
    
    x = plot_df['Month_abb'] # List of abscissas
    height = plot_df['acc_deaths']# List of ordinates
    width = 0.8 # bars widths
    plt.title("Accumulated deaths")
    plt.bar(x, height, width, color='yellow')  
    pdf.savefig()  # saves the current figure into a pdf page
    plt.close()
    
    word_string = ""
    for ind,row in disp.iterrows():
        word_string += (row['Month_name']+" ")*row['acc_deaths']
    
    wordcloud = WordCloud(max_words=100,    
                          stopwords= STOPWORDS,
                          collocations=False,
                          color_func=lambda *args, **kwargs: "yellow",
                          background_color='white',
                          width=1200,     
                          height=1000).generate(word_string)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    pdf.savefig()  # saves the current figure into a pdf page
    plt.close()
    
    fig = plt.figure(figsize=(15,0.5))
    plt.text(0, 1, mess1, horizontalalignment='left',
         verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
    plt.axis('off')
    pdf.savefig()
    plt.close()
    
    
    fig = plt.figure(figsize=(15,9))
    ax=plt.subplot(111)
    ax.axis('off')
    c = df.shape[1]
    plt.title('Primary hospital data')
    ax.table(cellText=disp.values, colLabels=disp.columns, bbox=[0,0,1,1])
    pdf.savefig()
    plt.close()
    
    fig = plt.figure(figsize=(15,0.5))
    plt.text(0, 1, mess2, horizontalalignment='left',
         verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))
    plt.axis('off')
    pdf.savefig()
    plt.close()
    
    fig = plt.figure(figsize=(15,9))
    ax=plt.subplot(111)
    ax.axis('off')
    c = df.shape[1]
    plt.title('Additional hospital data')
    ax.table(cellText=disp_add.values, colLabels=disp_add.columns, bbox=[0,0,1,1])
    pdf.savefig()
    plt.close()
    disp_add
    
    print("A multipage pdf file with the charts, wordclouds and tables has been generated in the working directory!")


#Generate a html page

tab1=disp.to_html()
tab2=disp_add.to_html()
tab1
html_string='''

<html>  
     <body>
         <img src="images/c1.png"
         width="275"
         height="231">
         
         <img src="images/c2.png"
         width="275"
         height="231">
         
         <img src="images/c3.png"
         width="275"
         height="231">
         
         <img src="images/c4.png"
         width="275"
         height="231">
     </body>
     <br> </br>
     <body>
         <img src="images/w1.png"
         width="275"
         height="231">
         
         <img src="images/w2.png"
         width="275"
         height="231">
         
         <img src="images/w3.png"
         width="275"
         height="231">
         
         <img src="images/w4.png"
         width="275"
         height="231">
     </body>
     <br> </br>
     
     <body>
         <img src="images/m1.png"
         width="275"
         height="231">
         
         <img src="images/m2.png"
         width="275"
         height="231">
         
         <img src="images/m3.png"
         width="275"
         height="231">
         
         <img src="images/m4.png"
         width="275"
         height="231">
     </body>
     <br> </br>
     
     
     <body>
        <h3>Primary Hospital information</h3>
        <p> '''+ mess1 +''' </p>
         ''' + tab1 + '''   
        <h3>Additional Hospital information</h3>
        <p> '''+ mess2 +''' </p>
        ''' + tab2 + '''
    </body>   
</html>     
'''

f = open('data/html_report.html','w')
f.write(html_string)
f.close()

print("A html report has been generated in the 'data' folder of the working directory!")


##Web application
from flask import Flask, render_template, Response 

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', he1 = mess1, 
                           tables1=[disp.to_html(classes='data',header=True)],
                           he2 = mess2, tables2=[disp_add.to_html(classes='data',header=True)])


@app.route("/charts")       
def charts():
    return render_template("disp.html")

@app.route("/")
def hello():
    return 

@app.route("/getcsv1")
def getcsv1():
    csv = disp.to_csv(line_terminator='\n')
    return Response(csv,
            mimetype="text/csv",
            headers={"Content-disposition":
                     "attachment; filename=csv1.csv"})

@app.route("/getjson1")
def getjson1():
    csv = disp.to_json(indent=4)
    return Response(csv,
            mimetype="application/json",
            headers={"Content-disposition":
                     "attachment; filename=json1.json"})
    
@app.route("/getcsv2")
def getcsv2():
    csv = disp_add.to_csv(line_terminator='\n')
    return Response(csv,
            mimetype="text/csv",
            headers={"Content-disposition":
                     "attachment; filename=csv2.csv"})

@app.route("/getjson2")
def getjson2():
    csv = disp_add.to_json(indent=4)
    return Response(csv,
            mimetype="application/json",
            headers={"Content-disposition":
                     "attachment; filename=json2.json"})

if __name__ == "__main__":
    app.run()




