import streamlit as st
from datetime import datetime, timedelta

# Sayfa Ayarları
st.set_page_config(page_title="Vardiya Takvimim", page_icon="📅")

st.title("🗓️ Vardiya Takip Sistemi")
st.write("Tarih seçerek çalışma durumunuzu kontrol edin.")

# Döngü başlangıcı: 9 Şubat 2026 (Gündüz vardiyasının 1. günü)
BASLANGIC = datetime(2026, 2, 9).date()

def hesapla(secilen_tarih):
    # Gün farkını al
    fark = (secilen_tarih - BASLANGIC).days
    
    if fark < 0:
        return "HATA", "Lütfen 9 Şubat 2026 ve sonrası bir tarih seçin."
    
    # Döngü toplam 15 gün sürüyor (5 Gündüz + 10 gün süren Gece periyodu)
    dongu_gunu = fark % 15 
    
    # --- DURUM 1: GÜNDÜZ VARDİYASI (0, 1, 2, 3, 4. günler) ---
    if 0 <= dongu_gunu <= 4:
        kacinci = dongu_gunu + 1
        return "GUNDUZ", f"☀️ **GÜNDÜZ VARDİYASI**\n\n⏰ Çalışma Saati: 08:00 - 19:00\n\n📅 Durum: 5 günlük gündüz serisinin **{kacinci}.** günündesiniz."

    # --- DURUM 2: GECE İŞE GİDİŞ (5, 7, 9, 11, 13. günler) ---
    # Bu günlerde akşam 19:00'da iş başı yapılır.
    elif dongu_gunu in [5, 7, 9, 11, 13]:
        nobet_sirasi = ((dongu_gunu - 5) // 2) + 1
        ertesi_gun = secilen_tarih + timedelta(days=1)
        return "GECE_IS", f"🌙 **GECE VARDİYASI (İŞ BAŞI)**\n\n⏰ Giriş: Bu akşam 19:00\n🚪 Çıkış: Yarın sabah ({ertesi_gun.strftime('%d.%m.%Y')}) 08:00\n\n🔢 Durum: **{nobet_sirasi}.** gece nöbetine gidiyorsunuz."

    # --- DURUM 3: İSTİRAHAT (6, 8, 10, 12, 14. günler) ---
    # Bu günler, sabah işten çıktığın ve o akşam işe gitmediğin günlerdir.
    else:
        # Hangi geceden çıktığını hesapla
        biten_nobet = ((dongu_gunu - 6) // 2) + 1
        
        # Eğer döngünün son günü (14. gün) ise özel uyarı ekle
        ek_not = ""
        if dongu_gunu == 14:
            ek_not = "\n\n⚠️ **DİKKAT:** Bu son istirahat gününüz. Yarın sabah 08:00'de Gündüz vardiyası başlıyor!"
        else:
            ek_not = "\n\n🔜 **Durum:** Bu akşam iş yok, yarın akşam 19:00'da tekrar işe gideceksiniz."

        return "ISTIRAHAT", f"🛌 **İSTİRAHAT (GECEDEN ÇIKIŞ)**\n\n✅ Bu sabah 08:00'de **{biten_nobet}. gece** nöbetinden çıktınız.\n💤 Bugün ve bu gece tamamen dinleniyorsunuz.{ek_not}"

# Tarih Seçici
tarih = st.date_input("Sorgulanacak Tarih", datetime.now().date())

if tarih:
    durum, mesaj = hesapla(tarih)
    
    if durum == "GUNDUZ":
        st.success(mesaj) # YEŞİL KUTU
    elif durum == "GECE_IS":
        st.error(mesaj)   # KIRMIZI KUTU (Dikkat çekmesi için)
    elif durum == "ISTIRAHAT":
        st.info(mesaj)    # MAVİ KUTU (Dinlenme/Bilgi)
    else:
        st.warning(mesaj)
