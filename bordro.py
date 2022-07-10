import streamlit as st
import pandas as pd
import numpy as np



Aylık = [0,1,2,3,4,5,6,7,8,9,10,11]
kvm = [0,1,2,3,4,5,6,7,8,9,10,11,12]
vm = [0,1,2,3,4,5,6,7,8,9,10,11]
sskm = [0,1,2,3,4,5,6,7,8,9,10,11]
sske = [0,1,2,3,4,5,6,7,8,9,10,11]
sski = [0,1,2,3,4,5,6,7,8,9,10,11]
dv = [0,1,2,3,4,5,6,7,8,9,10,11]
idv =  [37.98,37.98,37.98,37.98,37.98,37.98,49.12,49.12,49.12,49.12,49.12,49.12]

igv = [638.01,638.01,638.01,638.01,638.01,638.01,825.05,1051.11,1100.07,1100.07,1100.07,1100.07]
tavan = [5004*7.5,5004*7.5,5004*7.5,5004*7.5,5004*7.5,5004*7.5,6471*7.5,6471*7.5,6471*7.5,6471*7.5,6471*7.5,6471*7.5]

net = [0,1,2,3,4,5,6,7,8,9,10,11]
gv = [0,1,2,3,4,5,6,7,8,9,10,11]

def vergi(kum, matrah):
    v = [32000,70000,250000,880000]
    o = [0.15,0.2,0.27,0.35,0.4]
    t= kum + matrah
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
    
    
    
    

c1,c2,c3 = st.columns(3)

with c1:
    Aylık[0] = st.number_input(label= "Ocak", step=1, value= 7800 )
    Aylık[1] = st.number_input(label= "Şubat", step=1, value= Aylık[0] )
    Aylık[2] = st.number_input(label= "Mart", step=1, value= Aylık[1] )
    Aylık[3] = st.number_input(label= "Nisan", step=1, value= Aylık[2] )
with c2:
    Aylık[4] = st.number_input(label= "Mayıs", step=1, value= Aylık[3] )
    Aylık[5] = st.number_input(label= "Haziran", step=1 , value= Aylık[4])
    Aylık[6] = st.number_input(label= "Temmuz", step=1, value= Aylık[5] )
    Aylık[7] = st.number_input(label= "Ağustos", step=1, value= Aylık[6] )
with c3:
    Aylık[8] = st.number_input(label= "Eylül", step=1 , value= Aylık[7])
    Aylık[9]= st.number_input(label= "Ekim", step=1 , value= Aylık[8])
    Aylık[10] = st.number_input(label= "Kasım", step=1, value= Aylık[9] )
    Aylık[11] = st.number_input(label= "Aralık", step=1, value= Aylık[10] )

for i in range(12):

    sskm[i] = min(tavan[i], Aylık[i])
    sske[i] = round(sskm[i]*0.14,2)
    sski[i] = round(sskm[i]*0.01,2)
    dv[i] = round(Aylık[i]*0.00759,2)
    vm[i] = round(Aylık[i]-sske[i]-sski[i])
    kvm[i+1] = round(kvm[i] + vm[i])
    gv[i] = round(vergi(kvm[i], vm[i]))
    net[i] = round(Aylık[i]-(sske[i]+sski[i]+dv[i]+gv[i]) + igv[i] + idv[i])

dic = {"Aylık": Aylık,"Emekli Sandık":sske,"İşsizlik Payı":sski,"Gelir Vergi":gv,"Damga İstisna":idv,"vergi istisnası": igv,"Net Tutar": net}
  
tablo = pd.DataFrame(dic, index=["Ocak","Şubat", "Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos",
                                 "Eylül","Ekim","Kasım","Aralık"])

tablo = tablo.applymap("{0:,.2f}₺".format)
st.table(tablo)







    

