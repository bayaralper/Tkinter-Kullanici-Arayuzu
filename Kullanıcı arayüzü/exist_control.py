from tkinter.font import names
from typing_extensions import IntVar
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import requests
from bs4 import BeautifulSoup
from tkinter import *
import os 
from typing_extensions import IntVar
from tkcalendar import *
import shutil
cred=credentials.Certificate("")#json isimlendirme
firebase_admin.initialize_app(cred)
db=firestore.client()  
path='' #control txtlerinin path'i
db_url=[]
db_url.append(os.listdir(path))#txtlerden anasayfa urllerini alıyor.
dict={}


for i in range(len(db_url[0])): #urlleri arrayde tuttu.
    temp=db_url[0][i]
    print(temp)
    url=open(str(str(path)+"/"+str(temp)),"r")
    url=url.read()
    dict[i]=url

def exist_control(collection_title):  
   docs=db.collection(collection_title).get() #dökümanlara erişti
 
   for doc in docs:
      doc_title=doc.id
      doc=doc.to_dict()
      r=requests.get(doc.get('url'),verify=False)
      try:
         data={}
         data=doc
         data['exist']='True'#Databaseye ekleme yaptı
         print(data)
      
      except ConnectionError:#Erişim hatası verirse
         data['exist']='False' #Databaseye ekleme yaptı.
      db.collection(collection_title).document(doc_title).set(data)   
   
class GUI:        
    def __init__(self, master):
        self.master = master

        master.title("Haber Arşivi Kullanıcı Arayüzü")
        master.geometry("300x800")#Boyut belirlendi
        self.mb=Menubutton(master,text='Url listesi')#Menu button oluşturuldu.
        self.mb.location(0,0)
        self.mb.menu=Menu(self.mb,tearoff=0)
        self.mb['menu']=self.mb.menu
        data={}
        for i in range(len(dict)):#Menu ekledi
           var=StringVar()
           self.mb.menu.add_checkbutton (label=dict[i],      #Menu buttona eleman eklendi on ve off değerleri atandı.
                              variable=var,onvalue=1,offvalue=0)
           data[i]=var
           self.mb.pack()
        
        self.button = Button(master, text="Continue",command=lambda:self.first_page(data),bg='red') #First_page komutu butona tıklandığında çağrıldı.
        self.button.pack()#Button eklemesi yapıldı.
        
        
    def first_page(self,data):
        for i in range(len(data)):   
          if data[i].get()==str(1):
              self.mb.destroy() #Menü,button sildirildi.(Yeni sayfa için)
              self.button.destroy()
              self.label_text=Label(self.master,text="Seçilen Haber Sitesi:")
              self.label_adress=Label(self.master,text=dict[i])
              self.collection_title=dict[i][12:17]
              exist_control(self.collection_title)#Exist ataması yapan fonksiyon çağrıldı.
              self.label_adress.pack()#Label eklendi.
              self.date1=Calendar(self.master,selectmode="day",year=2021,month=8,day=25)   #Takvim eklendi.
              self.date1.pack()    
              self.date2=Calendar(self.master,selectmode="day",year=2021,month=8,day=25) 
              self.date2.pack()
      
              
              self.date_button=Button(self.master,text="Tarih seçtiyseniz devam edin",command=lambda:self.get_date_data()) 
              self.date_button.pack()#Button eklendi
              
    def get_date_data(self):
       
        for self.widget in self.master.winfo_children():
           self.widget.destroy()

        self.label_date1=Label(self.master,text="İlk gunun tarihi:"+self.date1.get_date())#Tarih aldırıldı.
        self.label_date2=Label(self.master,text="İkinci gunun tarihi"+self.date2.get_date())
       
        
        self.label_date1.pack()
        self.label_date2.pack()
        self.mb=Menubutton(self.master,text='Url Getirme Seçenekleri')
        self.mb.menu=Menu(self.mb,tearoff=0)
        self.mb['menu']=self.mb.menu
        var=StringVar()
        var1=StringVar()
        var2=StringVar()
        data_exist={}
        self.mb.menu.add_checkbutton (label="exist olmayanlar",
                              variable=var,onvalue=1,offvalue=0)
        data_exist[0]=var
        self.mb.menu.add_checkbutton (label="exist olanlar",
                              variable=var,onvalue=3,offvalue=2)
        data_exist[1]=var1
        self.mb.menu.add_checkbutton (label="hepsi",
                              variable=var,onvalue=5,offvalue=4)
        data_exist[2]=var2
        self.mb.pack()

        self.veri_button=Button(self.master,text="Veri getir",command=lambda:self.veri_getir(data_exist))
        self.veri_button.pack()

    def veri_getir(self,data_exist):      
            collec=db.collection(self.collection_title)
            if data_exist[0].get()==str(1):

              query=collec.where('exist','==','False')#Database üzerinden sorgu yapıldı.
              results=query.get()#Dökümanlar alındı.

            elif data_exist[1].get()==str(3):
              query=collec.where('exist','==','True')
              results=query.get()

            else:
              results=db.collection(self.collection_title).get() #Veri alındı databaseden
            
            date1_choosen=self.date1.get_date().split('.')[0]#Gün ayırma işlemi yapıldı.
            date2_choosen=self.date2.get_date().split('.')[0]
            self.label_array=[]
            self.index=0
            
            for self.widget in self.master.winfo_children():#İtemler sildirildi.
              self.widget.destroy()
              
            for result in results:
               date=result.get('date')
               day=date.split(' ')[0]
               if date1_choosen<=day: #Databasedeki günler ile kullanıcının seçtiği günler karşılaştırıldı.
                  if date2_choosen>=day:
                     print(result.get('url'))
                     print(result.id)
                     page_id=result.id.split('_')[1]
                   #  file_url=#Pnglerin olduğu dosya +collection_title+'_'+page_id+'.png'
                    # target=#Pnglerin kullanıcıya tarihe göre sunulduğu dosya                     
                     self.label_array=Label(self.master,text=result.get('url'))
                     self.label_array.pack()
                     self.index+=1
                     #shutil.copy(file_url,target)  #Screenshot kopyalama işlemi yapıldı.

root = Tk()
my_gui = GUI(root)
root.mainloop()






