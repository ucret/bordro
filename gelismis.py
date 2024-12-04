import streamlit as st

import pandas as pd

import numpy as np

import math as mt

import random
 

Aylık = [0]*12 #Aylık Ücret
onceki_aylik=[0]*13
onceki_aylik[0] = 33000
Tazm_Top = [0]*12 # Aylık ücret dışındaki Tazminatlar toplamı
ilave = [0]*12 #Ay içinde ödenen değişken ücret- brüt
ikramiye =[0]*12 #İkramiye
send_aidat=[0]*12 #sendika aidatı 

yemek_net = [0]*12
yemek_gun_say = [0]*12
banka_yemek = [275 if i < 6 else 300 for i in range(12)]

ek_gorev = [0]*12 #Ek Görev
ek_gorev_brut = [0]*12 # Ek Görev brüt

jest = [0]*12 #Jestiyon
jest_brut = [0]*12 #Jestiyon brüt 

ms_B=[0]*12 # Munzam Sandik Banka payı
ms_B_brüt=[0]*12 # Brütleştirilmiş MS Banka Payı

kvm = [0]*14 #kümulatif gelir matrahı
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

ms_yukselme_C_net=[0]*12
ms_yukselme_B_net=[0]*12
ms_yukselme_C_brut=[0]*12
ms_yukselme_B_brut=[0]*12

 

igv = [2550.32,2550.32,2550.32,2550.32,2550.32,2550.32,3001.06,3400.42,3400.42,3400.42,3400.42,3400.42] #Gelir vergisi istisnası

tavan = [20002.5 * 7.5 if i < 6 else 20002.5 * 7.5 for i in range(12)] #Emekli sandığı tavanı

devreden1 = [0]*14 #birinci devreden matrah

devreden2 = [0]*14 #ikinci devreden matrah

devreden1_kullanılan = [0]*12 # 1. devreden matrahtan kullanılan

devreden2_kullanılan = [0]*12 # 2. devreden matrahtan kullanılan

dtoplam = [0] *12  #devreden toplam

ktoplam = [0]*12 # devreden matrah kullanılan

mtrh_bosluk= [0]*12

dev_1_mtrh_bosluk= [0]*12

matrah_artigi_1=[0]*14
matrah_artigi_2=[0]*14
devreden1c = [0]*14
devreden2c = [0]*14
devreden1b = [0]*14
devreden2b = [0]*14
devreden1c_kullanılan = [0]*14
devreden2c_kullanılan = [0]*14
devreden1b_kullanılan = [0]*14
devreden2b_kullanılan = [0]*14


net = [0]*12 # net gelir
net_msli = [0] * 12 
net_mscli = [0] * 12 # 


gv = [0]*12 # gelir vergisi

gv_MS_B_Dahil = [0]*12

yemek_ESIS_istisna=[105.75 if i < 6 else 157.69 for i in range(12)]
yemek_GV_istisna=[170]*12
 

def vergi(kum, matrah):  # Vergi hesaplama fonksiyonu (doğru çalışan versiyon)
    v = [110000, 230000, 870000, 3000000]  # Vergi dilimleri
    o = [0.15, 0.2, 0.27, 0.35, 0.4]  # Vergi oranları
    kalan_matrah = matrah  # Kalan matrah miktarı
    toplam_vergi = 0  # Toplam vergi
    
    # İlk dilimden başla ve sırasıyla diğer dilimlere geç
    for i in range(len(v)):
        # Bulunduğumuz dilimde ne kadar matrah kullanabiliriz?
        dilim_matrah = max(0, min(kalan_matrah, v[i] - kum))
        # Bu dilim için ödenecek vergiyi hesapla
        toplam_vergi += dilim_matrah * o[i]
        # Kalan matrahtan bu dilimdekini düş
        kalan_matrah -= dilim_matrah
        # Kümülatif matrahı güncelle
        kum += dilim_matrah
        # Eğer kalan matrah sıfırlandıysa döngüyü sonlandır
        if kalan_matrah <= 0:
            break
    
    # Eğer matrah en üst dilimlere giriyorsa, kalan matrah için oranı uygula
    if kalan_matrah > 0:
        toplam_vergi += kalan_matrah * o[-1]
    
    return toplam_vergi

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

def netten_brute(i,gv_matrah,es_matrah,net, indirim = None):
    
    if indirim == 1:
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

def netten_brute_yemek(i,gv_matrah,es_matrah,net, indirim = None):
    
    if indirim == 1:
      net = max(0,net-(idv[i]+igv[i]))
    damga = 0.00759
    es_kalan_brut = tavan[i]-es_matrah
    es_kalan_net = es_kalan_brut-vergi(gv_matrah,es_kalan_brut * 0.85 ) - es_kalan_brut * damga -  es_kalan_brut*0.15
    
    if es_kalan_net >= net-yemek_ESIS_istisna[i]:
        brut = brut_vergi_sgk(gv_matrah, net - yemek_GV_istisna[i]) 
    else:
        es_artan_net = (net-yemek_GV_istisna[i])-es_kalan_net
        gv_matrah2 = es_kalan_brut*0.85 + gv_matrah 
        brut =  brut_vergi(gv_matrah2, es_artan_net) + es_kalan_brut
    return brut

def sandik_isleri(i,aylik_once,aylik): # MS Yükselme payları hesaplama 
    if aylik_once==0:
        ms_C[i] = round((aylik + mt.ceil(aylik/3))*0.07,2) 
        ms_B[i] = round((aylik + mt.ceil(aylik/3))*0.15,2)
    elif aylik <=aylik_once:
        ms_C[i] = round((aylik + mt.ceil(aylik/3))*0.07,2) 
        ms_B[i] = round((aylik + mt.ceil(aylik/3))*0.15,2)
    else:
        ms_C[i]= (aylik_once + mt.ceil(aylik/3))*0.07
        ms_yukselme_C_net[i]= aylik - aylik_once
        ms_B[i]= (aylik_once + mt.ceil(aylik/3))*0.15
        ms_yukselme_B_net[i] = (aylik - aylik_once)*3

def yemekhane(i,gv_matrah,es_matrah,net, yemek_gun): 

    damga = 0.00759
    es_kalan_brut = max(tavan[i]-es_matrah,0)
    vergisiz_kalan = es_kalan_brut * 0.85
    vergisiz_sgklı = (yemek_GV_istisna[i] - yemek_ESIS_istisna[i]) * yemek_gun
    tavanı_asan_net = max(vergisiz_sgklı - vergisiz_kalan,0)
    sgk_vergisiz_kullanılan = min(vergisiz_sgklı/0.85, es_kalan_brut)
    sgk_tutar = sgk_vergisiz_kullanılan * 0.15
    eklenecek_tutar = tavanı_asan_net + sgk_vergisiz_kullanılan
    
    es_kalan_brut -= sgk_vergisiz_kullanılan 
    
    es_kalan_net = es_kalan_brut-vergi(gv_matrah,es_kalan_brut * 0.85 ) - es_kalan_brut * damga -  es_kalan_brut*0.15
    net -= (yemek_GV_istisna[i]) * yemek_gun
    if es_kalan_net >= net:
        brut = brut_vergi_sgk(gv_matrah, net) + yemek_ESIS_istisna[i] * yemek_gun + eklenecek_tutar
    else:
        es_artan_net = net-es_kalan_net
        gv_matrah2 = es_kalan_brut*0.85 + gv_matrah 
        brut =  brut_vergi(gv_matrah2, es_artan_net) + es_kalan_brut + yemek_ESIS_istisna[i] * yemek_gun + eklenecek_tutar
    return brut

def ucret_sonrasi_yeni_sgkm_ve_kum_gv(sgk_onceki_matrah,onceki_gelir_vergi_matrahi,ucret,asgari_tavan,devreden_tipi=1): #önceki ay demek değil, hesaplama önceliği
    #devreden tipi (1,2,3) = 1 çalışan ödediği durum, 2 Banka ödediği durum, 3 devretmeyen durum
    sgk_matrah = min(asgari_tavan,ucret)
    matrah_artigi= max((sgk_onceki_matrah+ucret) - asgari_tavan,0)

    matrah_bosluk= min(ucret, max(0,asgari_tavan - sgk_onceki_matrah))
    yeni_sgk_matrah = sgk_onceki_matrah + matrah_bosluk 
    esis_kesinti = matrah_bosluk * 0.15

    gelir_vergi_matrahi = ucret-esis_kesinti
    kum_gelir_vergi_matrahi = gelir_vergi_matrahi + onceki_gelir_vergi_matrahi 
    
    if devreden_tipi==1:
        matrah_artigi_calisan=matrah_artigi
        matrah_artigi_banka=0
    elif devreden_tipi==2:
        matrah_artigi_banka=matrah_artigi
        matrah_artigi_calisan=0
    else:
        matrah_artigi_banka=0
        matrah_artigi_calisan=0
        
    return yeni_sgk_matrah,kum_gelir_vergi_matrahi,matrah_artigi_calisan,matrah_artigi_banka

def matrah_artigi_topla(i,a,b):
    matrah_artigi_1[i]+=a
    matrah_artigi_2[i]+=b
    return matrah_artigi_1[i],matrah_artigi_2[i]

def asgari_ucret_uyari(ucret):
    if ucret < 20002:
        return st.error(f"Uyarı: Toplam brüt tutarınız {ucret} TL. Bu tutar 20.002 TL'nin altında olmamalıdır.")


# Kullanıcı Girdileri için Ay Bazında Grup Kutuları

aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]


if 'info_shown_sidebar' not in st.session_state:
    st.session_state.info_shown_sidebar = False

with st.sidebar:
    if st.button("📣 Uygulama Hakkında"):
        st.session_state.info_shown_sidebar = not st.session_state.info_shown_sidebar
        

if st.session_state.info_shown_sidebar:
    st.info("💁 Net Gelir Hesaplama uygulaması ile yan taraftan giriş yapacağınız ücretlerinizin yıl içerisindeki brüt/net dağılımını aşağıdaki tablolarımız ile görebilirsiniz")
    st.info("Bilgilendirmeyi tamamladıysak Uygulama Hakkında butonuna tıklayarak kutuları kapatalıbirsiniz ",icon="✅")

st.sidebar.header("Ücret Girdi Alanları")

zamlı_aylik=0
with st.sidebar.expander("2024 Aralık"):
    onceki_aylik[0] = st.number_input("Maaş Tutarınız (Brüt TL):", step=1000,value=0
        ,help=":money_with_wings: Bu alan 2024 yılı Aralık maaşınız ve 2025 Ocak maaşınızın arasındaki yükselme farkı hesaplaması için oluşturulmuştur.") # i=0: Aralık Ayı indeksi

for i, ay in enumerate(aylar):
    with st.sidebar.expander(f"2025 {ay}"):
        # Sabit Ödemeleriniz kısmı
        with st.container():
            st.markdown("### **Sabit Ödemeleriniz**")
            Aylık[i] = st.number_input(f":money_with_wings: Maaş Tutarınız (Brüt TL)",step=1000,value=Aylık[i] if i == 0 else Aylık[i - 1], key=f"Aylik_{i}",
                help="Lütfen bordronuzdaki Maaş kalemini giriniz")
            
            ikramiye[i] = mt.ceil(Aylık[i] / 3)
            st.write(f":money_with_wings: İkramiye Tutarınız: {format(ikramiye[i], ',').replace(',', '.')} TL")
            
            Tazm_Top[i] = st.number_input(f":money_with_wings: Tazminat Toplamlarınız (Brüt TL)", step=1000, value=Tazm_Top[i - 1] if i > 0 else 0, key=f"Tazm_Top_{i}",
                help="Unvan, Yabancı Dil, Kambiyo, Mali Tahlil gibi tazminatlarınızın toplamını giriniz")
            

            ek_gorev[i] = st.number_input(f":money_with_wings: İlave Ödemeleriniz (Net TL)", step=1000, value=ek_gorev[i - 1] if i > 0 else 0, key=f"ek_gorev_{i}"
                ,help="Net bir ödeneğiniz varsa net tutar kadar giriniz")
            
            yemek_gun_say[i]= st.number_input(f"🍔 Yemek Gün Sayınızı Giriniz", step=1, value=yemek_gun_say[i - 1] if i > 0 else 0, key=f"yemek_gun_say{i}")
            yemek_net[i]=yemek_gun_say[i] * banka_yemek[i]
            
            send_aidat[i]=Aylık[i] * 0.015
            
            asgari_ucret_uyari(Aylık[i]+ikramiye[i]+Tazm_Top[i])
            
             

        # Değişken Ödemeleriniz kısmı
        st.markdown("### **Değişken Ödemeleriniz**")
        
        if i==3:
            ilave[i] = st.number_input(f":money_with_wings: İlave Ödemeleriniz (Brüt TL)", step=1000, value=0, key=f"ilave_{i}"
                ,help="Ay içerisinde almış olduğunuz ilave brüt ödeneklerinizin (Satış Primi, Pys Primi, Temettü) toplamını girebilirsiniz.")
            jest[i] = st.number_input(f"Jestiyon Tutarınız (Net TL)", step=1000, value=0, key=f"jest_{i}"
                ,help="Jestiyon tutarınızı NET TL olarak giriniz")
            
        else:
            ilave[i] = st.number_input(f":money_with_wings: İlave Ödemeleriniz (Brüt TL)", step=1000, value=0, key=f"ilave_{i}"
                ,help="Ay içerisinde almış olduğunuz ilave brüt ödeneklerinizin (Satış Primi, Pys Primi, Temettü) toplamını girebilirsiniz.")






yemek_brut=[0]*12

for i in range(12): # i = ilgili ay, 12 ay için döngü
    
    sandik_isleri(i,onceki_aylik[0] if i==0 else Aylık[i-1] ,Aylık[i])

    toplam_sabit[i] = Aylık[i] +ikramiye[i] + Tazm_Top[i] #toplam brüt ücretler
    sskm[i], kvm[i], matrah_artigi_a,matrah_artigi_b = ucret_sonrasi_yeni_sgkm_ve_kum_gv(sskm[i],kvm[i],toplam_sabit[i],tavan[i],3) # Brüt ücretler sonrası matrahlar
    matrah_artigi_1[i],matrah_artigi_2[i] = matrah_artigi_topla(i,matrah_artigi_a,matrah_artigi_b)
    
    Toplam_brut[i] = toplam_sabit[i] + ilave[i] #toplam brüt ücretler
    sskm[i], kvm[i], matrah_artigi_a,matrah_artigi_b = ucret_sonrasi_yeni_sgkm_ve_kum_gv(sskm[i],kvm[i],ilave[i],tavan[i],1) # Brüt ücretler sonrası matrahlar
    matrah_artigi_1[i],matrah_artigi_2[i] = matrah_artigi_topla(i,matrah_artigi_a,matrah_artigi_b)
    
    ind = None
    if Toplam_brut[i] ==0:
     ind = 1
 
    ek_gorev_brut[i]= netten_brute(i,kvm[i],sskm[i],ek_gorev[i], indirim = ind)
    Toplam_Brut_Ekgorev[i]= Toplam_brut[i] +  ek_gorev_brut[i] # topmlam brütlere ek görev'in brütünü ekleme
    sskm[i], kvm[i], matrah_artigi_a,matrah_artigi_b = ucret_sonrasi_yeni_sgkm_ve_kum_gv(sskm[i],kvm[i],ek_gorev_brut[i],tavan[i],2) #Ek görev sonrası matrahlar
    matrah_artigi_1[i],matrah_artigi_2[i] = matrah_artigi_topla(i,matrah_artigi_a,matrah_artigi_b)

    if ind == 1 and ek_gorev_brut[i]>0:
     ind = None
    
    #yemek kod"
    yemek_brut[i]=yemekhane(i,kvm[i],sskm[i],yemek_net[i],yemek_gun_say[i])
    
    Toplam_Brut_Ekgorev[i]= round(Toplam_Brut_Ekgorev[i] + yemek_brut[i],2)
    sskm[i], kvm[i], matrah_artigi_a,matrah_artigi_b = ucret_sonrasi_yeni_sgkm_ve_kum_gv(sskm[i],kvm[i],yemek_brut[i],tavan[i],3)
    matrah_artigi_1[i],matrah_artigi_2[i] = matrah_artigi_topla(i,matrah_artigi_a,matrah_artigi_b)
    #yemek kod"


    jest_brut[i]=netten_brute(i,kvm[i],sskm[i],jest[i], indirim = ind)
    Toplam[i] = round(Toplam_Brut_Ekgorev[i] + jest_brut[i],2) # jest brüt tutarını ek görevli brütlere ekleme
    sskm[i], kvm[i], matrah_artigi_a,matrah_artigi_b = ucret_sonrasi_yeni_sgkm_ve_kum_gv(sskm[i],kvm[i],jest_brut[i],tavan[i],2) #Jestiyon sonrası matrahlar
    matrah_artigi_1[i],matrah_artigi_2[i] = matrah_artigi_topla(i,matrah_artigi_a,matrah_artigi_b)
    
    ms_B_brüt[i]= netten_brute(i,kvm[i],sskm[i],ms_B[i])
    Toplam_Ms_Dahil[i]= round(Toplam[i] + ms_B_brüt[i],2)  # toplam tutarlara ms banka brüt ekleme
    sskm[i], kvm[i], matrah_artigi_a,matrah_artigi_b = ucret_sonrasi_yeni_sgkm_ve_kum_gv(sskm[i],kvm[i],ms_B_brüt[i],tavan[i],3) #Munzam sandık brüt sonrası matrahlar 
    matrah_artigi_1[i],matrah_artigi_2[i] = matrah_artigi_topla(i,matrah_artigi_a,matrah_artigi_b)

    ms_yukselme_B_brut[i]= netten_brute(i,kvm[i],sskm[i],ms_yukselme_B_net[i]) 
    Toplam_Ms_Dahil[i]= round(Toplam_Ms_Dahil[i] + ms_yukselme_B_brut[i],2)  # toplam tutarlara ms banka yükselme brüt ekleme
    sskm[i], kvm[i], matrah_artigi_a,matrah_artigi_b = ucret_sonrasi_yeni_sgkm_ve_kum_gv(sskm[i],kvm[i],ms_yukselme_B_brut[i],tavan[i],3) #Munzam sandık yükselme brüt sonrası matrahlar 
    matrah_artigi_1[i],matrah_artigi_2[i] = matrah_artigi_topla(i,matrah_artigi_a,matrah_artigi_b)

    sskm[i] = sskm[i] - (yemek_ESIS_istisna[i]*yemek_gun_say[i])
    
    


    # -- Devreden hesaplama ---- 
    
    if (Aylık[i] +ikramiye[i] + Tazm_Top[i] + ms_B_brüt[i]) >= tavan[i]:
        sskm[i]=tavan[i]
    elif Toplam_Ms_Dahil[i]==0:
        sskm[i]=0
    elif sskm[i] < tavan[i]:
        sskm_bosluk= tavan[i] - sskm[i]
        
        devreden2_kullanılan[i] = min(sskm_bosluk,devreden2[i])
        devreden2c_kullanılan[i] = min(devreden2_kullanılan[i],devreden2c[i]) #ilk çalışan tarafından kullanılan hesaplanır
        devreden2b_kullanılan[i] = max(0,devreden2_kullanılan[i] - devreden2c_kullanılan[i]) #banka tarafından ödenen kullanılan hesaplanır.
        sskm_bosluk= sskm_bosluk - devreden2_kullanılan[i]
     
        devreden1_kullanılan[i] = min(sskm_bosluk,devreden1[i]) 
        devreden1c_kullanılan[i] = min(devreden1_kullanılan[i],devreden1c[i]) #ilk çalışan tarafından kullanılan hesaplanır
        devreden1b_kullanılan[i] = max(0,devreden1_kullanılan[i] - devreden1c_kullanılan[i]) 
        sskm_bosluk = sskm_bosluk - devreden1_kullanılan[i]
     
        devreden2[i] = max(0,devreden2[i])
        devreden2[i+1] = devreden2[i+1] - devreden1_kullanılan[i]
        devreden2c[i+1] = devreden2c[i+1] - devreden1c_kullanılan[i]
        devreden2b[i+1] = devreden2b[i+1] - devreden1b_kullanılan[i]
     
        sskm[i] = sskm[i] + devreden1_kullanılan[i] + devreden2_kullanılan[i] - devreden1b_kullanılan[i] - devreden2b_kullanılan[i]

    elif Toplam_Ms_Dahil[i] > tavan[i]:
        sskm[i]=tavan[i] 
        devreden1[i+1] = matrah_artigi_1[i] + matrah_artigi_2[i]
        devreden2[i+2] = matrah_artigi_1[i] + matrah_artigi_2[i]
        devreden1c[i+1] = matrah_artigi_1[i]
        devreden2c[i+2] = matrah_artigi_1[i]
        devreden1b[i+1] = matrah_artigi_2[i]
        devreden2b[i+2] = matrah_artigi_2[i]
 
    sske[i] = min(Toplam_Ms_Dahil[i],round(sskm[i]*0.14,2))
    sski[i] = min(Toplam_Ms_Dahil[i],round(sskm[i]*0.01,2))
    dv[i] = round((Toplam_Ms_Dahil[i]-(yemek_gun_say[i]*yemek_GV_istisna[i]))*0.00759,2)
    vm[i] = round(Toplam_Ms_Dahil[i]-sske[i]-sski[i]-(yemek_gun_say[i]*yemek_GV_istisna[i])-send_aidat[i],2)
    kvm[i+1] = round(kvm[i],2)
    gv[i] = max(0,round(vergi(kvm[i-1], vm[i]),2))

    igv[i] = min(gv[i],igv[i])
    idv[i] = min(idv[i],dv[i])
    net[i] = max(0,round((Toplam_Ms_Dahil[i]-(sske[i]+sski[i]+dv[i]+gv[i]) + igv[i] + idv[i]-ms_C[i]-ms_B[i]-ms_yukselme_C_net[i]-ms_yukselme_B_net[i]-send_aidat[i]),2))

    net_msli[i]= round((Toplam_Ms_Dahil[i]-(sske[i]+sski[i]+dv[i]+gv[i]) + igv[i] + idv[i]-ms_C[i]),2)
    net_mscli[i] = round((Toplam_Ms_Dahil[i]-(sske[i]+sski[i]+dv[i]+gv[i]) + igv[i] + idv[i]),2)
    ktoplam[i] = devreden1_kullanılan[i] + devreden2_kullanılan[i]
    dtoplam[i] = devreden1[i] + devreden2[i]
    

kesinti_esis_toplam = sum(sske) + sum(sski)
kesinti_gvdv_toplam = sum(dv) + sum(gv) 
kesinti_toplam = kesinti_esis_toplam + kesinti_gvdv_toplam + sum(ms_C) + sum(ms_yukselme_C_net)


#sonuç sözlüğü toparlama tablosu

dic = {"Toplam Brüt Ücret": Toplam,"Yaklaşık Net Tutar": net,  
       "es matrah":sskm,
       "ES":sske,"IS":sski,
       
       "GV Mat":vm,
       "GV":gv,"DV":dv,
       
       "Devreden Toplam Matrah": dtoplam,"Devreden Matrahtan Kullanılan": ktoplam,
       
       "Munzam Sandık Çalışan Payı (%7)": ms_C,"Munzam Sandık Yükselme Payı": ms_yukselme_C_net,

       "Damga Vergisi İstisnası":idv,"Vergi İstisnası": igv, 
              
       "Yemek brut":yemek_brut,"yemek net":yemek_net
       }

dic_vrb={"MS Banka Brüt tutar": ms_B_brüt, "MS Banka Net tutar": ms_B,
         "ms yükselme C net": ms_yukselme_C_net,"ms yükselme B net":ms_yukselme_B_net,"ms yükselme B brüt":ms_yukselme_B_brut
         ,"sendika":send_aidat

         }

dic_13={"Küm GV": kvm,"Devreden1":devreden1,"Devreden2":devreden2, "çalışan_devreden_1": devreden1c, "çalışan_devreden_2": devreden2c,"Banka_dev_1": devreden1b, "banka dev 2": devreden2b,
       "artan_matra" : matrah_artigi_1, "artan_matrah": matrah_artigi_2}


#sonuç tablosu

tablo = pd.DataFrame(dic, index=["Ocak","Şubat", "Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos",

                                 "Eylül","Ekim","Kasım","Aralık"])

columns = pd.MultiIndex.from_tuples([   # Sözlük ve gösterim sıralaması önemli
    ("", "Ücretler Toplamı"),
    ("", "Yaklaşık Net Tutar"),

    ("Matrah", "Emekli Sandığı"),
    ("Yasal Kesintiler", "Emekli Sandığı Üye Payı"),
    ("Yasal Kesintiler", "İşsizlik Sig. Üye Payı"),
    
    ("Matrah", "Gelir Vergisi"),
    ("Yasal Kesintiler", "Gelir Vergisi"),
    ("Yasal Kesintiler", "Damga Vergisi"),
    
    ("Prim Ödemeleri Sonrası Oluşan", "Emekli Sandığı Devir Matrahı"),
    ("Prim Ödemeleri Sonrası Oluşan", "Emk. Snd. Devir Mat. Kullanılan"),

    ("Munzam Sandık Kesinti", "Üye Payı"),
    ("Munzam Sandık Kesinti", "Üye Yükselme Payı"),
    
    ("Yasal Asgari Ücret İadeleri", "Damga Vergisi İstisnası"),
    ("Yasal Asgari Ücret İadeleri", "Vergi İstisnası"),

    
    ("", "Yemek Ücreti (Brüt TL)"),
    ("", "Yemek Ücreti (Net TL)"),
])

tablo.columns = columns
 

tablo_ms = pd.DataFrame(dic_vrb, index=["Ocak","Şubat", "Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos",

                                 "Eylül","Ekim","Kasım","Aralık"])

 

tablo_mt = pd.DataFrame(dic_13, index=[0,1,2,3,4,5,6,7,8,9,10,11,12,13])
 

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

# ---- Ay Tabloları Gösterim --- --------------------------------------------------

# Renk teması ayarları
background_colors = ["#fce4ec", "#e3f2fd", "#f8bbd0"]  # Pembe-mavi tonları
text_color = "black"

# Açılır kapanır grup kutusu
with st.expander("Aylık Ücretler Detayları", expanded=False):
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
                    <p><strong>Brüt Ücretler Toplamınız</strong></p>
                    <p>{format(round(Toplam[i]), ',').replace(',', '.')} TL</p>
                    <p><strong>Yaklaşık Net Ücretiniz</strong></p>
                    <p>{format(round(net[i]), ',').replace(',', '.')} TL</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        # Yeni satıra geçmek için sütunları sıfırla
        if (i + 1) % 4 == 0:
            cols = st.columns(4)  # Yeni satır için sütunlar
#------------------------------------------------------------------------------------------


#streamlit tablo gösterimi
with st.expander("Yıllık Ücretleriniz Tablo Gösterimi"):
        st.dataframe(tablo.style.set_table_styles(
    ))



#st.table(tablo_ms)
#st.table(tablo_mt)


#---- PİE Charts ---- 

import altair as alt

with st.expander("Yıllık Ücret Dağılımı", expanded=False):# Donut chart verisi
    donut_data = pd.DataFrame({
        "Kategori": ["Net Ücret", "Kesintiler"],
        "Tutar": [sum(net), kesinti_toplam]
    })

    # Özel renk skalası
    color_scale = alt.Scale(
        domain=["Net Ücret: " + f"{sum(net):,.0f} TL", "Kesintiler: " + f"{kesinti_toplam:,.0f} TL"],
        range=["#FF69B4", "#40E0D0"]  # Pembe ve Turkuaz
    )

    # Donut Chart oluşturma
    base_chart = alt.Chart(donut_data).mark_arc(innerRadius=100, outerRadius=150).encode(
        theta=alt.Theta("Tutar:Q", stack=True),  # Dilim büyüklükleri
        color=alt.Color("Kategori:N", scale=color_scale, legend=alt.Legend(title="Kategori")),  # Renkler
        tooltip=[
            alt.Tooltip("Kategori:N")  # Tooltip'te sadece Kategori sütunu gösterilir
        ]
    ).properties(
        width=500,
        height=500
    )

    # "Kategori" ile "Tutar" bilgisini birleştirme
    donut_data["Kategori"] = donut_data["Kategori"] + ": " + donut_data["Tutar"].apply(lambda x: f"{x:,.0f} TL")

    # Dilimlere tutar değerlerini ekleme
    text_chart = alt.Chart(donut_data).mark_text(radiusOffset=-20, fontSize=12).encode(
        theta=alt.Theta("Tutar:Q", stack=True),
        text=alt.Text("Tutar:Q", format=',')
    )

    # Ortadaki brüt ücreti ekleme
    center_text = alt.Chart(pd.DataFrame({"label": [f"Ücretler Toplamı (Brüt TL): {round(sum(Toplam),2):,} TL"]})).mark_text(
        fontSize=16,
        align='center',
        baseline='middle'
    ).encode(
        text='label:N'
    )

    # Grafik katmanlama
    donut_chart = base_chart + center_text

    # Streamlit üzerinden Donut Chart gösterimi
    st.altair_chart(donut_chart, use_container_width=True)
