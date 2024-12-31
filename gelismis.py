import streamlit as st
import pandas as pd
import numpy as np
import math as mt
import random
from bs4 import BeautifulSoup
import re
#import matplotlib.pyplot as plt
#import plotly.graph_objects as go
import altair as alt

#---PARAMETRELER --- 
igv = [3315.70,3315.70,3315.70,3315.70,3315.70,3315.70,3315.70,4257.57,4420.94,4420.94,4420.94,4420.94] #Gelir vergisi istisnası 2025 güncellendi
asgari_ucret_brut=26005.5 #2025 güncellendi
asgari_ucret_gunluk= round(asgari_ucret_brut / 30,2)
yemek_sgk_ist=round(asgari_ucret_gunluk * 0.2365,2)
tavan = [asgari_ucret_brut * 7.5 if i < 6 else asgari_ucret_brut * 7.5 for i in range(12)] #Emekli sandığı tavanı 2025 güncellendi
idv =  [197.38]*12 # vergi istisnası 2025 güncellendi
yemek_ESIS_istisna=[yemek_sgk_ist if i < 6 else yemek_sgk_ist for i in range(12)]
yemek_GV_istisna=[240]*12 # 2025 güncellendi
v = [158000, 330000, 1200000,4300000] # 2025 güncellendi
o = [0.15,0.2,0.27,0.35,0.4] # 2025 güncellendi
banka_yemek = [300 if i < 6 else 300 for i in range(12)]

#------------------------------------------



aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
Aylık = [0]*12 #Aylık Ücret
onceki_aylik=[0]*13
onceki_aylik[0] = 33000
Tazm_Top = [0]*12 # Aylık ücret dışındaki Tazminatlar toplamı
ilave = [0]*12 #Ay içinde ödenen değişken ücret- brüt
ikramiye =[0]*12 #İkramiye
send_aidat=[0]*12 #sendika aidatı 

yemek_net = [0]*12
yemek_gun_say = [0]*12


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
dv=[0] * 12




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



#html değişkenleri 
table_bordro = []
html_content=None
yuklenen_bordro_ay=0
html_tazm_top=0
html_ek_gorev_net=0
html_kıra_yardımı_brut=0
html_kıra_yardımı_net=0
html_kıra_yardımı=0
yemek_secim = [0] * 12


tazminat_kalemleri = [
    "Avukatlık Tazminatı (1)", "Avukatlık Tazminatı (2)", "BT Müfettiş Tazminatı",
    "BT Tazminatı", "BT Tazminatı (1)", "BT Tazminatı (2)", "BT Vardiya Tazminatı",
    "Çağrı Test Tazminatı", "Güvenlik ve Koruma Tazminatı", "İç Kontrol Görevlileri Tazminatı",
    "Kambiyo Tazminatı", "Kıbrıs Tazminatı", "Kıd.BT Müfettiş Tazminatı",
    "Kıd.Ünvan Tazminatı", "Mali Tahlil Tazminatı", "Müfettiş Ödeneği",
    "Mühendislik-Mimarlık Tazminatı  (2)", "Mühendislik-Mimarlık Tazminatı (1)",
    "Ölüm ve Yaralanma Tazminatı", "Proje Sorumluluğu Tazminatı", "Sınav Teşvik Ödeneği",
    "Takip Memuru Tazminatı", "Tazminat Farkı", "Teknik Personel Tazminatı", "Unvan Tazm.",
    "Uzmanlık Tazminatı", "Ünvan Tazminatı", "Vardiya Tazminatı Gece-MT", "Vardiya Tazminatı Gece-MY",
    "Yabancı Dil-Alm.-1.Derece", "Yabancı Dil-Alm.-2.Derece", "Yabancı Dil-Alm.-3.Derece",
    "Yabancı Dil-Alm.-4.Derece", "Yabancı Dil-Alm.-5.Derece", "Yabancı Dil-Alm.-6.Derece",
    "Yabancı Dil-Alm.-7.Derece", "Yabancı Dil-Fra.-1.Derece", "Yabancı Dil-Fra.-2.Derece",
    "Yabancı Dil-Fra.-3.Derece", "Yabancı Dil-Fra.-4.Derece", "Yabancı Dil-Fra.-5.Derece",
    "Yabancı Dil-Fra.-6.Derece", "Yabancı Dil-Fra.-7.Derece", "Yabancı Dil-İng.-1.Derece",
    "Yabancı Dil-İng.-2.Derece", "Yabancı Dil-İng.-3.Derece", "Yabancı Dil-İng.-4.Derece",
    "Yabancı Dil-İng.-5.Derece", "Yabancı Dil-İng.-6.Derece", "Yabancı Dil-İng.-7.Derece",
    "Yıpranma Tazminatı", "Yol Yardımı", "Yüksek Verimlilik Tazminatı Ücret Tutar"
]
 

odemeler_listesi = [
    "Avukatlık Vekalet Ücreti",
    "Ders Ücreti",
    "Doğrudan Satış Ekibi Yol Yardımı",
    "Ek Ödeme",
    "FM Diğer Tutar",
    "FM İzin Ödeme",
    "Geçici Deprem Desteği",
    "Geçici Taşınma Destek Ödemesi",
    "Hedef Ödül",
    "İç Kontrol Bölümü Yol Yardımı-Ankara",
    "İç Kontrol Bölümü Yol Yardımı-İstanbul",
    "İç Kontrol Bölümü Yol Yardımı-İzmir",
    "İlave Geçici Deprem Desteği Ödemesi",
    "İlk Giriş Ödeneği",
    "İnternet ve Enerji Gid. Dest. Ödemesi",
    "Ödül Brüt",
    "Özel Eğitim Destek Ödemesi",
    "PYS Prim Farkı",
    "PYS Primi",
    "Rol Bazlı İlave Geçici PYS Primi-Üç Ayl",
    "Satış Primi",
    "Sınav Teşvik Ödeneği Farkı",
    "Şehir İçi Görev Ödeneği",
    "Temettü",
    "TİS Ek Artış Ödeneği",
    "Yüksek Verimlilik"
]

Aylık = [39600,39600,39600,39600,39600,39600,47520,47520,47520,47520,47520,47520]

def vergi(kum, matrah):  # Vergi hesaplama fonksiyonu (doğru çalışan versiyon)
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
        gv_matrah2 = es_kalan_brut * 0.85 + gv_matrah 
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
    if ucret < asgari_ucret_brut:
        return st.error(f"Uyarı: Toplam brüt tutarınız {ucret} TL. Bu tutar {asgari_ucret_brut}'nin altında olmamalıdır.")

def html_brutten_nete(brut_tutar): #ESIS tavanı aşan durumlar için, brut tutarın dv ve gv ile brütten nete çevrilmesi örn.EkGörev Sıralama düzenlenebilir 
    gvmatrah = veri_getir_kesintitablosu("Kümülatif GV Matrah")
    gve = veri_getir_kesintitablosu("Gelir Vergisi")
    return brut_tutar - vergi(gvmatrah - brut_tutar,brut_tutar) - (brut_tutar*0.00759)

def netten_brute_yemek_ayni(i,gv_matrah,net, gun, indirim = None): 
    damga = 0.00759
    istisna =yemek_GV_istisna[i] * gun
    net_toplam = net*gun
    vergili_kisim = net_toplam - istisna
    brut = brut_vergi(gv_matrah, vergili_kisim) + istisna
    return brut

def veri_getir(bordro_kalem):
    tutar = 0.0
    try:
        for table in soup.find_all('table'):
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) > 1:
                    key = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True).replace(",", "")
                    try:
                        value = float(value)  # Sayısal bir değer olup olmadığını kontrol et
                        if key in bordro_kalem :
                            tutar = value
                    except ValueError:
                        continue
    except Exception as e:
        tutar=0
    return tutar

def veri_getir_ucrettablosu(bordro_kalem):
    tutar = 0.0
    try:
        # Tabloların varlığını kontrol et
        if tables and len(tables) > 4:  # En az 5 tablo mevcutsa
            for row in tables[3].find_all('tr'):  # 5. tabloyu ara
                cells = row.find_all('td')
                if len(cells) > 1:
                    key = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True).replace(",", "")
                    try:
                        if key.strip() == bordro_kalem:  # Tam eşleşme
                            tutar += float(value)   # İlk bulunan değeri döndür
                    except ValueError:
                        continue    
    except Exception as e:
        tutar=0
    return tutar

def veri_getir_kesintitablosu(bordro_kalem):
    tutar = 0.0
    try:
        # Tabloların varlığını kontrol et
        if tables and len(tables) > 4:  # En az 5 tablo mevcutsa
            for row in tables[4].find_all('tr'):  # 5. tabloyu ara
                cells = row.find_all('td')
                if len(cells) > 1:
                    key = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True).replace(",", "")
                    try:
                        if key.strip() == bordro_kalem:  # Tam eşleşme
                            tutar += float(value)   # İlk bulunan değeri döndür
                    except Exception:
                        continue    
    except Exception as e:
        tutar=0
    return tutar

def taztop(bordro_kalem):
    tutar = 0.0
    try:
        # Tabloların varlığını kontrol et
        if tables and len(tables) > 2:  # En az 5 tablo mevcutsa
            for row in tables[3].find_all('tr'):  # 5. tabloyu ara
                cells = row.find_all('td')
                if len(cells) > 1:
                    key = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True).replace(",", "")
                    try:
                        if key in bordro_kalem:  # Tam eşleşme
                            tutar += float(value)   # İlk bulunan değeri döndür
                    except Exception:
                        continue    
    except Exception as e:
        tutar=0
    return tutar

def yemek_brut_tutar():
        # Eğer tables mevcutsa işlem yap
    if 'tables' in globals() and len(tables) > 3:  # tables tanımlı ve en az 4 tablo varsa
        for row in tables[3].find_all('tr'):  # "Yemek Ücreti" satırından iş günü sayısını alma
            cells = row.find_all('td')
            if len(cells) > 1:
                key = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True).replace(",", "")
                if "Yemek Ücreti" in key or "Yemek Çeki/ Kartı" in key:
                    brut_tutar=float(value)    
    else:
        brut_tutar=0
    return brut_tutar

def html_yemek_secimi():  # yemek seçim
    index = 0
    if 'tables' in globals() and len(tables) > 3:  # tables globalde mi ve yeterli eleman var mı?
        for row in tables[3].find_all('tr'):
            cells = row.find_all('td')
            if len(cells) > 1:
                key = cells[0].get_text(strip=True)
                if "Yemek Ücreti" in key:
                    index = 0
                elif "Yemek Çeki/ Kartı" in key:
                    index = 1
    return index

def sidebar_ac():
    st.session_state.sidebar_open = True

def cont_ucur(cont_key, info_key=None):
    st.session_state.containers[cont_key] = False  # Container görünürlüğünü False yap
    if info_key:
        st.session_state.info_messages[info_key] = True  # İlgili info kutusunu göster

if "expanders" not in st.session_state:
    st.session_state.expanders = {
        "bordro_yukleme": True
    }

def html_kutu_kapa(exp_key):
    st.session_state.expanders[exp_key] = False



if "info_shown_sidebar" not in st.session_state:
    st.session_state.info_shown_sidebar = False

if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = False


        
if st.session_state.info_shown_sidebar:    
    st.info("Uygulamamız ile bordronuzdaki tutarların yaklaşık olmasını beklemekteyiz. __Çocuk zammı, kasa tazminatı__ gibi bireysel ödemeler ve bireysel sigorta gibi kesintiler henüz uygulamamıza dahil değildir", icon="❗")
    st.info("Temmuz ayı maaşına Toplu İş Sözleşmesi'ndeki esaslara göre zam oranı tahminini de eklemen gerektiğini hatırlatmak isteriz 😊", icon="❗")
    st.info("Bilgilendirmeyi tamamladıysan '📣 Uygulama Hakkında' butonuna tıklayarak bilgi kutularını kapatabilirsin ",icon="💯")

uploaded_file=None

with st.container(border=True):
    st.markdown('''
    **:blue[Bu uygulama finansal planlamanı daha etkili bir şekilde yapmana yardımcı olmak için geliştirilmiştir. Tasarlanan bu özel uygulama ücret hesaplamalarını kolaylaştırmayı amaçlıyor. Ücret detaylarını uygulamaya girerek ya da son bordronu yükleyerek yıl içinde oluşacak yaklaşık net gelirini kolayca öğrenebilirsin.]**''')

with st.expander("Bordro Dosyası Yükleme (Önerilen Yöntem)",icon="📎",expanded=True):
    st.markdown(
        """
        - 📥 **Dosya Adı**: `Bordro.html`
        """,
        help="Her ay sonu gelen bordro mailinin ekindeki bordro.html dosyasını yüklemelisin. Aynı zamanda IKON > Çalışan İşlemleri > E-Bordro sayfasından bordronu kendine mail atabilirsin"
    )
    
    uploaded_file = st.file_uploader(
        "⬆️ HTML Bordro Dosyası Yükleme Alanı",
        type=["html"],
        help="İstediğin bir ayın bordro dosyanı buradan yükleyerek hesaplamalara başlayabilirsin",
    )
     


if uploaded_file is not None:  # Yalnızca dosya yüklendiyse çalıştır
    try:
        # Dosya içeriğini oku
        html_content = uploaded_file.read().decode("ISO-8859-9")
        
        # HTML içeriğini ayrıştırma
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        tables = soup.find_all('table')

        table_bordro = []  # Tabloları saklamak için bir liste
        if len(tables) > 0:
            for i, table in enumerate(tables):
                table_data = []
                rows = table.find_all('tr')
                for row in rows:
                    columns = row.find_all('td')
                    if columns:
                        row_data = [col.get_text(strip=True) for col in columns]
                        table_data.append(row_data)

                # DataFrame oluşturma
                df = pd.DataFrame(table_data)
                table_bordro.append(df)

            # Tabloların uygunluğunu kontrol et ve hücre değerini al
            if table_bordro and len(table_bordro) > 1:
                try:
                    cell_value = table_bordro[1].loc[4, 1]  # Hücreye erişim
                    if isinstance(cell_value, str) and '-' in cell_value and '/' in cell_value:
                        yuklenen_bordro_ay = int(cell_value.split('-')[1].split('/')[0])
                    else:
                        yuklenen_bordro_ay = 0  # Varsayılan değer
                except (IndexError, KeyError):  # Hücre mevcut değilse
                    st.warning("Yüklediğiniz dosyada beklenen formatta bir tablo veya hücre bulunamadı.")
                    yuklenen_bordro_ay = 0  # Varsayılan ay
            else:
                st.warning("Beklenen formatta bordro tablosu bulunamadı.")
                yuklenen_bordro_ay = 0  # Varsayılan ay

            # Eğer tablo başarıyla ayrıştırılmışsa
            if yuklenen_bordro_ay > 0:
                sidebar_ac()
                st.info(
                    f"✅ {aylar[yuklenen_bordro_ay - 1]} ayı bordrosu başarıyla yüklendi."
                )
                with st.expander("❗ Bordro Yükleme Adımları",expanded=True):
                    st.markdown(
                        """
                        1️⃣ Aralık ayı maaş tutar bilgisini girmelisin (sadece 01.01.2025 tarihinden önce Bankamızda çalışmaya başladıysan).
                        
                        2️⃣ Açılan panellerden yüklediğin bordro ayından sonraki aylar için değişiklik yaparak programı kullanabilirsin.                
                        
                        3️⃣ Yüklediğin bordro ayından önceki aylar için manuel girişler kapalı olacaktır ve hesaplamalara dahil edilmeyecektir.
                        
                        4️⃣ Pys Primi, temettü gibi değişken ücretlerini de ilgili aylar için girmelisin.
                        
                        5️⃣ Aşağıdaki tablo ve grafikler ile ücretlerinin yıl içindeki dağılımını görebilirsin.
                        
                        
                        Bilmende Fayda Var:
                        
                        - Uygulama şuan için kasa tazminatı, çocuk yardımı gibi bireysel ödemeleri kapsamamaktadır.
                        - Temmuz ayından itibaren Toplu İş Sözleşmesi’nde belirlenen esaslara göre zam artış oranı tahminini eklemelisin.
                        
                        """                    
                            )
                cont_ucur("cont_mg")
            else:
                st.warning("Bordro dosyanız uygun formatta değil. Lütfen doğru bir dosya yükleyin.")
        else:
            st.warning("Yüklediğiniz dosyada hiç tablo bulunamadı. Lütfen bordro dosyanızın doğru formatta olduğundan emin olun.")
    except UnicodeDecodeError:
        st.error("Dosya kodlaması okunamadı. Lütfen doğru dosyayı yüklediğinizden emin olun.")


# Session state başlatma
if "containers" not in st.session_state:
    st.session_state.containers = {
        "cont_html": True,
        "cont_mg": True,
    }

if "info_messages" not in st.session_state:
    st.session_state.info_messages = {
        "info_mg": False,  # Manuel giriş info kutusu başlangıçta gizli
        "info_html": False  # Diğer info kutusu başlangıçta gizli
    }

# Placeholder'lar
placeholder1 = st.empty()
placeholder2 = st.empty()

# Manuel Giriş Container
if st.session_state.containers["cont_mg"]:
    with placeholder2.container(border=True):  # Placeholder içinde container
        col1, col2 = st.columns(2)
        with col1:
            st.write("✍🏼 Manuel Giriş (Alternatif Yöntem)")
        with col2:
            if st.button(
                "Manuel Giriş",
                help="Manuel Giriş butonuna tıkladığında ücret girdi paneli açılır ve panel ile ücretlerini girerek tahmini hesaplamlar yapabilirsin",
                key="btn_close_bordro"
            ):
                # Butona tıklandığında container'ı gizle ve bilgi mesajını göster
                html_kutu_kapa("bordro_yukleme")
                sidebar_ac()
                cont_ucur("cont_mg", "info_mg")
                placeholder2.empty()  # Placeholder temizlenir
                

# Bilgi Mesajı: Manuel Giriş
if st.session_state.info_messages["info_mg"]:
    #st.info("Manuel giriş adımları;yaparken solda açılan pencerede yer alan tüm alanları doldurman gerekiyor. Alanların içindeki açıklamalar ücretlerini doğru girmen için yardımcı olacaktır.",icon="❗")
        with st.expander("❗ Manuel Giriş Adımları",expanded=True):
            st.markdown(
            """
            1️⃣ Aralık ayı maaş tutar bilgisini girmelisin (sadece 01.01.2025 tarihinden önce Bankamızda çalışmaya başladıysan).
            
            2️⃣ Ocak ayına sabit ücretlerini (maaş, tazminat ...) girmelisin, uygulama kalan ayları otomatik dolduracaktır.
            
            3️⃣ Pys Primi, temettü gibi değişken ücretlerini de ilgili aylar için girmelisin.
            
            4️⃣  Aşağıdaki tablo ve grafikler ile ücretlerinin yıl içindeki dağılımını görebilirsin.
            
            Bilmende Fayda Var:
            
            - Uygulama şuan için kasa tazminatı, çocuk yardımı gibi bireysel ödemeleri kapsamamaktadır.
            - Temmuz ayından itibaren Toplu İş Sözleşmesi’nde belirlenen esaslara göre zam artış oranı tahminini eklemelisin.
            
            """   
        )
    

yemek_is_gunu = None

# Eğer tables mevcutsa işlem yap
if 'tables' in locals() and len(tables) > 3:  # tables tanımlı ve en az 4 tablo varsa
    for row in tables[3].find_all('tr'):  # "Yemek Ücreti" satırından iş günü sayısını alma
        cells = row.find_all('td')
        if len(cells) > 1:
            key = cells[0].get_text(strip=True)
            if "Yemek Ücreti" in key or "Yemek Çeki/ Kartı" in key:
                # Parantez içindeki sayıyı ayıkla
                match = re.search(r'\((\d+)\s*iş günü\)', key)
                if match:
                    yemek_is_gunu = int(match.group(1))
                    break
else:
    # Eğer tables tanımlı değilse veya yeterince tablo yoksa varsayılan değer
    yemek_is_gunu = 0  # Varsayılan değer

yemek_index=[0] * 12 


for ozan in range(len(yemek_index)):
    yemek_index[ozan] = html_yemek_secimi()


#Yemek Çeki/ Kartı (15 iş günü)

html_kıra_yardımı=veri_getir_ucrettablosu("Kira Yardımı")

if html_kıra_yardımı > 30000: # Zam döneminde min kira'ya göre güncellenmesi gerekir  
    html_kıra_yardımı_net = html_brutten_nete(html_kıra_yardımı)
else:
    html_kıra_yardımı_brut= html_kıra_yardımı

html_ek_gorev_net=html_brutten_nete(veri_getir_ucrettablosu("İştirak Görev Ücreti"))

html_net_gelir = html_ek_gorev_net + html_kıra_yardımı_net 

if 'info_shown_sidebar' not in st.session_state:
    st.session_state.info_shown_sidebar = False


if st.session_state.sidebar_open: 
    if st.sidebar.button("📣 Uygulama Hakkında"):
        st.session_state.info_shown_sidebar = not st.session_state.info_shown_sidebar
    

    st.sidebar.header("Ücret Girdi Paneli")


    with st.sidebar.expander("🗓️ 2024 Aralık", expanded=True):
        onceki_aylik[0] = st.number_input(":money_with_wings: Maaş Tutarınız (Brüt TL):", step=1000,value=0
            ,help="Bu alan 2024 yılı Aralık maaşınız ve 2025 Ocak maaşın arasındaki Munzam Sandık yükselme farkı hesaplaması için oluşturulmuştur. Bu alana giriş yapmazsan Munzam Sandık yükselme payı hesaplamalarda dikkate alınamayacaktır")

    for i, ay in enumerate(aylar):
        with st.sidebar.expander(f"🗓️ 2025 {ay}",expanded=(i==yuklenen_bordro_ay-1)):
            if i==6:
                st.info("Temmuz ayı maaşına Toplu İş Sözleşmesi'ndeki esaslara göre zam oranı tahminini de eklemen gerektiğini hatırlatmak isteriz 😊")
            # Sabit Ödemeleriniz kısmı
            with st.container():
                st.markdown("### **Sabit Ödemeleriniz**")
                if i < yuklenen_bordro_ay: # Kullanıcı HTML yüklendiyse, yüklediği aydan öncekileri dondur
                    html_maas = int(float(veri_getir_ucrettablosu("Maaş"))) if i >= yuklenen_bordro_ay-1 else (Aylık[i - 1] if i > 0 else 0)
                    html_tazm_top_a = int(float(taztop(tazminat_kalemleri))) + int(html_kıra_yardımı_brut) if i >= yuklenen_bordro_ay-1 else (Tazm_Top[i - 1] if i > 0 else 0)
                    html_yemek_gun_say=int(float(yemek_is_gunu)) if i >= yuklenen_bordro_ay-1 else (yemek_gun_say[i - 1] if i > 0 else 0)  
                    html_net_gelir_a = int(html_net_gelir) if i >= yuklenen_bordro_ay-1 else (ek_gorev[i - 1] if i > 0 else 0)     

                    Aylık[i] = st.number_input(f":money_with_wings: Maaş Tutarınız (Brüt TL)",step=1000,value=html_maas, key=f"Aylik_{i}",
                    help="Hesaplama bordro verileriniz ile devam etmektedir",disabled=True)
                    
                    ikramiye[i] = mt.ceil(Aylık[i] / 3)
                    st.write(f":money_with_wings: İkramiye Tutarınız: {format(ikramiye[i], ',').replace(',', '.')} TL")
                    
                    Tazm_Top[i] = st.number_input(f":money_with_wings: Tazminat Toplamınız (Brüt TL)", step=1000, value=html_tazm_top_a, key=f"Tazm_Top_{i}",
                        help="Hesaplama bordro verileriniz ile devam etmektedir",disabled=True)
                    
                    yemek_gun_say[i]= st.number_input(f"🍔 Yemek Gün Sayınızı Giriniz", step=1, value=html_yemek_gun_say, key=f"yemek_gun_say{i}",disabled=True)
                    
                    if i==0 or i==6:
                        yemek_secim[i]=st.radio("",options=["Nakit","Yemek Çeki"],index=yemek_index[i] if i == 0 else ["Nakit", "Yemek Çeki"].index(yemek_secim[i - 1]),key=f"yemek_secim_{i}",horizontal=True,disabled=True)
                    else:
                        yemek_secim[i]=yemek_secim[i-1]
                    

                    ek_gorev[i] = st.number_input(f":money_with_wings: İlave Ödemeleriniz (Net TL)", step=1000, value=html_net_gelir_a, key=f"ek_gorev_{i}"
                        ,help="Hesaplama bordro verileriniz ile devam etmektedir",disabled=True)
                
                else:    
                    Aylık[i] = st.number_input(f":money_with_wings: Maaş Tutarınız (Brüt TL)",step=1000,value=Aylık[i] if Aylik[i] >= 0 else Aylık[i - 1], key=f"Aylik_{i}",
                        help="Aylık ücretinizi bu alana girebilirsiniz (Bordronuzdaki 'Maaş' alanı)")
                
                    ikramiye[i] = mt.ceil(Aylık[i] / 3)
                    st.write(f":money_with_wings: İkramiye Tutarınız: {format(ikramiye[i], ',').replace(',', '.')} TL")
                
                    Tazm_Top[i] = st.number_input(f":money_with_wings: Tazminat Toplamınız (Brüt TL)", step=1000, value=Tazm_Top[i - 1] if i > 0 else 0, key=f"Tazm_Top_{i}",
                        help="Unvan, Yabancı Dil, Kambiyo, Mali Tahlil gibi tazminatlarınızın toplamını bu alana girebilirsiniz")
                
                    ek_gorev[i] = st.number_input(f":money_with_wings: İlave Ödemeleriniz (Net TL)", step=1000, value=ek_gorev[i - 1] if i > 0 else 0, key=f"ek_gorev_{i}"
                        ,help="Sabit net gelirlerinizi bu alana girebilirsiniz")
                
                    yemek_gun_say[i]= st.number_input(f"🍔 Yemek Gün Sayınızı Giriniz", step=1, value=yemek_gun_say[i - 1] if i > 0 else 0, key=f"yemek_gun_say{i}")
                    
                    if i==0 or i==6:
                        yemek_secim[i]=st.radio("",options=["Nakit","Yemek Çeki"],index=yemek_index[i] if i == 0 else ["Nakit", "Yemek Çeki"].index(yemek_secim[i - 1]),key=f"yemek_secim_{i}",horizontal=True)
                    else:
                        yemek_secim[i]=yemek_secim[i-1]
                    
                    yemek_net[i]=yemek_gun_say[i] * banka_yemek[i]
                    
                    asgari_ucret_uyari(Aylık[i]+ikramiye[i]+Tazm_Top[i]+ek_gorev[i])
                    yemek_index[i] = 1 if yemek_secim[i]=="Yemek Çeki" else 0
                
                
                send_aidat[i]=Aylık[i] * 0.015
                            
            # Değişken Ödemeleriniz kısmı
            st.markdown("### **Değişken Ödemeleriniz**")
            if i < yuklenen_bordro_ay: # Kullanıcı HTML yüklendiyse, yüklediği aydan öncekileri dondur
                html_brut_odenek = int(float(taztop(odemeler_listesi))) if i >= yuklenen_bordro_ay-1 else (ilave[i - 1] if i > 0 else 0)
                html_jest_net = int(float(veri_getir("Jestiyon Ödenen"))) if i >= yuklenen_bordro_ay-1 else (jest[i - 1] if i > 0 else 0)

                if i==3:
                    ilave[i] = st.number_input(f":money_with_wings: İlave Ödemeleriniz (Brüt TL)", step=1000, value=html_brut_odenek, key=f"ilave_{i}"
                        ,help="Hesaplama bordro verileriniz ile devam etmektedir",disabled=True)
                    jest[i] = st.number_input(f"Jestiyon Tutarınız (Net TL)", step=1000, value=html_jest_net, key=f"jest_{i}"
                        ,help="Hesaplama bordro verileriniz ile devam etmektedir",disabled=True)
                else:
                    ilave[i] = st.number_input(f":money_with_wings: İlave Ödemeleriniz (Brüt TL)", step=1000, value=html_brut_odenek, key=f"ilave_{i}"
                        ,help="Hesaplama bordro verileriniz ile devam etmektedir",disabled=True)
            else:
                if i==3:
                    ilave[i] = st.number_input(f":money_with_wings: İlave Ödemeleriniz (Brüt TL)", step=1000, value=0, key=f"ilave_{i}"
                        ,help="Ay içerisinde almış olduğunuz ilave brüt ödeneklerinizin (Satış Primi, Pys Primi, Temettü) toplamını bu alana girebilirsiniz.")
                    jest[i] = st.number_input(f"Jestiyon Tutarınız (Net TL)", step=1000, value=0, key=f"jest_{i}"
                        ,help="Jestiyon tutarınızı NET TL olarak bu alana girebilirsiniz")
                    
                else:
                    ilave[i] = st.number_input(f":money_with_wings: İlave Ödemeleriniz (Brüt TL)", step=1000, value=0, key=f"ilave_{i}"
                        ,help="Ay içerisinde almış olduğunuz ilave brüt ödeneklerinizin (Satış Primi, Pys Primi, Temettü) toplamını bu alana girebilirsiniz.")




yemek_brut=[0]*12


for i in range(12): # i = ilgili ay, 12 ay için döngü
    sandik_isleri(i,onceki_aylik[0] if i==0 else Aylık[i-1] ,Aylık[i])
    if i == yuklenen_bordro_ay-1:
        sskm[i] = veri_getir_kesintitablosu("Emekli Sandığı Matrahı")
        sske[i] = veri_getir_kesintitablosu("Emekli Sandığı Üye Payı")
        sski[i] = veri_getir_kesintitablosu("İşsizlik Sig. Üye Payı")
        dv[i] = veri_getir_kesintitablosu("Damga Vergisi")
        vm[i] = veri_getir_kesintitablosu("Gelir Vergisi Matrah")
        kvm[i] = veri_getir_kesintitablosu("Kümülatif GV Matrah")
        kvm[i+1] = veri_getir_kesintitablosu("Kümülatif GV Matrah")
        gv[i] = veri_getir_kesintitablosu("Gelir Vergisi")
        ms_B_brüt[i] = veri_getir_kesintitablosu("MS Banka Katılma Payı")
        yemek_brut[i] = yemek_brut_tutar()
        yemek_net[i]=yemek_is_gunu * banka_yemek[i] 

        igv[i] = min(gv[i],igv[i])
        idv[i] = min(idv[i],dv[i])
 
        Toplam_Ms_Dahil[i] = (veri_getir("ÜCRETLER TOPLAMI TL") or 0) + (veri_getir("MS Banka Katılma Payı") or 0)
        Toplam[i]=veri_getir("ÜCRETLER TOPLAMI TL")
        net[i] = max(0,round((Toplam_Ms_Dahil[i]-(sske[i]+sski[i]+dv[i]+gv[i]) + igv[i] + idv[i]-ms_C[i]-ms_B[i]-ms_yukselme_C_net[i]-ms_yukselme_B_net[i]-send_aidat[i]-(yemek_net[i]*yemek_index[i])),2))

        net_msli[i]= round((Toplam_Ms_Dahil[i]-(sske[i]+sski[i]+dv[i]+gv[i]) + igv[i] + idv[i]-ms_C[i]),2)
        net_mscli[i] = round((Toplam_Ms_Dahil[i]-(sske[i]+sski[i]+dv[i]+gv[i]) + igv[i] + idv[i]),2)
        ktoplam[i] = veri_getir_kesintitablosu("Emekli Sandığı Devir Matrahından Kullanılan")
        dtoplam[i] = veri_getir_kesintitablosu("Emekli Sandığı Devir Matrahı")
    else:
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
        kvm[i] = kvm[i] +(yemek_gun_say[i]*yemek_ESIS_istisna[i]) * 0.15 - (yemek_gun_say[i]*yemek_GV_istisna[i]) - send_aidat[i] 
        
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
    
        #Hesaplamalar sonrası matrahlar
        sske[i] = min(Toplam_Ms_Dahil[i],round(sskm[i]*0.14,2))
        sski[i] = min(Toplam_Ms_Dahil[i],round(sskm[i]*0.01,2))
        dv[i] = round((Toplam_Ms_Dahil[i]-(yemek_gun_say[i]*yemek_GV_istisna[i]))*0.00759,2)
        vm[i] = round(Toplam_Ms_Dahil[i]-sske[i]-sski[i]-(yemek_gun_say[i]*yemek_GV_istisna[i])-send_aidat[i],2)
        kvm[i+1] = round(kvm[i],2)
        gv[i] = max(0,round(vergi(kvm[i-1], vm[i]),2))

        igv[i] = min(gv[i],igv[i])
        idv[i] = min(idv[i],dv[i])
        net[i] = max(0,round((Toplam_Ms_Dahil[i]-(sske[i]+sski[i]+dv[i]+gv[i]) + igv[i] + idv[i]-ms_C[i]-ms_B[i]-ms_yukselme_C_net[i]-ms_yukselme_B_net[i]-send_aidat[i]-(yemek_net[i]*yemek_index[i])),2))

        net_msli[i]= round((Toplam_Ms_Dahil[i]-(sske[i]+sski[i]+dv[i]+gv[i]) + igv[i] + idv[i]-ms_C[i]),2)
        net_mscli[i] = round((Toplam_Ms_Dahil[i]-(sske[i]+sski[i]+dv[i]+gv[i]) + igv[i] + idv[i]),2)
        ktoplam[i] = devreden1_kullanılan[i] + devreden2_kullanılan[i]
        dtoplam[i] = devreden1[i] + devreden2[i]
    


kesinti_esis_toplam = sum(sske) + sum(sski)
kesinti_gvdv_toplam = sum(dv) + sum(gv) 
kesinti_toplam = kesinti_esis_toplam + kesinti_gvdv_toplam + sum(ms_C) + sum(ms_yukselme_C_net)



dic = {"Toplam Brüt Ücret": Toplam,"Yaklaşık Net Tutar": net,"Yemek Çeki":(np.array(yemek_net) *np.array(yemek_index)),  
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


tablo = pd.DataFrame(dic, index=["Ocak","Şubat", "Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos",

                                 "Eylül","Ekim","Kasım","Aralık"])

columns = pd.MultiIndex.from_tuples([   # Sözlük ve gösterim sıralaması önemli
    ("💸 💸 💸 💸 💸 💸 💸 💸 💸 💸", "Ücretler Toplamı"),
    ("💸 💸 💸 💸 💸 💸 💸 💸 💸 💸", "Yaklaşık Net Tutar"),
    ("💸 💸 💸 💸 💸 💸 💸 💸 💸 💸", "Yemek Çeki"),

    ("📈 Matrah", "Emekli Sandığı"),
    ("🏛️ Yasal Kesintiler", "Emekli Sandığı Üye Payı"),
    ("🏛️ Yasal Kesintiler", "İşsizlik Sig. Üye Payı"),
    
    ("📈 Matrah", "Gelir Vergisi"),
    ("🏛️ Yasal Kesintiler", "Gelir Vergisi"),
    ("🏛️ Yasal Kesintiler", "Damga Vergisi"),
    
    ("ℹ️ Prim Ödemeleri Sonrası Oluşan", "Emekli Sandığı Devir Matrahı"),
    ("ℹ️ Prim Ödemeleri Sonrası Oluşan", "Emk. Snd. Devir Mat. Kullanılan"),

    ("🪙 Munzam Sandık Kesinti", "Üye Payı"),
    ("🪙 Munzam Sandık Kesinti", "Üye Yükselme Payı"),
    
    ("Yasal Asgari Ücret İadeleri", "Damga Vergisi İstisnası"),
    ("Yasal Asgari Ücret İadeleri", "Vergi İstisnası"),

    
    ("🍕 🌮 Yemek Ücreti/Çeki", "     Brüt TL     "),
    ("🍕 🌮 Yemek Ücreti/Çeki", "     Net TL     "),
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

tablo = tablo.apply(lambda x: x.map("{:,.2f}₺".format) if x.dtype == "float" else x)

tablo_ms = tablo_ms.apply(lambda x: x.map("{:,.2f}₺".format) if x.dtype == "float" else x)

tablo_mt = tablo_mt.apply(lambda x: x.map("{:,.2f}₺".format) if x.dtype == "float" else x)
#st.table(tablo_ms)
#st.table(tablo_mt)

# ---- Ay Tabloları Gösterim ----------------------------------------------------

# Renk teması ayarları
#background_colors = ["#fce4ec", "#e3f2fd", "#f8bbd0"]  # Pembe-mavi tonları
#text_color = "black"


# Farkı hesaplayın
Kesintiler = [toplam - net for toplam, net in zip(Toplam, net)]

# Verileri DataFrame'e çevir
data = pd.DataFrame({
    "Aylar": aylar,
    "Net": net,
    "Kesintiler": Kesintiler
})

# Ayları sıralı kategorik veri olarak tanımla
data["Aylar"] = pd.Categorical(data["Aylar"], categories=[
    "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", 
    "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
], ordered=True)

chart = alt.Chart(data).transform_fold(
    ["Net", "Kesintiler"],  # Çizilecek sütunlar
    as_=["Kategori", "Toplam Brüt Ücret (TL)"]  # Yeniden düzenlenen sütun isimleri
).mark_bar().encode(
    x=alt.X("Aylar:N", sort=list(aylar)),  # Ayları sabit sıraya göre göster
    y=alt.Y("Toplam Brüt Ücret (TL):Q", scale=alt.Scale(domainMin=0)),
    color=alt.Color(
        "Kategori:N",
        scale=alt.Scale(
            domain=["Net", "Kesintiler"],  # Kategoriler
            range=["#FF69B4", "#40E0D0"]  # Özel renkler
        ),
        legend=alt.Legend(title="Kategori")  # Efsane başlığı
    ),
    tooltip=["Aylar:N", "Kategori:N", "Toplam Brüt Ücret (TL):Q"]
).properties(
    width=700,  # Grafik genişliği
    height=400,  # Grafik yüksekliği
).configure_view(
    stroke=None  # Grafik kenarlığını kaldırır
).interactive()



# Expander içinde grafiği göster
with st.expander("Aylık Ücretler Detayları", expanded=False):
    st.altair_chart(chart, use_container_width=True)
  



#------------------------------------------------------------------------------------------


#streamlit tablo gösterimi
with st.expander("Yıllık Ücretleriniz Tablo Gösterimi"):
        st.dataframe(tablo.style.set_table_styles(
    ))





def tutar_format(value):
    
    formatted_value = f"{value:,.2f}"  # Binlik ayraçlar ve iki ondalık basamak
    formatted_value = formatted_value.replace(",", "X").replace(".", ",").replace("X", ".")
    return formatted_value

#---- PİE Charts ---- 


with st.expander("Yıllık Ücret Dağılımı", expanded=False):
    # Donut chart verisi
    donut_data = pd.DataFrame({
        "Kategori": ["Net Ücret", "Kesintiler"],
        "Tutar": [sum(net), kesinti_toplam]
    })

    # Tutarları formatlayalım
    a = tutar_format(sum(net))
    b = tutar_format(kesinti_toplam)

    # "Kategori" ile "Tutar" bilgisini birleştirme (grafikten önce yapılır)
    donut_data["Kategori"] = donut_data["Kategori"] + ": " + donut_data["Tutar"].apply(lambda x: f"{tutar_format(x)} TL")

    # Özel renk skalası
    color_scale = alt.Scale(
        domain=donut_data["Kategori"].tolist(),  # Güncellenmiş Kategori sütununu kullan
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

    # Ortadaki yazılar için iki ayrı katman
    center_text_label = alt.Chart(pd.DataFrame({
        "label": ["Ücretler Toplamı (Brüt TL)"]
    })).mark_text(
        fontSize=16,
        align='center',
        baseline='bottom',
        dy=-10  # Yüksekliği yukarı taşı
    ).encode(
        text='label:N'
    )

    formatlanmıs_brut = tutar_format(round(sum(Toplam), 2))

    center_text_value = alt.Chart(pd.DataFrame({
        "value": [f"{formatlanmıs_brut} TL"]
    })).mark_text(
        fontSize=16,
        align='center',
        baseline='top',
        dy=10  # Yüksekliği aşağı taşı
    ).encode(
        text='value:N'
    )

    # Grafik katmanlama
    donut_chart = base_chart + center_text_label + center_text_value

    # Streamlit üzerinden Donut Chart gösterimi
    st.altair_chart(donut_chart, use_container_width=True)



