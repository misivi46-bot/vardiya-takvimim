import streamlit as st
from datetime import datetime, timedelta

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Vardiya Takip", page_icon="🏭")

st.title("🏭 Vardiya Takip Sistemi")

# --- GRUP SEÇİMİ (KULLANICI GİRİŞİ) ---
# Kullanıcıya hangi grupta olduğunu soruyoruz.
secilen_grup = st.selectbox(
    "Hangi grupta çalışıyorsunuz?",
    ("1. Grup", "2. Grup", "3. Grup"),
    index=1  # Varsayılan olarak 2. Grup seçili gelir
)

st.markdown("---")

# --- SABİTLER VE REFERANS ---
# Referans Noktası: 2. Grup, 9 Şubat 2026'da GÜNDÜZ vardiyasına başlar.
BASLANGIC = datetime(2026, 2, 9).date()

def durum_metni_olustur(grup_adi, dongu_gunu, tarih):
    """
    Döngü gününe (0-14) göre durum metnini, detayını ve rengini belirler.
    """
    # 1. BÖLÜM: GÜNDÜZ (0-4)
    if 0 <= dongu_gunu <= 4:
        kacinci = dongu_gunu + 1
        baslik = f"☀️ {grup_adi} - GÜNDÜZ VARDİYASI"
        detay = f"⏰ 08:00 - 19:00\n📅 Durum: 5 günlük serinin **{kacinci}.** günü."
        renk = "success" # Yeşil

    # 2. BÖLÜM: GECE İŞ (5, 7, 9, 11, 13)
    elif dongu_gunu in [5, 7, 9, 11, 13]:
        nobet_sirasi = ((dongu_gunu - 5) // 2) + 1
        ertesi_gun = tarih + timedelta(days=1)
        baslik = f"🌙 {grup_adi} - GECE VARDİYASI (İŞ BAŞI)"
        detay = f"⏰ Giriş: 19:00 -> Çıkış: Yarın 08:00\n🔢 Durum: **{nobet_sirasi}.** gece nöbetine gidiliyor."
        renk = "error" # Kırmızı

    # 3. BÖLÜM: İSTİRAHAT (6, 8, 10, 12, 14)
    else:
        biten_nobet = ((dongu_gunu - 6) // 2) + 1
        uyari = ""
        # Son gün uyarısı
        if dongu_gunu == 14:
            uyari = "\n⚠️ **DİKKAT:** Yarın sabah 08:00'de Gündüz vardiyası başlıyor!"
        
        baslik = f"🛌 {grup_adi} - İSTİRAHAT (GECEDEN ÇIKIŞ)"
        detay = f"✅ Sabah 08:00'de **{biten_nobet}. nöbetten** çıkıldı.\n💤 Bugün ve gece istirahat.{uyari}"
        renk = "info" # Mavi
        
    return baslik, detay, renk

# --- TARİH SEÇİMİ ---
tarih = st.date_input("Sorgulanacak Tarih", datetime.now().date())

# --- HESAPLAMALAR ---
if tarih:
    fark = (tarih - BASLANGIC).days
    
    if fark < 0:
        st.warning("Lütfen sistem başlangıcı olan 9 Şubat 2026 ve sonrası bir tarih seçin.")
    else:
        # Her grubun döngüdeki yerini hesapla (Mod 15)
        # 2. Grup Referans (fark)
        # 3. Grup, 2'den 5 gün sonra başlar (fark - 5)
        # 1. Grup, 3'ten 5 gün sonra başlar (fark - 10)
        
        idx_grup2 = fark % 15
        idx_grup3 = (fark - 5) % 15
        idx_grup1 = (fark - 10) % 15
        
        # Grupları bir sözlükte toplayalım ki seçime göre çekebilelim
        gruplar = {
            "1. Grup": idx_grup1,
            "2. Grup": idx_grup2,
            "3. Grup": idx_grup3
        }

        # --- 1. KULLANICININ SEÇTİĞİ GRUBU GÖSTER (ANA EKRAN) ---
        st.subheader(f"👤 Sizin Durumunuz ({secilen_grup})")
        
        secilen_idx = gruplar[secilen_grup]
        baslik, detay, renk = durum_metni_olustur(secilen_grup, secilen_idx, tarih)
        
        if renk == "success":
            st.success(f"**{baslik}**\n\n{detay}")
        elif renk == "error":
            st.error(f"**{baslik}**\n\n{detay}")
        else:
            st.info(f"**{baslik}**\n\n{detay}")

        # --- 2. DİĞER GRUPLARI GÖSTER (ALT EKRAN) ---
        st.markdown("---")
        st.caption("Diğer grupların durumu:")
        
        col1, col2 = st.columns(2)
        
        # Seçilen grup dışındaki diğer 2 grubu bul
        diger_gruplar = [g for g in gruplar.keys() if g != secilen_grup]
        
        # Sol Kutu (İlk diğer grup)
        with col1:
            grup_adi = diger_gruplar[0]
            g_idx = gruplar[grup_adi]
            baslik, detay, renk = durum_metni_olustur(grup_adi, g_idx, tarih)
            # Daha sade görünüm için st.markdown kullanalım
            if renk == "success": st.success(f"**{grup_adi}**\n\nGündüz")
            elif renk == "error": st.error(f"**{grup_adi}**\n\nGece İş")
            else: st.info(f"**{grup_adi}**\n\nİstirahat")
            with st.expander("Detay"):
                st.write(detay)

        # Sağ Kutu (İkinci diğer grup)
        with col2:
            grup_adi = diger_gruplar[1]
            g_idx = gruplar[grup_adi]
            baslik, detay, renk = durum_metni_olustur(grup_adi, g_idx, tarih)
            if renk == "success": st.success(f"**{grup_adi}**\n\nGündüz")
            elif renk == "error": st.error(f"**{grup_adi}**\n\nGece İş")
            else: st.info(f"**{grup_adi}**\n\nİstirahat")
            with st.expander("Detay"):
                st.write(detay)
