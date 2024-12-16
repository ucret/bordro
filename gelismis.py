import streamlit as st
import pandas as pd
import numpy as np
import math as mt
import random
from bs4 import BeautifulSoup
import re

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
dv=[0] * 12
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
    "Kambiyo Tazminatı", "Kıbrıs Tazminatı", "Kıd.BT Müfettiş Tazminatı", "Kıd.Kasa Tazminatı",
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

def yemekhane(i,gv_matrah,es_matrah,net, yemek_gun,cek_nakit=0): # 0= nakit , 1=çek 
    damga = 0.00759
    if cek_nakit==0:
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
    else:
        istisna =yemek_GV_istisna[i] * yemek_gun
        #net_toplam = net*yemek_gun
        vergili_kisim = net - istisna
        brut = brut_vergi(gv_matrah, vergili_kisim) + istisna
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

def html_brutten_nete(brut_tutar): #ESIS tavanı aşan durumlar için, brut tutarın dv ve gv ile brütten nete çevrilmesi örn.EkGörev Sıralama düzenlenebilir 
    gvmatrah = float(table_bordro[4].loc[6, 1].replace(",", ""))
    gve = float(table_bordro[4].loc[5, 1].replace(",", ""))
    return brut_tutar - vergi(gvmatrah - brut_tutar,brut_tutar) - (brut_tutar*0.00759)

def netten_brute_yemek_ayni(i,gv_matrah,net, gun, indirim = None): 
    damga = 0.00759
    istisna =yemek_GV_istisna[i] * gun
    net_toplam = net*gun
    vergili_kisim = net_toplam - istisna
    brut = brut_vergi(gv_matrah, vergili_kisim) + istisna
    return brut

aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]


if 'info_shown_sidebar' not in st.session_state:
    st.session_state.info_shown_sidebar = False

with st.sidebar:
    if st.button("📣 Uygulama Hakkında"):
        st.session_state.info_shown_sidebar = not st.session_state.info_shown_sidebar
        

if st.session_state.info_shown_sidebar:
    st.info("Net Gelir Hesaplama uygulaması ile yan panelden giriş yapacağınız ücretlerinizin yıl içerisindeki brüt/net ücret dağılımınızı aşağıdaki tablolarımız ile görebilirsiniz",icon="💁")
    st.info("Uygulamamız ile bordronuzdaki tutarların yaklaşık olmasını beklemekteyiz. Çocuk zammı, kasa tazminatı gibi bazı bireysel ödemeler ve bireysel sigorta kesintileri gibi kesintiler henüz uygulamamıza dahil değildir",icon="⚖️")
    st.info("Bilgilendirmeyi tamamladıysak '📣 Uygulama Hakkında' butonuna tıklayarak bilgi kutularını kapatabilirsiniz ",icon="✅")

st.sidebar.header("Ücret Girdi Alanları")

# HTML dosyasını kullanıcıdan yükleme
uploaded_file = st.file_uploader("Lütfen bir HTML bordro dosyası yükleyin:", type=["html"])

if uploaded_file is not None:
    # HTML içeriğini okuma ve ayrıştırma
    try:
        html_content = uploaded_file.read().decode("ISO-8859-9")
    except UnicodeDecodeError:
        st.error("Dosya kodlaması okunamadı. Lütfen doğru dosyayı yüklediğinizden emin olun.")

if html_content: #Yüklenen bordronun ayrı tablo ve dataframe'lere ayrılması
    # BeautifulSoup ile HTML'i ayrıştırma
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Tabloları bulma
    tables = soup.find_all('table')
    st.write(f"Toplam {len(tables)} tablo bulundu.")

    # Tabloları ayrı ayrı ayrıştırma ve gösterme
    if len(tables) > 0:
        for i, table in enumerate(tables):
            table_data = []
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                if columns:  # Sütunları varsa ekle
                    row_data = [col.get_text(strip=True) for col in columns]
                    table_data.append(row_data)

            # DataFrame oluşturma
            df = pd.DataFrame(table_data)
            st.write(f"Tablo {i + 1}")
            st.dataframe(df)
            table_bordro.append(df)
    else:
        st.write("Hiç tablo bulunamadı.")


def veri_getir(bordro_kalem): #Tüm tablolarda veri getirir     
    tutar=0
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
    return tutar

def veri_getir_ucrettablosu(bordro_kalem): #Ücretler toplamı tablosundaki kalemlerden veri getirme     
    tutar=0
    for row in tables[3].find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 1:
            key = cells[0].get_text(strip=True)
            value = cells[1].get_text(strip=True).replace(",", "")
            try:
                value = float(value)  # Sayısal bir değer olup olmadığını kontrol et
                if key in bordro_kalem :
                    tutar += value
            except ValueError:
                continue
    return tutar

def veri_getir_kesintitablosu(bordro_kalem): #Kesintiler tablosundaki kalemlerden veri getirme     
    tutar=0
    for row in tables[4].find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 1:
            key = cells[0].get_text(strip=True)
            value = cells[1].get_text(strip=True).replace(",", "")
            try:
                value = float(value)  # Sayısal bir değer olup olmadığını kontrol et
                if key in bordro_kalem:
                    tutar += value
            except ValueError:
                continue
    return tutar



yuklenen_bordro_ay=int(table_bordro[1].loc[4,1].split('-')[1].split('/')[0]) # Kullanıcının yüklediği bordronun ay bilgisi

yemek_is_gunu = None
for row in tables[3].find_all('tr'): # "Yemek Ücreti" satırından iş günü sayısını alma
    cells = row.find_all('td')
    if len(cells) > 1:
        key = cells[0].get_text(strip=True)
        if "Yemek Ücreti" or "Yemek Çeki/ Kartı" in key:
            # Parantez içindeki sayıyı ayıkla
            match = re.search(r'\((\d+)\s*iş günü\)', key)
            if match:
                yemek_is_gunu = int(match.group(1))
                break

def html_yemek_secimi(i): # yemek seçim
    yemek_index=[0] * 12 
    for row in tables[3].find_all('tr'): 
        cells = row.find_all('td')
        if len(cells) > 1:
            key = cells[0].get_text(strip=True)
            if "Yemek Ücreti" in key:
                yemek_index[i] = 0
            if "Yemek Çeki/ Kartı" in key:
                yemek_index[i] = 1 
    return yemek_index[i]






#Yemek Çeki/ Kartı (15 iş günü)

html_kıra_yardımı=veri_getir_ucrettablosu("Kira Yardımı")

if html_kıra_yardımı > 30000: # Zam döneminde min kira'ya göre güncellenmesi gerekir  
    html_kıra_yardımı_net = html_brutten_nete(html_kıra_yardımı)
else:
    html_kıra_yardımı_brut= html_kıra_yardımı

html_ek_gorev_net=html_brutten_nete(veri_getir_ucrettablosu("İştirak Görev Ücreti"))

html_net_gelir = html_ek_gorev_net + html_kıra_yardımı_net 



with st.sidebar.expander("🗓️ 2024 Aralık"):
    onceki_aylik[0] = st.number_input(":money_with_wings: Maaş Tutarınız (Brüt TL):", step=1000,value=0
        ,help=" Bu alan 2024 yılı Aralık maaşınız ve 2025 Ocak maaşınızın arasındaki yükselme farkı hesaplaması için oluşturulmuştur.") # i=0: Aralık Ayı indeksi

for i, ay in enumerate(aylar):
    with st.sidebar.expander(f"🗓️ 2025 {ay}"):
        # Sabit Ödemeleriniz kısmı
        with st.container():
            st.markdown("### **Sabit Ödemeleriniz**")
            if i < yuklenen_bordro_ay: # Kullanıcı HTML yüklendiyse, yüklediği aydan öncekileri dondur
                html_maas = int(float(veri_getir_ucrettablosu("Maaş"))) if i >= yuklenen_bordro_ay-1 else (Aylık[i - 1] if i > 0 else 0)
                html_tazm_top_a = int(float(veri_getir_ucrettablosu(tazminat_kalemleri))) + int(html_kıra_yardımı_brut) if i >= yuklenen_bordro_ay-1 else (Tazm_Top[i - 1] if i > 0 else 0)
                html_yemek_gun_say=int(float(yemek_is_gunu)) if i >= yuklenen_bordro_ay-1 else (yemek_gun_say[i - 1] if i > 0 else 0)  
                html_net_gelir_a = int(html_net_gelir) if i >= yuklenen_bordro_ay-1 else (ek_gorev[i - 1] if i > 0 else 0)     

                Aylık[i] = st.number_input(f":money_with_wings: Maaş Tutarınız (Brüt TL)",step=1000,value=html_maas, key=f"Aylik_{i}",
                help="Hesaplama bordro verileriniz ile devam etmektedir",disabled=True)
                
                ikramiye[i] = mt.ceil(Aylık[i] / 3)
                st.write(f":money_with_wings: İkramiye Tutarınız: {format(ikramiye[i], ',').replace(',', '.')} TL")
                
                Tazm_Top[i] = st.number_input(f":money_with_wings: Tazminat Toplamlarınız (Brüt TL)", step=1000, value=html_tazm_top_a, key=f"Tazm_Top_{i}",
                    help="Hesaplama bordro verileriniz ile devam etmektedir",disabled=True)
                
                yemek_gun_say[i]= st.number_input(f"🍔 Yemek Gün Sayınızı Giriniz", step=1, value=html_yemek_gun_say, key=f"yemek_gun_say{i}",disabled=True)
                
                if i==0 or i==6:
                    yemek_secim[i]=st.radio("",options=["Nakit","Yemek Çeki"],index=html_yemek_secimi(i) if i == 0 else ["Nakit", "Yemek Çeki"].index(yemek_secim[i - 1]),key=f"yemek_secim_{i}",horizontal=True,disabled=True)
                else:
                    yemek_secim[i]=yemek_secim[i-1]

                ek_gorev[i] = st.number_input(f":money_with_wings: İlave Ödemeleriniz (Net TL)", step=1000, value=html_net_gelir_a, key=f"ek_gorev_{i}"
                    ,help="Hesaplama bordro verileriniz ile devam etmektedir",disabled=True)
            
            else:    
                Aylık[i] = st.number_input(f":money_with_wings: Maaş Tutarınız (Brüt TL)",step=1000,value=Aylık[i] if i == 0 else Aylık[i - 1], key=f"Aylik_{i}",
                    help="Aylık ücretinizi bu alana girebilirsiniz (Bordronuzdaki 'Maaş' alanı)")
            
                ikramiye[i] = mt.ceil(Aylık[i] / 3)
                st.write(f":money_with_wings: İkramiye Tutarınız: {format(ikramiye[i], ',').replace(',', '.')} TL")
            
                Tazm_Top[i] = st.number_input(f":money_with_wings: Tazminat Toplamlarınız (Brüt TL)", step=1000, value=Tazm_Top[i - 1] if i > 0 else 0, key=f"Tazm_Top_{i}",
                    help="Unvan, Yabancı Dil, Kambiyo, Mali Tahlil gibi tazminatlarınızın toplamını bu alana girebilirsiniz")
            
                ek_gorev[i] = st.number_input(f":money_with_wings: İlave Ödemeleriniz (Net TL)", step=1000, value=ek_gorev[i - 1] if i > 0 else 0, key=f"ek_gorev_{i}"
                    ,help="Sabit net gelirlerinizi bu alana girebilirsiniz")
            
                yemek_gun_say[i]= st.number_input(f"🍔 Yemek Gün Sayınızı Giriniz", step=1, value=yemek_gun_say[i - 1] if i > 0 else 0, key=f"yemek_gun_say{i}")
                
                if i==0 or i==6:
                    yemek_secim[i]=st.radio("",options=["Nakit","Yemek Çeki"],index=0 if i == 0 else ["Nakit", "Yemek Çeki"].index(yemek_secim[i - 1]),key=f"yemek_secim_{i}",horizontal=True)
                else:
                    yemek_secim[i]=yemek_secim[i-1]
                
                yemek_net[i]=yemek_gun_say[i] * banka_yemek[i]
                
                asgari_ucret_uyari(Aylık[i]+ikramiye[i]+Tazm_Top[i]+ek_gorev[i])

            
                
            send_aidat[i]=Aylık[i] * 0.015
                        
        # Değişken Ödemeleriniz kısmı
        st.markdown("### **Değişken Ödemeleriniz**")
        if i < yuklenen_bordro_ay: # Kullanıcı HTML yüklendiyse, yüklediği aydan öncekileri dondur
            if i==3:
                ilave[i] = st.number_input(f":money_with_wings: İlave Ödemeleriniz (Brüt TL)", step=1000, value=0, key=f"ilave_{i}"
                    ,help="Hesaplama bordro verileriniz ile devam etmektedir",disabled=True)
                jest[i] = st.number_input(f"Jestiyon Tutarınız (Net TL)", step=1000, value=0, key=f"jest_{i}"
                    ,help="Hesaplama bordro verileriniz ile devam etmektedir",disabled=True)
            else:
                ilave[i] = st.number_input(f":money_with_wings: İlave Ödemeleriniz (Brüt TL)", step=1000, value=0, key=f"ilave_{i}"
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
st.write(yemek_secim)

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

        igv[i] = min(gv[i],igv[i])
        idv[i] = min(idv[i],dv[i])

        Toplam_Ms_Dahil[i] = (veri_getir("ÜCRETLER TOPLAMI TL") or 0) + (veri_getir("MS Banka Katılma Payı") or 0)
        Toplam[i]=veri_getir("ÜCRETLER TOPLAMI TL")
        net[i] = max(0,round((Toplam_Ms_Dahil[i]-(sske[i]+sski[i]+dv[i]+gv[i]) + igv[i] + idv[i]-ms_C[i]-ms_B[i]-ms_yukselme_C_net[i]-ms_yukselme_B_net[i]-send_aidat[i]),2))

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
        yemek_brut[i]=yemekhane(i,kvm[i],sskm[i],yemek_net[i],yemek_gun_say[i],yemek_secim[i])
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
        kvm[i] = kvm[i] +(yemek_gun_say[i]*yemek_ESIS_istisna[i])*0.15 - (yemek_gun_say[i]*yemek_GV_istisna[i]) - send_aidat[i] #İNDİRMLERİ EKLE!!!!!!!!!-------------
        
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
    ("💸 💸 💸 💸 💸 💸 💸 💸 💸 💸", "Ücretler Toplamı"),
    ("💸 💸 💸 💸 💸 💸 💸 💸 💸 💸", "Yaklaşık Net Tutar"),

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

    
    ("🍕🌮🍜", "Yemek Ücreti (Brüt TL)"),
    ("🍕🌮🍜", "Yemek Ücreti (Net TL)"),
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

# ---- Ay Tabloları Gösterim ----------------------------------------------------

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
                    <h3 style="text-align: left; color: {text_color}; font-size: 21px;">{ay}</h3>
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



st.table(tablo_ms)
st.table(tablo_mt)

def tutar_format(value):
    
    formatted_value = f"{value:,.2f}"  # Binlik ayraçlar ve iki ondalık basamak
    formatted_value = formatted_value.replace(",", "X").replace(".", ",").replace("X", ".")
    return formatted_value

#---- PİE Charts ---- 

import altair as alt

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
