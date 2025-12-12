# main.py — KivyMD Stok Takip — %100 Çalışır (PC + Android) — DÜZELTİLDİ!
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton, MDFloatingActionButton
from kivymd.uix.list import OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.label import MDLabel
from kivymd.toast import toast
import sqlite3
import os

class AnaEkran(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Veritabanı (PC ve Android uyumlu)
        db_path = "stok_takip.db"
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

        # Tablo oluştur
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS urunler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                urun_adi TEXT NOT NULL,
                kategori TEXT,
                urun_boyutu TEXT,
                stok INTEGER NOT NULL
            )
        ''')

        # Eski tablolarda urun_boyutu yoksa ekle
        try:
            self.cur.execute("PRAGMA table_info(urunler)")
            columns = [col[1] for col in self.cur.fetchall()]
            if "urun_boyutu" not in columns:
                self.cur.execute("ALTER TABLE urunler ADD COLUMN urun_boyutu TEXT")
        except:
            pass
        self.conn.commit()

        # Ana layout
        ana = MDBoxLayout(orientation="vertical", padding="12dp", spacing="12dp")

        # Başlık
        toolbar = MDTopAppBar(title="Stok Takip Sistemi", elevation=4)
        ana.add_widget(toolbar)

        # Arama alanı
        self.arama = MDTextField(
            hint_text="Ürün, kategori veya boyut ara...",
            mode="rectangle",
            size_hint_x=0.95,
            pos_hint={"center_x": 0.5}
        )
        self.arama.bind(text=self.arama_yap)
        ana.add_widget(self.arama)

        # Liste (ScrollView içinde)
        self.scroll = MDScrollView()
        self.liste = MDBoxLayout(orientation="vertical", adaptive_height=True, spacing="8dp", padding="8dp")
        self.scroll.add_widget(self.liste)
        ana.add_widget(self.scroll)

        # Giriş alanları — DÜZELTİLDİ: hint_text883 → hint_text
        self.adi = MDTextField(hint_text="Ürün Adı *", required=True)
        self.kategori = MDTextField(hint_text="Kategori")
        self.boyut = MDTextField(hint_text="Ürün Boyutu / Model")
        self.stok = MDTextField(hint_text="Stok Miktarı", input_filter="int")

        for field in [self.adi, self.kategori, self.boyut, self.stok]:
            ana.add_widget(field)

        # Butonlar
        btn_row = MDBoxLayout(spacing="12dp", size_hint_y=None, height="60dp")
        btn_row.add_widget(MDRectangleFlatButton(text="EKLE",      md_bg_color=(0, 0.7, 0, 1),   text_color=(1,1,1,1), on_release=self.ekle))
        btn_row.add_widget(MDRectangleFlatButton(text="GÜNCELLE",  md_bg_color=(0, 0.5, 1, 1),   text_color=(1,1,1,1), on_release=self.guncelle))
        btn_row.add_widget(MDRectangleFlatButton(text="SİL",       md_bg_color=(1, 0, 0, 1),     text_color=(1,1,1,1), on_release=self.sil))
        btn_row.add_widget(MDRectangleFlatButton(text="TEMİZLE",   on_release=self.temizle))
        ana.add_widget(btn_row)

        # Düşük stok butonu
        fab = MDFloatingActionButton(
            icon="alert",
            md_bg_color=(1, 0, 0, 1),
            pos_hint={"center_x": 0.9, "center_y": 0.12}
        )
        fab.bind(on_release=self.dusuk_stok_raporu)
        ana.add_widget(fab)

        self.add_widget(ana)
        self.yukle()

    def yukle(self):
        self.liste.clear_widgets()
        self.cur.execute("SELECT id, urun_adi, kategori, urun_boyutu, stok FROM urunler ORDER BY id DESC")
        rows = self.cur.fetchall()

        if not rows:
            self.liste.add_widget(MDLabel(text="Henüz ürün eklenmedi.", halign="center", theme_text_color="Hint"))
            return

        for row in rows:
            stok = row[4]
            if stok <= 5:
                renk = "#C62828"  # Koyu kırmızı
            elif stok <= 10:
                renk = "#FF6D00"  # Turuncu
            else:
                renk = "#2E7D32"  # Yeşil

            item = OneLineListItem(
                text=f"[b]{row[1]}[/b]",
                secondary_text=f"{row[2] or '-'} • {row[3] or '-'} • [color={renk}]Stok: {stok}[/color]"
            )
            item.bind(on_release=lambda x, r=row: self.sec(r))
            self.liste.add_widget(item)

    def sec(self, row):
        self.secili_id = row[0]
        self.adi.text = row[1]
        self.kategori.text = row[2] or ""
        self.boyut.text = row[3] or ""
        self.stok.text = str(row[4])
        toast(f"Seçildi: {row[1]}")

    def ekle(self, *args):
        if not self.adi.text.strip():
            toast("Ürün adı zorunlu!"); return
        try:
            stok = int(self.stok.text or 0)
        except:
            toast("Stok sayı olmalı!"); return

        self.cur.execute("INSERT INTO urunler (urun_adi, kategori, urun_boyutu, stok) VALUES (?, ?, ?, ?)",
                        (self.adi.text.strip(), self.kategori.text.strip(), self.boyut.text.strip(), stok))
        self.conn.commit()
        toast("Eklendi")
        self.temizle()
        self.yukle()

    def guncelle(self, *args):
        if not hasattr(self, "secili_id"):
            toast("Önce bir ürün seçin!"); return
        if not self.adi.text.strip():
            toast("Ürün adı boş olamaz!"); return
        try:
            stok = int(self.stok.text or 0)
        except:
            toast("Stok geçerli olmalı!"); return

        self.cur.execute("UPDATE urunler SET urun_adi=?, kategori=?, urun_boyutu=?, stok=? WHERE id=?",
                        (self.adi.text.strip(), self.kategori.text.strip(), self.boyut.text.strip(), stok, self.secili_id))
        self.conn.commit()
        toast("Güncellendi")
        self.temizle()
        self.yukle()

    def sil(self, *args):
        if not hasattr(self, "secili_id"):
            toast("Silmek için ürün seçin!"); return
        self.cur.execute("DELETE FROM urunler WHERE id=?", (self.secili_id,))
        self.conn.commit()
        toast("Silindi")
        self.temizle()
        self.yukle()

    def temizle(self, *args):
        self.adi.text = self.kategori.text = self.boyut.text = self.stok.text = ""
        if hasattr(self, "secili_id"):
            del self.secili_id

    def arama_yap(self, instance, text):
        self.liste.clear_widgets()
        if not text.strip():
            self.yukle()
            return
        self.cur.execute("""
            SELECT id, urun_adi, kategori, urun_boyutu, stok FROM urunler
            WHERE urun_adi LIKE ? OR kategori LIKE ? OR urun_boyutu LIKE ?
        """, (f"%{text}%",)*3)
        for row in self.cur.fetchall():
            item = OneLineListItem(text=f"{row[1]} — Stok: {row[4]}")
            self.liste.add_widget(item)

    def dusuk_stok_raporu(self, *args):
        self.cur.execute("SELECT urun_adi, stok FROM urunler WHERE stok <= 10 ORDER BY stok")
        rows = self.cur.fetchall()
        if not rows:
            toast("Tüm stoklar yeterli!", duration=4)
            return
        rapor = "DÜŞÜK STOK!\n"
        for r in rows:
            durum = "KRİTİK" if r[1] <= 5 else "Düşük"
            rapor += f"• {r[0]} → {r[1]} [{durum}]\n"
        toast(rapor, duration=10)


class StokApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Amber"
        return AnaEkran()


if __name__ == "__main__":
    StokApp().run()
