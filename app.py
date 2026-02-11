import streamlit as st
from datetime import datetime, timedelta

# Sayfa Ayarları
st.set_page_config(page_title="Vardiya Takvimim", page_icon="📅")

st.title("🗓️ Vardiya Takip")
st.write("Tarih seçerek çalışma durumunuzu kontrol edin.")

# Döngü başlangıcı: 9 Şubat 2026 (İlk Gündüz Vardiyası)
BASLANGIC = datetime(2026, 2, 9).date()

def hesapla(secilen_tarih):
    fark = (secilen_tarih - BASLANGIC).days
    
    if fark < 0:
        return "HATA", "Lütfen 9 Şubat 2026 ve sonrası bir tarih seçin."
    
    # Döngü artık 15 gün sürüyor (5 gün gündüz + 10 gün geceye yayılmış nöbetler)
    dongu_gunu = fark % 15 
    
    # 1. BÖLÜM: GÜNDÜZ VARDİYASI (İlk 5 gün peş peşe)
    if 0 <= dongu_gunu <= 4:
        kacinci = dongu_gunu + 1
        return "GÜNDÜZ", f"☀️ **GÜNDÜZ VARDİYASI**\n\n⏰ Saat: 08:00 - 19:00\n\n📅 Durum: 5 günlük serinin **{kacinci}.** günü."

    # 2. BÖLÜM: GECE VARDİYASI VE BOŞ GÜNLER
    # Gece işe gidilen günler: 5, 7, 9, 11, 13. günler (Döngü indeksine göre)
    elif dongu_gunu in [5, 7, 9, 11, 13]:
        # Hangi nöbet olduğunu bulalım (1., 2., 3., 4. veya 5. nöbet)
        nobet_sirasi = ((dongu_gunu - 5) // 2) + 1
        ertesi_gun = secilen_tarih + timedelta(days=1)
        return "GECE", f"🌙 **GECE VARDİYASI**\n\n⏰ Giriş: Bugün 19:00\n🚪 Çıkış: Yarın ({ertesi_gun.strftime('%d.%m')}) 08:00\n\n🔢 Durum: 5 gecelik serinin **{nobet_sirasi}.** nöbeti."

    # 3. BÖLÜM: İSTİRAHAT GÜNLERİ (Gece çıkışı olan günler)
    # 6, 8, 10, 12, 14. günler
    else:
        # Son dinlenme günü mü kontrol et (Ertesi gün gündüz vardiyası başlar)
        if dongu_gunu == 14:
             return "BOS", "☕ **İSTİRAHAT (DÖNGÜ SONU)**\n\n✅ Bu sabah işten çıktınız, bu akşam iş yok.\n\n🔄 **DİKKAT:** Yarın sabah 08:00'de Gündüz vardiyası ile başa dönüyorsunuz!"
        else:
             return "BOS", "☕ **İSTİRAHAT GÜNÜ**\n\n✅ Bu sabah işten çıktınız, bu akşam işe gitmiyorsunuz.\n\n🔜 Bir sonraki nöbet: Yarın akşam 19:00'da."

# Tarih Seçici
tarih = st.date_input("Sorgulanacak Tarih", datetime.now().date())

if tarih:
    tip, mesaj = hesapla(tarih)
    
    if tip == "GÜNDÜZ":
        st.success(mesaj)
    elif tip == "GECE":
        st.error(mesaj) # Gece olduğu için kırmızı/dikkat çekici
    elif tip == "BOS":
        st.info(mesaj)  # Dinlenme olduğu için mavi/bilgi
    else:
        st.warning(mesaj)
