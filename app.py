import streamlit as st
from datetime import datetime, timedelta

# Sayfa Ayarları
st.set_page_config(page_title="Vardiya Takvimim", page_icon="📅")

st.title("🏃‍♂️ Çalışma Takvimi")
st.write("Vardiya durumunuzu öğrenmek için tarih seçin.")

# Döngü başlangıcı: 9 Şubat 2026
BASLANGIC = datetime(2026, 2, 9).date()

def hesapla(secilen_tarih):
    fark = (secilen_tarih - BASLANGIC).days
    if fark < 0:
        return None, "Lütfen 9 Şubat 2026 ve sonrası bir tarih seçin."
    
    dongu_gunu = fark % 10 # 5 Gündüz + 5 Gece = 10 günlük döngü
    
    if dongu_gunu <= 4:
        # Gündüz Vardiyası
        sira = dongu_gunu + 1
        return "GÜNDÜZ", f"☀️ **Gündüz Vardiyası**ndasınız.\n\n⏰ Saat: 08:00 - 19:00\n\n📅 Bu, 5 günlük serinin **{sira}.** günü."
    else:
        # Gece Vardiyası
        sira = dongu_gunu - 4
        ertesi = secilen_tarih + timedelta(days=1)
        return "GECE", f"🌙 **Gece Vardiyası**ndasınız.\n\n⏰ Giriş: {secilen_tarih.strftime('%d.%m')} saat 19:00\n\n⏰ Çıkış: {ertesi.strftime('%d.%m')} saat 08:00\n\n📅 Bu, 5 gecelik serinin **{sira}.** gecesi."

# Tarih Seçici
tarih = st.date_input("Bir Tarih Seçin", datetime.now().date())

if tarih:
    tip, mesaj = hesapla(tarih)
    if tip == "GÜNDÜZ":
        st.success(mesaj)
    elif tip == "GECE":
        st.info(mesaj)
    else:
        st.warning(mesaj)

# Bilgi Notu
st.divider()
st.caption("Not: Döngü 9 Şubat 2026 Pazartesi günü 5 günlük gündüz mesaisi ile başlar.")
