

import streamlit as st
import pandas as pd
import numpy as np
import math as mt



Aylık = [0]*12 #Aylık Ücret
Tazm_Top = [0]*12 # Aylık ücret dışındaki Tazminatlar toplamı
ilave = [0]*12 #Ay içinde ödenen değişken ücret- brüt
ikramiye =[0]*12 #İkramiye
ek_gorev = [0]*12 #Ek Görev
jest = [0]*12 #Jestiyon


kvm = [0,1,2,3,4,5,6,7,8,9,10,11,12] #kümulatif gelir matrahı
kvm_MS_B_Dahil = [0,1,2,3,4,5,6,7,8,9,10,11,12]
vm = [0]*12 # vergi matrahı
vm_MS_B_Dahil = [0]*12 
sskm = [0]*12 #Emekli sandığı matrahı
sske = [0]*12 #Emekli sandığı payı
sski = [0]*12 #İşsizlik çalışan payı
dv = [0]*12 #damga vergisi
idv =  [151.82]*12 # vergi istisnası
Toplam = [0]*12 #Toplam Brüt ücret
ms_C = [0]*12 # Munzam Sandik Çalışan payı 

ms_B=[0]*12 # Munzam Sandik Banka payı
ms_B_brüt=[0]*12 # Brütleştirilmiş MS Banka Payı
ms_B_dahil_toplam_brüt=[0]*12 
sskm_msB_dahil=[0]*12 # MS banka brüt tutarı dahil ssk matrahı

igv = [2550.32,2550.32,2550.32,2550.32,2550.32,2550.32,3001.06,3400.42,3400.42,3400.42,3400.42,3400.42] #Gelir vergisi istisnası
tavan = [20002.5 * 7.5 if i < 6 else 20002.5 * 7.5 for i in range(12)] #Emekli sandığı tavanı
devreden1 = [0,0,0,0,0,0,0,0,0,0,0,0,0] #birinci devreden matrah
devreden2 = [0,0,0,0,0,0,0,0,0,0,0,0,0] #ikinci devreden matrah
kullan1 = [0,0,0,0,0,0,0,0,0,0,0,0] # 1. devreden matrahtan kullanılan
kullan2 = [0,0,0,0,0,0,0,0,0,0,0,0] # 2. devreden matrahtan kullanılan
dtoplam = [0,0,0,0,0,0,0,0,0,0,0,0] #devreden toplam
ktoplam = [0,0,0,0,0,0,0,0,0,0,0,0] # devreden matrah kullanılan
mtrh_bosluk= [0]*12
dev_1_mtrh_bosluk= [0]*12
net = [0]*12 # net gelir
net_ms = [0]*12 
gv = [0]*12 # gelir vergisi
gv_MS_B_Dahil = [0]*12 

def ms_es_banka(toplam, tavan):
    if toplam < tavan:
        return toplam * 0.2275
    else:
        return tavan * 0.2275   

def ms_banka_payi(Aylık):
    return (Aylık + mt.ceil(Aylık[i]/3)) * 0.15

def vergi(kum, matrah): # Vergi hesaplama fonksiyonu, Kümulatif matrah ve aylık matrah

    v = [110000,230000,870000,3000000] # vergi dilimleri

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

 

def brut_vergi(kum,net):

    v = [110000,230000,870000,3000000] # vergi dilimleri

    o = [0.15,0.2,0.27,0.35,0.4] #vergi oranları

    damga = 0.00759

    v_brut_bosluk = [0,0,0,0]

    v_net_bosluk = [0,0,0,0]

    vergi_brutu = 0

    for i in range(len(v)):

        if i == 0:      

            v_brut_bosluk[i] = max(v[i]-kum,0)           

        else:

            v_brut_bosluk[i] = max (v[i]-kum-v_brut_bosluk[i-1],0)

    for i in  range(len(v)):

        v_net_bosluk[i] =  v_brut_bosluk[i]*(1-o[i]-damga)

    if net - v_net_bosluk[0] <= 0:

        vergi_brutu = net/(1-o[0]-damga)

    elif net - sum(v_net_bosluk[:2]) <= 0:

        vergi_brutu = v_brut_bosluk[0]+ (net-v_net_bosluk[0])/(1-o[1]-damga)

    elif net - sum(v_net_bosluk[:3]) <= 0:

        vergi_brutu = sum(v_brut_bosluk[:2])+ (net-sum(v_net_bosluk[:2]))/(1-o[2]-damga)

    elif net - sum(v_net_bosluk[:4]) <= 0:

        vergi_brutu = sum(v_brut_bosluk[:3])+ (net-sum(v_net_bosluk[:3]))/(1-o[3]-damga)

    else:

         vergi_brutu = sum(v_brut_bosluk[:4])+ (net-sum(v_net_bosluk[:4]))/(1-o[4]-damga)      

    return vergi_brutu

 

 

def brut_vergi_sgk(kum,net):

    v = [110000,230000,870000,3000000] # vergi dilimleri

    o = [0.15,0.2,0.27,0.35,0.4] #vergi oranları

    damga = 0.00759

    v_brut_bosluk = [0,0,0,0]

    v_net_bosluk = [0,0,0,0]

    vergi_brutu = 0

    for i in range(len(v)):

        if i == 0:      

            v_brut_bosluk[i] = max(v[i]-kum,0)/0.85         

        else:

            v_brut_bosluk[i] = max (v[i]-kum-v_brut_bosluk[i-1],0)/0.85

    for i in  range(len(v)):

        v_net_bosluk[i] =  v_brut_bosluk[i]*((0.85)*(1-o[i])-damga)

    if net - v_net_bosluk[0] <= 0:

        vergi_brutu = net/((1-o[0])*0.85-damga)

    elif net - sum(v_net_bosluk[:2]) <= 0:

        vergi_brutu = v_brut_bosluk[0]+ (net-v_net_bosluk[0])/((1-o[1])*0.85-damga)

    elif net - sum(v_net_bosluk[:3]) <= 0:

        vergi_brutu = sum(v_brut_bosluk[:2])+ (net-sum(v_net_bosluk[:2]))/((1-o[2])*0.85-damga)

    elif net - sum(v_net_bosluk[:4]) <= 0:

        vergi_brutu = sum(v_brut_bosluk[:3])+ (net-sum(v_net_bosluk[:3]))/((1-o[3])*0.85-damga)

    else:

         vergi_brutu = sum(v_brut_bosluk[:4])+ (net-sum(v_net_bosluk[:4]))/((1-o[4])*0.85-damga)      

    return vergi_brutu

 

def netten_brute(i,gv_matrah,es_matrah,net):
 
    damga = 0.00759

    es_kalan_brut = tavan[i]-es_matrah

    es_kalan_net = es_kalan_brut-vergi(gv_matrah,es_kalan_brut * 0.85 ) - es_kalan_brut * damga -  es_kalan_brut*0.15

    if es_kalan_net >= net:

        brut = brut_vergi_sgk(gv_matrah, net)

    else:

        es_artan_net = net-es_kalan_net

        gv_matrah2 = es_kalan_brut*0.85 + gv_matrah  

        brut =  brut_vergi(gv_matrah2, es_artan_net) + es_kalan_brut

    return brut





# Kullanıcı Girdileri için Ay Bazında Grup Kutuları
aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

for i, ay in enumerate(aylar):
    with st.expander(f"{ay}"):

        # Kullanıcı girişleri
        Aylık[i] = st.number_input(f"{ay} Ayı Aylık Ücret (Brüt TL)", step=1000, value=33000 if i == 0 else Aylık[i - 1], key=f"Aylik_{i}")
        ikramiye[i] = round(Aylık[i] / 3, 2)
        st.write(f"{ay} Ayı İkramiye Tutarınız (Brüt TL): {ikramiye[i]}₺")
        Tazm_Top[i] = st.number_input(f"{ay} Ayı Tazminat Toplamınız (Brüt TL)", step=1000, value=Tazm_Top[i - 1] if i > 0 else 0, key=f"Tazm_Top_{i}")
        ilave[i] = st.number_input(f"{ay} Ayı Prim/Temettü Toplamınız (Brüt TL)", step=1000, value=0 )
        ek_gorev[i] = st.number_input(f"{ay} Ek Görev Tutarınız (Net TL)", step=1000, value=ek_gorev[i - 1] if i > 0 else 0, key=f"ek_gorev_{i}")
        jest[i] = st.number_input(f"{ay} Jestiyon Tutarınız (Net TL)", step=1000, value=0 )


for i in range(12): # i = ilgili ay, 12 ay için döngü
    Toplam[i] = Aylık[i] +ikramiye[i]+ Tazm_Top[i] + ilave[i]
    if (Aylık[i] + mt.ceil(Aylık[i]/3) + Tazm_Top[i]) >= tavan[i]:
        sskm[i]= tavan[i]

    elif Toplam[i] <= tavan[i]:
        sskm[i] = min(Toplam[i] + devreden1[i] + devreden2[i], tavan[i])
        
        mtrh_bosluk[i] = tavan[i]- Toplam[i] # İlk matrah boşluğu
        dev_1_mtrh_bosluk[i] = max(mtrh_bosluk[i]-devreden1[i],0) 
        kullan1[i] = min(mtrh_bosluk[i],devreden1[i])
        kullan2[i] = min(dev_1_mtrh_bosluk[i],devreden2[i])
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
    ms_C[i] = round((Aylık[i] + mt.ceil(Aylık[i]/3))*0.07,2)
    ms_B[i] = round((Aylık[i] + mt.ceil(Aylık[i]/3))*0.15,2)

    igv[i] = min(gv[i],igv[i])
    idv[i] = min(idv[i],dv[i])
    net[i] = round(Toplam[i]-(sske[i]+sski[i]+dv[i]+gv[i]) + igv[i] + idv[i]-ms_C[i])
    ktoplam[i] = kullan1[i] + kullan2[i]
    dtoplam[i] = devreden1[i] + devreden2[i]

    ms_B_brüt[i]=netten_brute(i,kvm[i],sskm[i],ms_B[i]) # MS Banka Payı netten brüte çevirme
    ms_B_dahil_toplam_brüt[i]= Toplam[i] + ms_B_brüt[i] # Brüt ücretler + Brüt MS Banka Payı

    if (Aylık[i] + mt.ceil(Aylık[i]/3) + Tazm_Top[i]) >= tavan[i]:
        sskm_msB_dahil[i]= tavan[i]

    elif ms_B_dahil_toplam_brüt[i] <= tavan[i]:
        sskm_msB_dahil[i] = min(ms_B_dahil_toplam_brüt[i] + devreden1[i] + devreden2[i], tavan[i])
        mtrh_bosluk[i] = tavan[i]- ms_B_dahil_toplam_brüt[i]
        dev_1_mtrh_bosluk[i] = max(mtrh_bosluk[i]-devreden1[i],0)
        kullan1[i] = min(mtrh_bosluk[i],devreden1[i])
        kullan2[i] = min(dev_1_mtrh_bosluk[i],devreden2[i])
        if devreden1[i+1] != 0:
            devreden1[i+1] = devreden1[i+1] - kullan1[i]
        if devreden2[i+1] != 0:
            devreden2[i+1] = devreden2[i+1] - kullan2[i]

    elif ms_B_dahil_toplam_brüt[i] > tavan[i]:
        sskm_msB_dahil[i] = tavan[i]
        if devreden1[i+1] == 0:
            devreden1[i+1]= ms_B_dahil_toplam_brüt[i]-tavan[i]
            devreden1[i+2]= ms_B_dahil_toplam_brüt[i]-tavan[i]
        else:
            devreden2[i+1]= ms_B_dahil_toplam_brüt[i]-tavan[i]
            devreden2[i+2]= ms_B_dahil_toplam_brüt[i]-tavan[i]
    
    sske[i] = round(sskm_msB_dahil[i]*0.14,2)
    sski[i] = round(sskm_msB_dahil[i]*0.01,2)
    dv[i] = round(ms_B_dahil_toplam_brüt[i]*0.00759,2)
    vm_MS_B_Dahil[i] = round(ms_B_dahil_toplam_brüt[i]-sske[i]-sski[i])
    kvm_MS_B_Dahil[i+1] = round(kvm_MS_B_Dahil[i] + vm_MS_B_Dahil[i])
    gv_MS_B_Dahil[i] = round(vergi(kvm_MS_B_Dahil[i], vm_MS_B_Dahil[i]))

    igv[i] = min(gv[i],igv[i])
    idv[i] = min(idv[i],dv[i])
    net_ms[i] = round(ms_B_dahil_toplam_brüt[i]-(sske[i]+sski[i]+dv[i]+gv_MS_B_Dahil[i]) + igv[i] + idv[i]-ms_C[i])
    ktoplam[i] = kullan1[i] + kullan2[i]
    dtoplam[i] = devreden1[i] + devreden2[i]





    


#sonuç sözlüğü toparlama tablosu
dic = {"Toplam Brüt Ücret": Toplam,"Emekli Sandığı Payı":sske,"Emekli Sandığı İşsizlik Payı":sski,"Devreden Toplam": dtoplam,"Devreden Kullanılan": ktoplam,"Gelir Vergisi":gv,"Damga Vergisi İstisnası":idv,"Vergi İstisnası": igv, "Munzam Çalışan Payı": ms_C,"Net Tutar": net}
dic_ms = {"Toplam Brüt Ücret": ms_B_dahil_toplam_brüt,"Emekli Sandığı Payı":sske,"Emekli Sandığı İşsizlik Payı":sski,"Devreden Toplam": dtoplam,"Devreden Kullanılan": ktoplam,"Gelir Vergisi":gv_MS_B_Dahil,"Damga Vergisi İstisnası":idv,"Vergi İstisnası": igv, "Munzam Çalışan Payı": ms_C,"Net Tutar": net_ms,"ms b brüt": ms_B_brüt}

row_labels = [
    "Tavan",
    "ms'siz brüt toplam",
    "ms'li brüt",
    "matrah bosluğu",
    "devreden1",
    "devreden2",
    "1. devreden matrahtan kullanılan",
    "2. devreden matrahtan kullanılan",
    "devreden matrahtan kullanılan",
    "devreden matrah kullanılan",
]

dic_mt = {aylar[i]: [tavan[i], Toplam[i], ms_B_dahil_toplam_brüt[i], mtrh_bosluk[i], devreden1[i], devreden2[i], kullan1[i], kullan2[i], dtoplam[i], ktoplam[i]] for i in range(12)}



#sonuç tablosu
tablo = pd.DataFrame(dic, index=["Ocak","Şubat", "Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos",
                                 "Eylül","Ekim","Kasım","Aralık"])

tablo_ms = pd.DataFrame(dic_ms, index=["Ocak","Şubat", "Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos",
                                 "Eylül","Ekim","Kasım","Aralık"])

tablo_mt = pd.DataFrame(dic_mt, index=row_labels)



ortalamat = tablo.mean() #ortalama ödenen satırı
toplamat = tablo.sum() #toplam ödenen satırı
tablo.loc["Toplam"] = toplamat
tablo.loc["Ortalama"]= ortalamat

ortalamat_ms = tablo_ms.mean() #ortalama ödenen satırı
toplamat_ms = tablo_ms.sum() #toplam ödenen satırı
tablo_ms.loc["Toplam"] = toplamat_ms
tablo_ms.loc["Ortalama"]= ortalamat_ms




tablo = tablo.applymap("{0:,.2f}₺".format) # format
tablo_ms = tablo_ms.applymap("{0:,.2f}₺".format) # format
tablo_mt = tablo_mt.applymap("{0:,.2f}₺".format) # format

#streamlit tablo gösterimi
st.table(tablo) 
st.table(tablo_ms)

st.table(tablo_mt)
