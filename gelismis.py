import streamlit as st

import pandas as pd

import numpy as np

import math as mt

 

Aylık = [0]*12 #Aylık Ücret

Tazm_Top = [0]*12 # Aylık ücret dışındaki Tazminatlar toplamı

ilave = [0]*12 #Ay içinde ödenen değişken ücret- brüt

ikramiye =[0]*12 #İkramiye

ek_gorev = [0]*12 #Ek Görev
ek_gorev_brut = [0]*12 # Ek Görev brüt

jest = [0]*12 #Jestiyon
jest_brut = [0]*12 #Jestiyon brüt 
 
ms_B=[0]*12 # Munzam Sandik Banka payı
ms_B_brüt=[0]*12 # Brütleştirilmiş MS Banka Payı

kvm = [0,1,2,3,4,5,6,7,8,9,10,11,12] #kümulatif gelir matrahı

vm = [0]*12 # vergi matrahı

vm_MS_B_Dahil = [0]*12

sskm = [0]*12 #Emekli sandığı matrahı

sske = [0]*12 #Emekli sandığı payı

sski = [0]*12 #İşsizlik çalışan payı

dv = [0]*12 #damga vergisi

idv =  [151.82]*12 # vergi istisnası



ms_C = [0]*12 # Munzam Sandik Çalışan payı

toplam_sabit= [0]*12 # Toplam sabit ücretler (aylık + ikr + tazm)
Toplam_brut= [0]*12 # Toplam sabit ücretler (brütler) 
Toplam_Brut_Ekgorev = [0]*12 # Toplam sabit ücretler (brütler + ek görev) - devreden matrahına girmeyenler
Toplam_Ms_Dahil=[0]*12
Toplam = [0]*12 #Toplam Brüt ücret/Jestiyon dahil (Sabit+ Değişken)/Tüm ücretler

 


 

igv = [2550.32,2550.32,2550.32,2550.32,2550.32,2550.32,3001.06,3400.42,3400.42,3400.42,3400.42,3400.42] #Gelir vergisi istisnası

tavan = [20002.5 * 7.5 if i < 6 else 20002.5 * 7.5 for i in range(12)] #Emekli sandığı tavanı

devreden1 = [0,0,0,0,0,0,0,0,0,0,0,0,0] #birinci devreden matrah

devreden2 = [0,0,0,0,0,0,0,0,0,0,0,0,0] #ikinci devreden matrah

devreden1_kullanılan = [0,0,0,0,0,0,0,0,0,0,0,0] # 1. devreden matrahtan kullanılan

devreden2_kullanılan = [0,0,0,0,0,0,0,0,0,0,0,0] # 2. devreden matrahtan kullanılan

dtoplam = [0] *12  #devreden toplam

ktoplam = [0]*12 # devreden matrah kullanılan

mtrh_bosluk= [0]*12

dev_1_mtrh_bosluk= [0]*12

net = [0]*12 # net gelir
net_msli = [0] * 12 
net_mscli = [0] * 12


gv = [0]*12 # gelir vergisi

gv_MS_B_Dahil = [0]*12

 

def ms_es_banka(toplam, tavan):

    if toplam < tavan:

        return toplam * 0.2275

    else:

        return tavan * 0.2275  

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

def netten_brute(i,gv_matrah,es_matrah,net, Banka_Pay = None):
    
    if Banka_Pay == None:
      net = max(0,net-(idv[i]+igv[i]))

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

 
st.sidebar.header("Kullanıcı Girdileri")

for i, ay in enumerate(aylar):
  
    # Kullanıcı girişleri
    with st.sidebar.expander(f"{ay}"):
        Aylık[i] = st.number_input(f"{ay} Ayı Aylık Ücret (Brüt TL)", step=1000, value=33000 if i == 0 else Aylık[i - 1], key=f"Aylik_{i}")

        ikramiye[i] = mt.ceil(Aylık[i] / 3)
        ms_C[i] = round((Aylık[i] + mt.ceil(Aylık[i]/3))*0.07,2)
        ms_B[i] = round((Aylık[i] + mt.ceil(Aylık[i]/3))*0.15,2)
        st.write(f"İkramiye Tutarı: {format(ikramiye[i], ',').replace(',', '.')} TL")

        Tazm_Top[i] = st.number_input(f"{ay} Ayı Tazminat Toplamınız (Brüt TL)", step=1000, value=Tazm_Top[i - 1] if i > 0 else 0, key=f"Tazm_Top_{i}")

        ilave[i] = st.number_input(f"{ay} Ayı Prim/Temettü Toplamınız (Brüt TL)", step=1000, value=0)

        ek_gorev[i] = st.number_input(f"{ay} Ek Görev Tutarınız (Net TL)", step=1000, value=ek_gorev[i - 1] if i > 0 else 0, key=f"ek_gorev_{i}")

        jest[i] = st.number_input(f"{ay} Jestiyon Tutarınız (Net TL)", step=1000, value=0 )

 

def ucret_sonrasi_yeni_sgkm_ve_kum_gv(sgk_onceki_matrah,onceki_gelir_vergi_matrahi,ucret,asgari_tavan): #önceki ay demek değil, hesaplama önceliği
    sgk_matrah = min(asgari_tavan,ucret)
    matrah_bosluk= min(ucret, max(0,asgari_tavan - sgk_onceki_matrah))
    yeni_sgk_matrah = sgk_onceki_matrah + matrah_bosluk 
    esis_kesinti = matrah_bosluk * 0.15

    gelir_vergi_matrahi = ucret-esis_kesinti
    kum_gelir_vergi_matrahi = gelir_vergi_matrahi + onceki_gelir_vergi_matrahi 
    return yeni_sgk_matrah,kum_gelir_vergi_matrahi
    


for i in range(12): # i = ilgili ay, 12 ay için döngü
    
    Toplam_brut[i] = Aylık[i] +ikramiye[i] + Tazm_Top[i] + ilave[i] #toplam brüt ücretler
    sskm[i], kvm[i] = ucret_sonrasi_yeni_sgkm_ve_kum_gv(sskm[i],kvm[i],Toplam_brut[i],tavan[i]) # Brüt ücretler sonrası matrahlar

    ek_gorev_brut[i]= netten_brute(i,kvm[i],sskm[i],ek_gorev[i])
    Toplam_Brut_Ekgorev[i]= Toplam_brut[i] +  ek_gorev_brut[i] # topmlam brütlere ek görev'in brütünü ekleme
    sskm[i], kvm[i] = ucret_sonrasi_yeni_sgkm_ve_kum_gv(sskm[i],kvm[i],ek_gorev_brut[i],tavan[i]) #Ek görev sonrası matrahlar

    jest_brut[i]=netten_brute(i,kvm[i],sskm[i],jest[i])
    Toplam[i] = round(Toplam_Brut_Ekgorev[i] + jest_brut[i],2) # jest brüt tutarını ek görevli brütlere ekleme
    sskm[i], kvm[i] = ucret_sonrasi_yeni_sgkm_ve_kum_gv(sskm[i],kvm[i],jest_brut[i],tavan[i]) #Jestiyon sonrası matrahlar

    ms_B_brüt[i]= netten_brute(i,kvm[i],sskm[i],ms_B[i], Banka_Pay = 1)
    Toplam_Ms_Dahil[i]= round(Toplam[i] + ms_B_brüt[i],2)  # toplam tutarlara ms banka brüt ekleme
    sskm[i], kvm[i] = ucret_sonrasi_yeni_sgkm_ve_kum_gv(sskm[i],kvm[i],ms_B_brüt[i],tavan[i]) #Munzam sandık brüt sonrası matrahlar 
    
    if (Aylık[i] +ikramiye[i] + Tazm_Top[i] + ms_B_brüt[i] + ek_gorev_brut[i]) >= tavan[i]:
        sskm[i]=tavan[i]
    elif Toplam_Ms_Dahil[i]==0:
        sskm[i]=0
    elif sskm[i] < tavan[i]:
        sskm_bosluk= tavan[i] - sskm[i]
        
        devreden2_kullanılan[i] = min(sskm_bosluk,devreden2[i])
        sskm_bosluk= sskm_bosluk - devreden2_kullanılan[i]
        

        devreden1_kullanılan[i] = min(sskm_bosluk,devreden1[i])
        sskm_bosluk = sskm_bosluk - devreden1_kullanılan[i] 
        devreden2[i] = max(0,devreden2[i])
        devreden2[i+1] = devreden2[i+1] - devreden1_kullanılan[i]

        sskm[i] = sskm[i] + devreden1_kullanılan[i] + devreden2_kullanılan[i]
    elif Toplam_Ms_Dahil[i] > tavan[i]:
        sskm[i]=tavan[i] 
        devreden1[i+1] = Toplam[i] - tavan[i] 
        devreden2[i+2] = Toplam[i] - tavan[i] 
    
    
    sske[i] = min(Toplam_Ms_Dahil[i],round(sskm[i]*0.14,2))
    sski[i] = min(Toplam_Ms_Dahil[i],round(sskm[i]*0.01,2))
    dv[i] = round(Toplam_Ms_Dahil[i]*0.00759,2)
    vm[i] = round(Toplam_Ms_Dahil[i]-sske[i]-sski[i],2)
    kvm[i+1] = round(kvm[i],2)
    gv[i] = max(0,round(vergi(kvm[i-1], vm[i]),2))

    igv[i] = min(gv[i],igv[i])
    idv[i] = min(idv[i],dv[i])
    net[i] = max(0,round((Toplam_Ms_Dahil[i]-(sske[i]+sski[i]+dv[i]+gv[i]) + igv[i] + idv[i]-ms_C[i]-ms_B[i]),2))

    net_msli[i]= round((Toplam_Ms_Dahil[i]-(sske[i]+sski[i]+dv[i]+gv[i]) + igv[i] + idv[i]-ms_C[i]),2)
    net_mscli[i] = round((Toplam_Ms_Dahil[i]-(sske[i]+sski[i]+dv[i]+gv[i]) + igv[i] + idv[i]),2)
    ktoplam[i] = devreden1_kullanılan[i] + devreden2_kullanılan[i]
    dtoplam[i] = devreden1[i] + devreden2[i]

# ---- Ay Tabloları Gösterim --- --------------------------------------------------


# Renk teması ayarları
background_colors = ["#fce4ec", "#e3f2fd", "#f8bbd0"]  # Pembe-mavi tonları
text_color = "black"

# Açılır kapanır grup kutusu
with st.expander("Aylık Ücretler Detayları", expanded=True):
    cols = st.columns(4)  # Her satırda 4 sütun
    for i, ay in enumerate(aylar):
        col = cols[i % 4]  # 4 sütun içinde sırasıyla yerleşim
        with col:
            # Her ay için kutucuk
            st.markdown(
                f"""
                <div style="
                    border: 1px solid #d1c4e9;
                    border-radius: 8px;
                    padding: 16px;
                    background-color: {background_colors[i % len(background_colors)]};
                    text-align: left;
                    margin: 8px;
                ">
                    <h3 style="text-align: center; color: {text_color};">{ay}</h3>
                    <p><strong>Toplam Ücret</strong> (Brüt TL)</p>
                    <p>{format(Toplam[i], ',').replace(',', '.')} TL</p>
                    <p><strong>Yaklaşık Net Ücret</strong></p>
                    <p>{format(net_mscli[i], ',').replace(',', '.')} TL</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        # Yeni satıra geçmek için sütunları sıfırla
        if (i + 1) % 4 == 0:
            cols = st.columns(4)  # Yeni satır için sütunlar
#------------------------------------------------------------------------------------------

#sonuç sözlüğü toparlama tablosu

dic = {"Toplam Brüt Ücret": Toplam,"Toplam MS'Lİ Brüt Ücret": Toplam_Ms_Dahil,"Emekli Sandığı Payı":sske,"Emekli Sandığı İşsizlik Payı":sski,"Devreden Toplam": dtoplam,"Devreden Kullanılan": ktoplam,"Gelir Vergisi":gv,"Damga Vergisi İstisnası":idv,"Vergi İstisnası": igv, 
       "Munzam Çalışan Payı": ms_C,"Net Tutar": net,"Net Tutar (Ms Calısan)": net_mscli,"Net Tutar MS bankalı": net_msli}

dic_vrb={"Toplam sabit brütler": Toplam_brut,"Ek görev brüt": ek_gorev_brut,"jestiyon brüt":jest_brut,"MS Brüt tutar": ms_B_brüt, "MS Net tutar": ms_B,
         "devreden1 kullanılan":devreden1_kullanılan,"devreden2 kullanılan":devreden2_kullanılan}

dic_13={"Küm GV": kvm,"Devreden1":devreden1,"Devreden2":devreden2}


#sonuç tablosu

tablo = pd.DataFrame(dic, index=["Ocak","Şubat", "Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos",

                                 "Eylül","Ekim","Kasım","Aralık"])

 

tablo_ms = pd.DataFrame(dic_vrb, index=["Ocak","Şubat", "Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos",

                                 "Eylül","Ekim","Kasım","Aralık"])

 

tablo_mt = pd.DataFrame(dic_13, index=[0,1,2,3,4,5,6,7,8,9,10,11,12])
 

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
