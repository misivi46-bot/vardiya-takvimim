import streamlit as st
from datetime import datetime, timedelta

# Sayfa Ayarları
st.set_page_config(page_title="3'lü Vardiya Sistemi", page_icon="🏭")

st.title("🏭 Vardiya Takip Sistemi")
st.write("Tarih seçerek tüm grupların durumunu görüntüleyin.")

# Referans: 2. Grup (SEN) 9 Şubat 2026'da Gündüz Vardiyasına başlıyor.
BASLANGIC = datetime(2026, 2, 9).date()

def durum_belirle(grup_adi, dongu_gunu, secilen_tarih):
    """
    Verilen döngü gününe (0-14) göre grubun ne yaptığını metin ve renk olarak döndürür.
    """
    
    # --- DURUM 1: GÜNDÜZ VARDİYASI (0-4. günler) ---
    if 0 <= dongu_gunu <= 4:
        kacinci = dongu_gunu + 1
        baslik = f"☀️ {grup_adi}: GÜNDÜZ VARDİYASI"
        detay = f"⏰ 08:00 - 19:00\n📅 5 günlük serinin **{kacinci}.** günü."
        renk = "success" # Yeşil

    # --- DURUM 2: GECE İŞE GİDİŞ (5, 7, 9, 11, 13. günler) ---
    elif dongu_gunu in [5, 7, 9, 11, 13]:
        nobet_sirasi = ((dongu_gunu - 5) // 2) + 1
        ertesi_gun = secilen_tarih + timedelta(days=1)
        baslik = f"🌙 {grup_adi}: GECE VARDİYASI (İŞ BAŞI)"
        detay = f"⏰ Giriş: 19:00 -> Çıkış: Yarın 08:00\n🔢 **{nobet_sirasi}.** gece nöbetine gidiliyor."
        renk = "error" # Kırmızı

    # --- DURUM 3: İSTİRAHAT (6, 8, 10, 12, 14. günler) ---
    else:
        biten_nobet = ((dongu_gunu - 6) // 2) + 1
        uyari = ""
        if dongu_gunu == 14:
            uyari = "\n⚠️ **DİKKAT:** Yarın sabah 08:00'de Gündüz vardiyası başlıyor!"
        
        baslik = f"🛌 {grup_adi}: İSTİRAHAT (GECEDEN ÇIKIŞ)"
        detay = f"✅ Sabah 08:00'de **{biten_nobet}. nöbetten** çıkıldı.\n💤 Bugün ve gece komple istirahat.{uyari}"
        renk = "info" # Mavi
        
    return baslik, detay, renk

# Tarih Seçici
tarih = st.date_input("Sorgulanacak Tarih", datetime.now().date())
st.markdown("---")

if tarih:
    fark = (tarih - BASLANGIC).days
    
    if fark < 0:
        st.warning("Lütfen 9 Şubat 2026 ve sonrası bir tarih seçin.")
    else:
        # Döngü Hesaplamaları (15 Günlük Periyot)
        # Sen (2. Grup) referanssın.
        # 3. Grup, senin gündüzün bitince başlar (Senden 5 gün sonra başlar).
        # 1. Grup, 3. grup bitince başlar (Senden 10 gün sonra başlar).
        
        # Matematiksel Ofset Hesabı:
        # Grup 2 (Sen): fark % 15
        # Grup 3: (fark - 5) % 15 -> Senden 5 gün geriden gelir.
        # Grup 1: (fark - 10) % 15 -> Senden 10 gün geriden gelir.

        idx_grup2 = fark % 15
        idx_grup3 = (fark - 5) % 15
        idx_grup1 = (fark - 10) % 15

        # --- SENİN GRUBUN (GRUP 2) ---
        st.header("👤 Sizin Grubunuz (2. Grup)")
        baslik, detay, renk = durum_belirle("2. Grup", idx_grup2, tarih)
        
        if renk == "success":
            st.success(f"**{baslik}**\n\n{detay}")
        elif renk == "error":
            st.error(f"**{baslik}**\n\n{detay}")
        else:
            st.info(f"**{baslik}**\n\n{detay}")

        st.markdown("---")
        st.subheader("👥 Diğer Gruplar")

        # Yan yana kolonlar oluştur
        col1, col2 = st.columns(2)

        # --- GRUP 3 ---
        with col1:
            baslik3, detay3, renk3 = durum_belirle("3. Grup", idx_grup3, tarih)
            if renk3 == "success":
                st.success(f"**{baslik3}**\n\n{detay3}")
            elif renk3 == "error":
                st.error(f"**{baslik3}**\n\n{detay3}")
            else:
                st.info(f"**{baslik3}**\n\n{detay3}")

        # --- GRUP 1 ---
        with col2:
            baslik1, detay1, renk1 = durum_belirle("1. Grup", idx_grup1, tarih)
            if renk1 == "success":
                st.success(f"**{baslik1}**\n\n{detay1}")
            elif renk1 == "error":
                st.error(f"**{baslik1}**\n\n{detay1}")
            else:
                st.info(f"**{baslik1}**\n\n{detay1}")
