#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import os
from datetime import datetime
try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                                 QHBoxLayout, QLabel, QLineEdit, QPushButton,
                                 QScrollArea, QFrame, QMessageBox, QFileDialog,
                                 QGridLayout, QGroupBox, QDialog)
    from PyQt5.QtCore import Qt, QTimer
    from PyQt5.QtGui import QFont, QPalette, QColor
except ImportError:
    print("PyQt5 is not installed. Please install it using: pip install PyQt5")
    sys.exit(1)

class KuyumcuKasaSayim(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kuyumcu Günlük Kasa Sayım Programı")
        self.setGeometry(100, 100, 1400, 900)
        
        # Veri yapısı
        self.kalemler = {
            "22 Ayar Tel Bilezik (gram)": {"birim": "gram", "degerler": [0, 0, 0, 0, 0], "toplam": 0, "olması_gereken": 0},
            "Çeyrek Lira (adet)": {"birim": "adet", "degerler": [0, 0, 0, 0, 0], "toplam": 0, "olması_gereken": 0},
            "Yarım Lira (adet)": {"birim": "adet", "degerler": [0, 0, 0, 0, 0], "toplam": 0, "olması_gereken": 0},
            "Zinet Lira (adet)": {"birim": "adet", "degerler": [0, 0, 0, 0, 0], "toplam": 0, "olması_gereken": 0},
            "Ata Lira (adet)": {"birim": "adet", "degerler": [0, 0, 0, 0, 0], "toplam": 0, "olması_gereken": 0},
            "Gramse (adet)": {"birim": "adet", "degerler": [0, 0, 0, 0, 0], "toplam": 0, "olması_gereken": 0},
            "Yarım Beşli (adet)": {"birim": "adet", "degerler": [0, 0, 0, 0, 0], "toplam": 0, "olması_gereken": 0},
            "Beşli (adet)": {"birim": "adet", "degerler": [0, 0, 0, 0, 0], "toplam": 0, "olması_gereken": 0},
            "24 Ayar Has Altın (gram)": {"birim": "gram", "degerler": [0, 0, 0, 0, 0], "toplam": 0, "olması_gereken": 0},
            "22 Ayar Hurda (gram)": {"birim": "gram", "degerler": [0, 0, 0, 0, 0], "toplam": 0, "olması_gereken": 0},
            "18 Ayar Hurda (gram)": {"birim": "gram", "degerler": [0, 0, 0, 0, 0], "toplam": 0, "olması_gereken": 0},
            "14 Ayar Hurda (gram)": {"birim": "gram", "degerler": [0, 0, 0, 0, 0], "toplam": 0, "olması_gereken": 0},
            "Türk Lirası (TL)": {"birim": "TL", "degerler": [0, 0, 0, 0, 0], "toplam": 0, "olması_gereken": 0},
            "Dolar ($)": {"birim": "$", "degerler": [0, 0, 0, 0, 0], "toplam": 0, "olması_gereken": 0},
            "Euro (€)": {"birim": "€", "degerler": [0, 0, 0, 0, 0], "toplam": 0, "olması_gereken": 0}
        }
        
        self.entry_widgets = {}
        self.toplam_labels = {}
        self.fark_labels = {}
        
        self.init_ui()
        
    def init_ui(self):
        # Ana widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Ana layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Başlık frame
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-radius: 15px;
                margin: 10px;
            }
        """)
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(30, 20, 30, 20)
        
        # Ana başlık
        title_label = QLabel("KUYUMCU GÜNLÜK KASA SAYIM PROGRAMI")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: transparent;
                padding: 10px;
                margin-bottom: 5px;
            }
        """)
        title_layout.addWidget(title_label)
        
        # Tarih
        date_label = QLabel(f"Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        date_label.setAlignment(Qt.AlignCenter)
        date_label.setFont(QFont("Arial", 14, QFont.Bold))
        date_label.setStyleSheet("""
            QLabel {
                color: #bdc3c7;
                background-color: transparent;
                padding: 5px;
            }
        """)
        title_layout.addWidget(date_label)
        
        main_layout.addWidget(title_frame)
        
        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Scroll içerik widget
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(15)
        
        # Kalemler için widget'ları oluştur
        for kalem_adi, kalem_data in self.kalemler.items():
            self.create_kalem_widget(scroll_layout, kalem_adi, kalem_data)
        
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)
        
        # Butonlar frame
        button_frame = QFrame()
        button_frame.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 15px;
                margin: 10px;
            }
        """)
        button_frame.setFixedHeight(100)
        
        button_inner_layout = QHBoxLayout(button_frame)
        button_inner_layout.setContentsMargins(20, 15, 20, 15)
        button_inner_layout.setSpacing(15)
        
        # Butonlar
        buttons = [
            ("TOPLAMLARI HESAPLA", self.hesapla_toplamlar, "#3498db"),
            ("KAYDET", self.kaydet_veri, "#27ae60"),
            ("YÜKLE", self.yukle_veri, "#e67e22"),
            ("RAPOR", self.rapor_goster, "#9b59b6"),
            ("TEMİZLE", self.temizle_veri, "#e74c3c")
        ]
        
        for text, command, color in buttons:
            btn = QPushButton(text)
            btn.setFont(QFont("Arial", 13, QFont.Bold))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    padding: 18px 30px;
                    border-radius: 10px;
                    font-size: 13px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {self.darken_color(color)};
                }}
                QPushButton:pressed {{
                    background-color: {self.darken_color(color, 0.8)};
                }}
            """)
            btn.clicked.connect(command)
            button_inner_layout.addWidget(btn)
        
        main_layout.addWidget(button_frame)
        
        # Stil ayarları
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QScrollArea {
                border: none;
                background-color: #f5f5f5;
            }
        """)
        
    def create_kalem_widget(self, parent_layout, kalem_adi, kalem_data):
        # Grup kutusu
        group_box = QGroupBox()
        group_box.setFont(QFont("Arial", 14, QFont.Bold))
        group_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 3px solid #34495e;
                border-radius: 15px;
                margin-top: 15px;
                padding-top: 20px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 15px 0 15px;
                color: #2c3e50;
                background-color: white;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        
        # Başlık label'ı
        title_label = QLabel(kalem_adi)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                background-color: white;
                padding: 5px 15px;
                border: 2px solid #34495e;
                border-radius: 8px;
                margin: 10px;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        
        group_layout = QVBoxLayout(group_box)
        group_layout.setSpacing(15)
        group_layout.setContentsMargins(20, 20, 20, 20)
        
        # Başlık label'ını ekle
        group_layout.addWidget(title_label)
        
        # Giriş alanları başlığı
        entries_title = QLabel("Sayım Değerleri:")
        entries_title.setFont(QFont("Arial", 12, QFont.Bold))
        entries_title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                background-color: transparent;
                padding: 5px;
                margin-bottom: 10px;
            }
        """)
        group_layout.addWidget(entries_title)
        
        # Giriş alanları
        entries_layout = QHBoxLayout()
        entries_layout.setSpacing(10)
        
        self.entry_widgets[kalem_adi] = []
        for i in range(5):
            entry_layout = QVBoxLayout()
            
            label = QLabel(f"{i+1}.")
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Arial", 10, QFont.Bold))
            label.setStyleSheet("color: #7f8c8d; margin-bottom: 5px;")
            entry_layout.addWidget(label)
            
            entry = QLineEdit()
            entry.setPlaceholderText("0.00")
            entry.setAlignment(Qt.AlignCenter)
            entry.setFont(QFont("Arial", 11))
            entry.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #bdc3c7;
                    border-radius: 5px;
                    padding: 8px;
                    background-color: white;
                    color: #2c3e50;
                    font-size: 12px;
                    font-weight: bold;
                }
                QLineEdit:focus {
                    border-color: #3498db;
                    background-color: #f8f9fa;
                    color: #2c3e50;
                }
                QLineEdit:hover {
                    border-color: #3498db;
                    background-color: #f8f9fa;
                }
            """)
            entry.textChanged.connect(lambda _, k=kalem_adi: self.hesapla_kalem_toplami(k))
            entry_layout.addWidget(entry)
            
            self.entry_widgets[kalem_adi].append(entry)
            entries_layout.addLayout(entry_layout)
        
        group_layout.addLayout(entries_layout)
        
        # Toplam ve fark başlığı
        totals_title = QLabel("Hesaplamalar:")
        totals_title.setFont(QFont("Arial", 12, QFont.Bold))
        totals_title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                background-color: transparent;
                padding: 5px;
                margin: 15px 0 10px 0;
            }
        """)
        group_layout.addWidget(totals_title)
        
        # Toplam, olması gereken ve fark
        totals_layout = QHBoxLayout()
        totals_layout.setSpacing(30)
        
        # Toplam
        toplam_container = QVBoxLayout()
        toplam_label = QLabel("Toplam:")
        toplam_label.setFont(QFont("Arial", 11, QFont.Bold))
        toplam_label.setStyleSheet("color: #2c3e50; margin-bottom: 5px;")
        toplam_container.addWidget(toplam_label)
        
        toplam_value = QLabel("0")
        toplam_value.setAlignment(Qt.AlignCenter)
        toplam_value.setFont(QFont("Arial", 12, QFont.Bold))
        toplam_value.setStyleSheet("""
            QLabel {
                background-color: #e8f5e8;
                border: 2px solid #27ae60;
                border-radius: 5px;
                padding: 10px;
                color: #2c3e50;
                font-weight: bold;
            }
        """)
        toplam_container.addWidget(toplam_value)
        self.toplam_labels[kalem_adi] = toplam_value
        totals_layout.addLayout(toplam_container)
        
        # Olması gereken
        olmasi_container = QVBoxLayout()
        olmasi_label = QLabel("Olması Gereken:")
        olmasi_label.setFont(QFont("Arial", 11, QFont.Bold))
        olmasi_label.setStyleSheet("color: #2c3e50; margin-bottom: 5px;")
        olmasi_container.addWidget(olmasi_label)
        
        olmasi_entry = QLineEdit()
        olmasi_entry.setPlaceholderText("0.00")
        olmasi_entry.setAlignment(Qt.AlignCenter)
        olmasi_entry.setFont(QFont("Arial", 11))
        olmasi_entry.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 10px;
                background-color: white;
                color: #2c3e50;
                font-size: 12px;
                font-weight: bold;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #f8f9fa;
                color: #2c3e50;
            }
            QLineEdit:hover {
                border-color: #3498db;
                background-color: #f8f9fa;
            }
        """)
        olmasi_entry.textChanged.connect(lambda _, k=kalem_adi: self.hesapla_fark(k))
        olmasi_container.addWidget(olmasi_entry)
        kalem_data['olmasi_entry'] = olmasi_entry
        totals_layout.addLayout(olmasi_container)
        
        # Fark
        fark_container = QVBoxLayout()
        fark_label = QLabel("Fark:")
        fark_label.setFont(QFont("Arial", 11, QFont.Bold))
        fark_label.setStyleSheet("color: #2c3e50; margin-bottom: 5px;")
        fark_container.addWidget(fark_label)
        
        fark_value = QLabel("0")
        fark_value.setAlignment(Qt.AlignCenter)
        fark_value.setFont(QFont("Arial", 12, QFont.Bold))
        fark_value.setStyleSheet("""
            QLabel {
                background-color: #fff3cd;
                border: 2px solid #ffc107;
                border-radius: 5px;
                padding: 10px;
                color: #2c3e50;
                font-weight: bold;
            }
        """)
        fark_container.addWidget(fark_value)
        self.fark_labels[kalem_adi] = fark_value
        totals_layout.addLayout(fark_container)
        
        group_layout.addLayout(totals_layout)
        parent_layout.addWidget(group_box)
        
    def darken_color(self, color, factor=0.9):
        """Rengi koyulaştır"""
        color_map = {
            "#3498db": "#2980b9",
            "#27ae60": "#229954",
            "#e67e22": "#d35400",
            "#e74c3c": "#c0392b",
            "#9b59b6": "#8e44ad"
        }
        return color_map.get(color, color)
    
    def validate_number(self, text):
        """Sayısal girişi doğrula"""
        if not text.strip():
            return True, 0.0  # Boş giriş geçerli
        
        try:
            # Virgülü nokta ile değiştir (Türkçe format için)
            text = text.replace(',', '.')
            value = float(text)
            if value < 0:
                return False, 0.0
            return True, value
        except ValueError:
            return False, 0.0
        
    def hesapla_kalem_toplami(self, kalem_adi):
        try:
            toplam = 0
            for entry in self.entry_widgets[kalem_adi]:
                text = entry.text().strip()
                if text:
                    is_valid, value = self.validate_number(text)
                    if is_valid:
                        toplam += value
                        # Geçerli giriş için normal stil
                        entry.setStyleSheet("""
                            QLineEdit {
                                border: 2px solid #bdc3c7;
                                border-radius: 5px;
                                padding: 8px;
                                background-color: white;
                                color: #2c3e50;
                                font-size: 12px;
                                font-weight: bold;
                            }
                            QLineEdit:focus {
                                border-color: #3498db;
                                background-color: #f8f9fa;
                                color: #2c3e50;
                            }
                            QLineEdit:hover {
                                border-color: #3498db;
                                background-color: #f8f9fa;
                            }
                        """)
                    else:
                        # Geçersiz giriş için uyarı
                        entry.setStyleSheet("""
                            QLineEdit {
                                border: 2px solid #e74c3c;
                                border-radius: 5px;
                                padding: 8px;
                                background-color: #fdf2f2;
                                color: #e74c3c;
                                font-size: 12px;
                                font-weight: bold;
                            }
                        """)
                        return  # Hesaplamayı durdur
            
            self.kalemler[kalem_adi]['toplam'] = toplam
            
            # Gram olanlar için ondalık, TL için binlik ayırıcı, diğerleri için tam sayı
            if "gram" in kalem_adi.lower():
                toplam_text = f"{toplam:.2f}"
            elif "türk lirası" in kalem_adi.lower() or "tl" in kalem_adi.lower():
                toplam_text = f"{int(toplam):,}".replace(",", ".")
            else:
                toplam_text = f"{int(toplam)}"
            
            self.toplam_labels[kalem_adi].setText(toplam_text)
            self.hesapla_fark(kalem_adi)
            
        except ValueError:
            pass
    
    def hesapla_fark(self, kalem_adi):
        try:
            toplam = self.kalemler[kalem_adi]['toplam']
            olmasi_text = self.kalemler[kalem_adi]['olmasi_entry'].text().strip()
            
            if olmasi_text:
                is_valid, olmasi_deger = self.validate_number(olmasi_text)
                if not is_valid:
                    # Geçersiz giriş için uyarı
                    self.kalemler[kalem_adi]['olmasi_entry'].setStyleSheet("""
                        QLineEdit {
                            border: 2px solid #e74c3c;
                            border-radius: 5px;
                            padding: 10px;
                            background-color: #fdf2f2;
                            color: #e74c3c;
                            font-size: 12px;
                            font-weight: bold;
                        }
                    """)
                    return
                else:
                    # Geçerli giriş için normal stil
                    self.kalemler[kalem_adi]['olmasi_entry'].setStyleSheet("""
                        QLineEdit {
                            border: 2px solid #bdc3c7;
                            border-radius: 5px;
                            padding: 10px;
                            background-color: white;
                            color: #2c3e50;
                            font-size: 12px;
                            font-weight: bold;
                        }
                        QLineEdit:focus {
                            border-color: #3498db;
                            background-color: #f8f9fa;
                            color: #2c3e50;
                        }
                        QLineEdit:hover {
                            border-color: #3498db;
                            background-color: #f8f9fa;
                        }
                    """)
                fark = toplam - olmasi_deger
                
                # Gram olanlar için ondalık, TL için binlik ayırıcı, diğerleri için tam sayı
                if "gram" in kalem_adi.lower():
                    if fark > 0:
                        fark_text = f"+{fark:.2f}"
                    elif fark < 0:
                        fark_text = f"{fark:.2f}"
                    else:
                        fark_text = "0.00"
                elif "türk lirası" in kalem_adi.lower() or "tl" in kalem_adi.lower():
                    if fark > 0:
                        fark_text = f"+{int(fark):,}".replace(",", ".")
                    elif fark < 0:
                        fark_text = f"{int(fark):,}".replace(",", ".")
                    else:
                        fark_text = "0"
                else:
                    if fark > 0:
                        fark_text = f"+{int(fark)}"
                    elif fark < 0:
                        fark_text = f"{int(fark)}"
                    else:
                        fark_text = "0"
                
                if fark > 0:
                    fark_color = "#27ae60"  # Yeşil
                elif fark < 0:
                    fark_color = "#e74c3c"  # Kırmızı
                else:
                    fark_color = "#2c3e50"  # Siyah
                
                self.fark_labels[kalem_adi].setText(fark_text)
                if fark > 0:
                    bg_color = "#d4edda"
                    border_color = "#27ae60"
                elif fark < 0:
                    bg_color = "#f8d7da"
                    border_color = "#e74c3c"
                else:
                    bg_color = "#d1ecf1"
                    border_color = "#17a2b8"
                
                self.fark_labels[kalem_adi].setStyleSheet(f"""
                    QLabel {{
                        background-color: {bg_color};
                        border: 2px solid {border_color};
                        border-radius: 5px;
                        padding: 10px;
                        color: {fark_color};
                        font-weight: bold;
                    }}
                """)
            else:
                # Gram olanlar için ondalık, TL için binlik ayırıcı, diğerleri için tam sayı
                if "gram" in kalem_adi.lower():
                    default_text = "0.00"
                elif "türk lirası" in kalem_adi.lower() or "tl" in kalem_adi.lower():
                    default_text = "0"
                else:
                    default_text = "0"
                
                self.fark_labels[kalem_adi].setText(default_text)
                self.fark_labels[kalem_adi].setStyleSheet("""
                    QLabel {
                        background-color: #fff3cd;
                        border: 2px solid #ffc107;
                        border-radius: 5px;
                        padding: 10px;
                        color: #2c3e50;
                        font-weight: bold;
                    }
                """)
                
        except ValueError:
            self.fark_labels[kalem_adi].setText("Hata")
            self.fark_labels[kalem_adi].setStyleSheet("""
                QLabel {
                    background-color: #f8d7da;
                    border: 2px solid #e74c3c;
                    border-radius: 5px;
                    padding: 10px;
                    color: #e74c3c;
                    font-weight: bold;
                }
            """)
    
    def hesapla_toplamlar(self):
        for kalem_adi in self.kalemler:
            self.hesapla_kalem_toplami(kalem_adi)
        QMessageBox.information(self, "Başarılı", "Tüm toplamlar hesaplandı!")
    
    def kaydet_veri(self):
        try:
            kayit_verisi = {
                'tarih': datetime.now().strftime('%d.%m.%Y %H:%M'),
                'kalemler': {}
            }
            
            for kalem_adi, kalem_data in self.kalemler.items():
                degerler = []
                for entry in self.entry_widgets[kalem_adi]:
                    text = entry.text().strip()
                    degerler.append(float(text) if text else 0)
                
                olmasi_text = kalem_data['olmasi_entry'].text().strip()
                
                kayit_verisi['kalemler'][kalem_adi] = {
                    'degerler': degerler,
                    'toplam': kalem_data['toplam'],
                    'olmasi_gereken': float(olmasi_text) if olmasi_text else 0
                }
            
            dosya_adi = f"kasa_sayim_{datetime.now().strftime('%d.%m.%Y_%H-%M')}.json"
            
            with open(dosya_adi, 'w', encoding='utf-8') as f:
                json.dump(kayit_verisi, f, ensure_ascii=False, indent=2)
            
            QMessageBox.information(self, "Başarılı", f"Veriler kaydedildi: {dosya_adi}")
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kaydetme sırasında hata oluştu: {str(e)}")
    
    def yukle_veri(self):
        try:
            dosya_yolu, _ = QFileDialog.getOpenFileName(
                self, "Kayıtlı Veriyi Seç", "", "JSON dosyaları (*.json);;Tüm dosyalar (*.*)"
            )
            
            if dosya_yolu:
                with open(dosya_yolu, 'r', encoding='utf-8') as f:
                    veri = json.load(f)
                
                for kalem_adi, kalem_verisi in veri['kalemler'].items():
                    if kalem_adi in self.kalemler:
                        for i, deger in enumerate(kalem_verisi['degerler']):
                            if i < len(self.entry_widgets[kalem_adi]):
                                self.entry_widgets[kalem_adi][i].setText(str(deger) if deger > 0 else "")
                        
                        olmasi_entry = self.kalemler[kalem_adi]['olmasi_entry']
                        olmasi_entry.setText(str(kalem_verisi['olmasi_gereken']) if kalem_verisi['olmasi_gereken'] > 0 else "")
                
                self.hesapla_toplamlar()
                QMessageBox.information(self, "Başarılı", f"Veriler yüklendi: {veri.get('tarih', 'Bilinmeyen tarih')}")
                
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Yükleme sırasında hata oluştu: {str(e)}")
    
    def temizle_veri(self):
        reply = QMessageBox.question(self, "Onay", "Tüm verileri temizlemek istediğinizden emin misiniz?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            for kalem_adi in self.kalemler:
                for entry in self.entry_widgets[kalem_adi]:
                    entry.clear()
                
                self.kalemler[kalem_adi]['olmasi_entry'].clear()
                # Gram olanlar için ondalık, TL için binlik ayırıcı, diğerleri için tam sayı
                if "gram" in kalem_adi.lower():
                    default_toplam = "0.00"
                    default_fark = "0.00"
                elif "türk lirası" in kalem_adi.lower() or "tl" in kalem_adi.lower():
                    default_toplam = "0"
                    default_fark = "0"
                else:
                    default_toplam = "0"
                    default_fark = "0"
                
                self.toplam_labels[kalem_adi].setText(default_toplam)
                self.fark_labels[kalem_adi].setText(default_fark)
                self.fark_labels[kalem_adi].setStyleSheet("""
                    QLabel {
                        background-color: #fff3cd;
                        border: 2px solid #ffc107;
                        border-radius: 5px;
                        padding: 10px;
                        color: #2c3e50;
                        font-weight: bold;
                    }
                """)
                
                self.kalemler[kalem_adi]['degerler'] = [0, 0, 0, 0, 0]
                self.kalemler[kalem_adi]['toplam'] = 0
                self.kalemler[kalem_adi]['olması_gereken'] = 0
            
            QMessageBox.information(self, "Başarılı", "Tüm veriler temizlendi!")
    
    def rapor_goster(self):
        """Rapor penceresi göster"""
        try:
            rapor_pencere = QDialog(self)
            rapor_pencere.setWindowTitle("Kasa Sayım Raporu")
            rapor_pencere.setModal(True)
            rapor_pencere.resize(1200, 800)
        
            # Layout
            layout = QVBoxLayout(rapor_pencere)
            layout.setSpacing(10)
            layout.setContentsMargins(20, 20, 20, 20)
        
            # Başlık
            baslik = QLabel("KUYUMCU KASA SAYIM RAPORU")
            baslik.setAlignment(Qt.AlignCenter)
            baslik.setFont(QFont("Arial", 16, QFont.Bold))
            baslik.setStyleSheet("""
                QLabel {
                    background-color: #2c3e50;
                    color: white;
                    padding: 15px;
                    border-radius: 10px;
                    margin-bottom: 10px;
                }
            """)
            layout.addWidget(baslik)
            
            # Tarih
            tarih_label = QLabel(f"Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
            tarih_label.setAlignment(Qt.AlignCenter)
            tarih_label.setFont(QFont("Arial", 12, QFont.Bold))
            tarih_label.setStyleSheet("color: #7f8c8d; margin-bottom: 15px;")
            layout.addWidget(tarih_label)
        
            # Scroll area
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            
            # Scroll içerik
            scroll_widget = QWidget()
            scroll_layout = QVBoxLayout(scroll_widget)
            scroll_layout.setSpacing(5)
            
            # Her kalem için rapor - kompakt görünüm
            for kalem_adi, kalem_data in self.kalemler.items():
                # Tek satır rapor
                rapor_frame = QFrame()
                rapor_frame.setStyleSheet("""
                    QFrame {
                        background-color: white;
                        border: 1px solid #bdc3c7;
                        border-radius: 5px;
                        margin: 2px;
                    }
                """)
                rapor_layout = QHBoxLayout(rapor_frame)
                rapor_layout.setContentsMargins(10, 8, 10, 8)
                rapor_layout.setSpacing(15)
                
                # Kalem adı
                kalem_label = QLabel(kalem_adi)
                kalem_label.setFont(QFont("Arial", 11, QFont.Bold))
                kalem_label.setStyleSheet("color: #2c3e50;")
                kalem_label.setFixedWidth(200)
                rapor_layout.addWidget(kalem_label)
                
                # Mevcut
                mevcut_label = QLabel("Mevcut:")
                mevcut_label.setFont(QFont("Arial", 10, QFont.Bold))
                mevcut_label.setStyleSheet("color: #2c3e50;")
                mevcut_label.setFixedWidth(60)
                rapor_layout.addWidget(mevcut_label)
                
                # Gram olanlar için ondalık, TL için binlik ayırıcı, diğerleri için tam sayı
                if "gram" in kalem_adi.lower():
                    mevcut_deger = f"{kalem_data['toplam']:.2f}"
                elif "türk lirası" in kalem_adi.lower() or "tl" in kalem_adi.lower():
                    mevcut_deger = f"{int(kalem_data['toplam']):,}".replace(",", ".")
                else:
                    mevcut_deger = f"{int(kalem_data['toplam'])}"
                
                mevcut_value = QLabel(mevcut_deger)
                mevcut_value.setFont(QFont("Arial", 10, QFont.Bold))
                mevcut_value.setStyleSheet("""
                    QLabel {
                        background-color: #e8f5e8;
                        border: 1px solid #27ae60;
                        border-radius: 3px;
                        padding: 4px 8px;
                        color: #2c3e50;
                    }
                """)
                mevcut_value.setFixedWidth(100)
                rapor_layout.addWidget(mevcut_value)
                
                # Olması gereken
                olmasi_label = QLabel("Olması Gereken:")
                olmasi_label.setFont(QFont("Arial", 10, QFont.Bold))
                olmasi_label.setStyleSheet("color: #2c3e50;")
                olmasi_label.setFixedWidth(80)
                rapor_layout.addWidget(olmasi_label)
                
                olmasi_text = kalem_data['olmasi_entry'].text().strip()
                if olmasi_text:
                    olmasi_deger = float(olmasi_text)
                    if "gram" in kalem_adi.lower():
                        olmasi_display = f"{olmasi_deger:.2f}"
                    elif "türk lirası" in kalem_adi.lower() or "tl" in kalem_adi.lower():
                        olmasi_display = f"{int(olmasi_deger):,}".replace(",", ".")
                    else:
                        olmasi_display = f"{int(olmasi_deger)}"
                else:
                    if "gram" in kalem_adi.lower():
                        olmasi_display = "0.00"
                    elif "türk lirası" in kalem_adi.lower() or "tl" in kalem_adi.lower():
                        olmasi_display = "0"
                    else:
                        olmasi_display = "0"
                
                olmasi_value = QLabel(olmasi_display)
                olmasi_value.setFont(QFont("Arial", 10, QFont.Bold))
                olmasi_value.setStyleSheet("""
                    QLabel {
                        background-color: #fff3cd;
                        border: 1px solid #ffc107;
                        border-radius: 3px;
                        padding: 4px 8px;
                        color: #2c3e50;
                    }
                """)
                olmasi_value.setFixedWidth(100)
                rapor_layout.addWidget(olmasi_value)
                
                # Fark
                fark_label = QLabel("Fark:")
                fark_label.setFont(QFont("Arial", 10, QFont.Bold))
                fark_label.setStyleSheet("color: #2c3e50;")
                fark_label.setFixedWidth(40)
                rapor_layout.addWidget(fark_label)
                
                # Fark hesaplama
                if olmasi_text:
                    olmasi_deger = float(olmasi_text)
                    fark = kalem_data['toplam'] - olmasi_deger
                    
                    if "gram" in kalem_adi.lower():
                        if fark > 0:
                            fark_display = f"+{fark:.2f}"
                        elif fark < 0:
                            fark_display = f"{fark:.2f}"
                        else:
                            fark_display = "0.00"
                    elif "türk lirası" in kalem_adi.lower() or "tl" in kalem_adi.lower():
                        if fark > 0:
                            fark_display = f"+{int(fark):,}".replace(",", ".")
                        elif fark < 0:
                            fark_display = f"{int(fark):,}".replace(",", ".")
                        else:
                            fark_display = "0"
                    else:
                        if fark > 0:
                            fark_display = f"+{int(fark)}"
                        elif fark < 0:
                            fark_display = f"{int(fark)}"
                        else:
                            fark_display = "0"
                    
                    if fark > 0:
                        fark_color = "#d4edda"
                        fark_border = "#27ae60"
                        fark_text_color = "#27ae60"
                    elif fark < 0:
                        fark_color = "#f8d7da"
                        fark_border = "#e74c3c"
                        fark_text_color = "#e74c3c"
                    else:
                        fark_color = "#d1ecf1"
                        fark_border = "#17a2b8"
                        fark_text_color = "#17a2b8"
                else:
                    if "gram" in kalem_adi.lower():
                        fark_display = "0.00"
                    elif "türk lirası" in kalem_adi.lower() or "tl" in kalem_adi.lower():
                        fark_display = "0"
                    else:
                        fark_display = "0"
                    fark_color = "#fff3cd"
                    fark_border = "#ffc107"
                    fark_text_color = "#2c3e50"
                
                fark_value = QLabel(fark_display)
                fark_value.setFont(QFont("Arial", 10, QFont.Bold))
                fark_value.setStyleSheet(f"""
                    QLabel {{
                        background-color: {fark_color};
                        border: 1px solid {fark_border};
                        border-radius: 3px;
                        padding: 4px 8px;
                        color: {fark_text_color};
                    }}
                """)
                fark_value.setFixedWidth(100)
                rapor_layout.addWidget(fark_value)
                
                scroll_layout.addWidget(rapor_frame)
            
            scroll_area.setWidget(scroll_widget)
            layout.addWidget(scroll_area)
            
            # Kapat butonu
            kapat_btn = QPushButton("KAPAT")
            kapat_btn.setFont(QFont("Arial", 12, QFont.Bold))
            kapat_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    padding: 15px 30px;
                    border-radius: 8px;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            kapat_btn.clicked.connect(rapor_pencere.close)
            layout.addWidget(kapat_btn)
        
            # Pencereyi göster
            rapor_pencere.exec_()
            
        except Exception as e:
            error_msg = f"Rapor penceresi açılırken hata oluştu: {str(e)}"
            print(f"HATA: {error_msg}")  # Terminal'e hata mesajını yazdır
            QMessageBox.critical(self, "Hata", error_msg)

def main():
    app = QApplication(sys.argv)
    
    # Uygulama ayarları
    app.setApplicationName("Kuyumcu Kasa Sayım")
    app.setApplicationVersion("1.0")
    
    # Ana pencere
    window = KuyumcuKasaSayim()
    window.show()
    
    # Pencereyi öne getir
    window.raise_()
    window.activateWindow()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
