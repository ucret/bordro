
import streamlit as st
import pandas as pd
import numpy as np
import math as mt


Aylık = [0,1,2,3,4,5,6,7,8,9,10,11] #Aylık Ücret
Sabit = [0,1,2,3,4,5,6,7,8,9,10,11] # Aylık ücret dışındaki sabit ücretler
ilave = [0,1,2,3,4,5,6,7,8,9,10,11] #Ay içinde ödenen değişken ücret
kvm = [0,1,2,3,4,5,6,7,8,9,10,11,12] #kümulatif gelir matrahı
vm = [0,1,2,3,4,5,6,7,8,9,10,11] # vergi matrahı
sskm = [0,1,2,3,4,5,6,7,8,9,10,11] #Emekli sandığı matrahı
sske = [0,1,2,3,4,5,6,7,8,9,10,11] #Emekli sandığı payı
sski = [0,1,2,3,4,5,6,7,8,9,10,11] #İşsizlik çalışan payı
dv = [0,1,2,3,4,5,6,7,8,9,10,11] #damga vergisi
idv =  [37.98,37.98,37.98,37.98,37.98,37.98,49.12,49.12,49.12,49.12,49.12,49.12] # vergi istisnası
Toplam = [0,1,2,3,4,5,6,7,8,9,10,11] #Toplam Brüt ücret
munzam = [0,1,2,3,4,5,6,7,8,9,10,11] # Munzam Sandik payı

igv = [638.01,638.01,638.01,638.01,638.01,638.01,825.05,1051.11,1100.07,1100.07,1100.07,1100.07] #Gelir vergisi istisnası
tavan = [5004*7.5,5004*7.5,5004*7.5,5004*7.5,5004*7.5,5004*7.5,6471*7.5,6471*7.5,6471*7.5,6471*7.5,6471*7.5,6471*7.5] #Emekli sandığı tavanı
devreden1 = [0,0,0,0,0,0,0,0,0,0,0,0,0] #birinci devreden matrah
devreden2 = [0,0,0,0,0,0,0,0,0,0,0,0,0] #ikinci devreden matrah
kullan1 = [0,0,0,0,0,0,0,0,0,0,0,0] # 1. devreden matrahtan kullanılan
kullan2 = [0,0,0,0,0,0,0,0,0,0,0,0] # 2. devreden matrahtan kullanılan
dtoplam = [0,0,0,0,0,0,0,0,0,0,0,0] #devreden toplam
ktoplam = [0,0,0,0,0,0,0,0,0,0,0,0] # devreden matrah kullanılan

net = [0,1,2,3,4,5,6,7,8,9,10,11] # net gelir
gv = [0,1,2,3,4,5,6,7,8,9,10,11] # gelir vergisi

def vergi(kum, matrah): # Vergi hesaplama fonksiyonu, Kümulatif matrah ve aylık matrah
    v = [32000,70000,250000,880000] # vergi dilimleri
    o = [0.15,0.2,0.27,0.35,0.4] #vergi oranları
    t= kum + matrah #ara kümulatif matrah
    if t <= v[0]:
       return matrah*o[0]
    elif t <= v[1]:
       return max((v[0]-kum),0)*o[0] + (matrah-max((v[0]-kum),0))*o[1]
    elif t <= v[2]:
       return max((v[0]-kum),0)*o[0] + max((v[1]-kum),0)*o[1] + (matrah-max((v[1]-kum),0)-max((v[0]-kum),0))*o[2]
    elif t <= v[3]:
        return max((v[0]-kum),0)*o[0] + max((v[1]-kum),0)*o[1] + max((v[2]-kum),0)*o[2] + (matrah-max((v[2]-kum),0)-max((v[1]-kum),0)- max((v[0]-kum),0))*o[3]
    else:
       return max((v[0]-kum),0)*o[0] + max((v[1]-kum),0)*o[1] + max((v[2]-kum),0)*o[2] + max((v[3]-kum),0)*o[3]+ (matrah-max((v[3]-kum),0)-max((v[2]-kum),0)-max((v[1]-kum),0)-max((v[0]-kum),0))*o[4]
    
    
    


c1,c2,c3 = st.columns(3) # streamlit uygulama kodları

with c1: # streamlit uygulama kodları
    Aylık[0] = st.number_input(label= "Ocak Aylık Ücret", step=100, value= 7800 )
    Aylık[1] = st.number_input(label= "Şubat Aylık Ücret", step=100, value= Aylık[0] )
    Aylık[2] = st.number_input(label= "Mart Aylık Ücret", step=100, value= Aylık[1] )
    Aylık[3] = st.number_input(label= "Nisan Aylık Ücret", step=100, value= Aylık[2] )
    Aylık[4] = st.number_input(label= "Mayıs Aylık Ücret", step=100, value= Aylık[3] )
    Aylık[5] = st.number_input(label= "Haziran Aylık Ücret", step=100 , value= Aylık[4])
    Aylık[6] = st.number_input(label= "Temmuz Aylık Ücret", step=100, value= Aylık[5] )
    Aylık[7] = st.number_input(label= "Ağustos Aylık Ücret", step=100, value= Aylık[6] ) 
    Aylık[8] = st.number_input(label= "Eylül Aylık Ücret", step=100 , value= Aylık[7])
    Aylık[9]= st.number_input(label= "Ekim Aylık Ücret", step=100 , value= Aylık[8])
    Aylık[10] = st.number_input(label= "Kasım Aylık Ücret", step=100, value= Aylık[9] )
    Aylık[11] = st.number_input(label= "Aralık Aylık Ücret", step=100, value= Aylık[10] )    
with c2: # streamlit uygulama kodları
    Sabit[0] = st.number_input(label= "Diğer Sabit Ücretler", step=100, value= 0 )
    Sabit[1] = st.number_input(label= "Diğer Sabit Ücretler", step=100, value= Sabit[0], key="ş" )
    Sabit[2] = st.number_input(label= "Diğer Sabit Ücretler", step=100, value= Sabit[1],key="m" )
    Sabit[3] = st.number_input(label= "Diğer Sabit Ücretler", step=100, value= Sabit[2],key="n" )    
    Sabit[4] = st.number_input(label= "Diğer Sabit Ücretler", step=100, value= Sabit[3] ,key="mart")
    Sabit[5] = st.number_input(label= "Diğer Sabit Ücretler", step=100 , value= Sabit[4],key="h")
    Sabit[6] = st.number_input(label= "Diğer Sabit Ücretler", step=100, value= Sabit[5],key="t" )
    Sabit[7] = st.number_input(label= "Diğer Sabit Ücretler", step=100, value= Sabit[6],key="a" )
    Sabit[8] = st.number_input(label= "Diğer Sabit Ücretler", step=100 , value= Sabit[7],key="e")
    Sabit[9]= st.number_input(label= "Diğer Sabit Ücretler", step=100 , value= Sabit[8],key="k")
    Sabit[10] = st.number_input(label= "Diğer Sabit Ücretler", step=100, value= Sabit[9] ,key="s")
    Sabit[11] = st.number_input(label= "Diğer Sabit Ücretler", step=100, value= Sabit[10] ,key="r")
with c3: # streamlit uygulama kodları
    ilave[0] = st.number_input(label= "İlave Ödenek", step=100, value= 0 ,key="şs")
    ilave[1] = st.number_input(label= "İlave Ödenek", step=100, value= 0,key="marts" )
    ilave[2] = st.number_input(label= "İlave Ödenek", step=100, value= 0 ,key="nis")
    ilave[3] = st.number_input(label= "İlave Ödenek", step=100, value= 0 ,key="may")    
    ilave[4] = st.number_input(label= "İlave Ödenek", step=100, value= 0 ,key="haz")
    ilave[5] = st.number_input(label= "İlave Ödenek", step=100 , value= 0,key="tem")
    ilave[6] = st.number_input(label= "İlave Ödenek", step=100, value= 0 ,key="agu")
    ilave[7] = st.number_input(label= "İlave Ödenek", step=100, value= 0,key="eyl" )
    ilave[8] = st.number_input(label= "İlave Ödenek", step=100 , value= 0,key="ekm")
    ilave[9]= st.number_input(label= "İlave Ödenek", step=100 , value= 0,key="ksm")
    ilave[10] = st.number_input(label= "İlave Ödenek", step=100, value= 0 ,key="ara")
    ilave[11] = st.number_input(label= "İlave Ödenek", step=100, value= 0,key="sd")

for i in range(12): # i = ilgili ay, 12 ay için döngü
    Toplam[i] = Aylık[i] + Sabit[i] + ilave [i]
    if (Aylık[i] + Sabit[i]) >= tavan[i]:
        sskm[i]= tavan[i]
        
    elif Toplam[i] <= tavan[i]:
        sskm[i] = min(Toplam[i] + devreden1[i] + devreden2[i], tavan[i])
        kalan = tavan[i]- Toplam[i]
        kalan1 = max(kalan-devreden1[i],0)
        kullan1[i] = min(kalan,devreden1[i])
        kullan2[i] = min(kalan1,devreden2[i])
        if devreden1[i+1] != 0:
            devreden1[i+1] = devreden1[i+1] - kullan1[i]
        if devreden2[i+1] != 0:
            devreden2[i+1] = devreden2[i+1] - kullan2[i]
                        
        
        
    elif Toplam[i] > tavan[i]:
        sskm[i] = tavan[i]
        if devreden1[i+1] == 0:
            devreden1[i+1]= Toplam[i]-tavan[i]
            devreden1[i+2]= Toplam[i]-tavan[i]
        else:
            devreden2[i+1]= Toplam[i]-tavan[i]
            devreden2[i+2]= Toplam[i]-tavan[i]  


    sske[i] = round(sskm[i]*0.14,2)
    sski[i] = round(sskm[i]*0.01,2)
    dv[i] = round(Toplam[i]*0.00759,2)
    vm[i] = round(Toplam[i]-sske[i]-sski[i])
    kvm[i+1] = round(kvm[i] + vm[i])
    gv[i] = round(vergi(kvm[i], vm[i]))
    munzam[i] = round((Aylık[i] + mt.ceil(Aylık[i]/3))*0.07,2)
    
    igv[i] = min(gv[i],igv[i])
    idv[i] = min(idv[i],dv[i])
    net[i] = round(Toplam[i]-(sske[i]+sski[i]+dv[i]+gv[i]) + igv[i] + idv[i]-munzam[i])
    ktoplam[i] = kullan1[i] + kullan2[i]
    dtoplam[i] = devreden1[i] + devreden2[i]
    


#sonuç sözlüğü toparlama tablosu
dic = {"Toplam Brüt Ücret": Toplam,"Emekli Sandığı Payı":sske,"Emekli Sandığı İşsizlik Payı":sski,"Devreden Toplam": dtoplam,"Devreden Kullanılan": ktoplam,"Gelir Vergisi":gv,"Damga Vergisi İstisnası":idv,"Vergi İstisnası": igv, "Munzam Çalışan Payı": munzam,"Net Tutar": net}

#sonuç tablosu
tablo = pd.DataFrame(dic, index=["Ocak","Şubat", "Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos",
                                 "Eylül","Ekim","Kasım","Aralık"])



ortalamat = tablo.mean() #ortalama ödenen satırı
toplamat = tablo.sum() #toplam ödenen satırı
tablo.loc["Toplam"] = toplamat
tablo.loc["Ortalama"]= ortalamat




tablo = tablo.applymap("{0:,.2f}₺".format) # format


st.table(tablo) #streamlit tablo gösterimi








    


