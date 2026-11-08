# 🚀 Cross-Platform PNG & WebP Optimizer

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![macOS](https://img.shields.io/badge/Platform-macOS-lightgrey?style=for-the-badge&logo=apple)
![Windows](https://img.shields.io/badge/Platform-Windows-blue?style=for-the-badge&logo=windows)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

Web geliştiricileri ve içerik üreticileri için **Python (`CustomTkinter` & `Pillow`)** ile geliştirilmiş, **Sürükle-Bırak (Drag & Drop)** destekli, modern karanlık temalı (Dark Mode) masaüstü görsel sıkıştırma ve WebP dönüştürme uygulaması.

TinyPNG mantığıyla çalışan **8-bit Renk Kuantizasyonu (Color Quantization)** algoritması sayesinde PNG görsellerin şeffaflığını (alpha channel) bozmadan dosya boyutlarını **%70 ila %80 oranında** küçültür.

---

## ✨ Özellikler (Features)

* **📥 Sürükle ve Bırak (Drag & Drop):** Tek tek görselleri veya yüzlerce fotoğraf içeren bir klasörü doğrudan pencereye bırakın.
* **🎨 Akıllı 8-Bit PNG Sıkıştırma:** Şeffaf katmanı koruyarak renk uzayını optimize eder, gözle görülür kayıp olmadan dosya boyutunu düşürür.
* **🌐 WebP Dönüştürücü:** Web sitelerinde maksimum Core Web Vitals skoru için tek tıkla `.webp` çıktısı alır.
* **⚡ Donmayan Arayüz (Multi-threaded):** Arka plan iş parçacığı sayesinde toplu işlemlerde arayüz kilitlenmez, anlık ilerleme çubuğu ve log akışı sunar.
* **🛡️ Orijinal Dosyaları Korur:** İşlenen görselleri kaynak dizin içindeki `compressed_images` klasörüne aktarır ve işlem bitince klasörü dosya yöneticisinde (Finder / Dosya Gezgini) otomatik açar.

---

## 🛠️ Kurulum (Installation)

Projeyi bilgisayarınıza klonlayın ve proje dizinine geçin:

```bash
git clone https://github.com/erdemozturk52/mac-png-webp-optimizer.git
cd mac-png-webp-optimizer
```

Gerekli bağımlılıkları yükleyin:

```bash
pip install -r requirements.txt
```

> **macOS Notu:** Sisteminizde birden fazla Python sürümü varsa `pip3` ve `python3` komutlarını tercih ediniz.

---

## 🚀 Çalıştırma (Usage)

Uygulamayı başlatmak için terminal veya komut satırında şu komutu çalıştırın:

* **macOS:**
  ```bash
  python3 compressor.py
  ```

* **Windows:**
  ```cmd
  python compressor.py
  ```

---

## 📦 Bağımsız Masaüstü Uygulaması Olarak Derleme (Build Standalone App)

Terminal kullanmadan doğrudan çift tıklamayla açabileceğiniz bir uygulama oluşturmak için **PyInstaller** adımlarını izleyebilirsiniz.

### 🍎 macOS (`.app` Oluşturma)

Terminalde şu komutu çalıştırın:

```bash
pyinstaller --noconfirm --onedir --windowed \
--collect-all customtkinter \
--collect-all tkinterdnd2 \
--name "PNG Optimizer" compressor.py
```

* Derleme tamamlandığında `dist/PNG Optimizer.app` dosyasını **Masaüstüne** veya **Applications (Uygulamalar)** klasörüne sürükleyip kullanabilirsiniz.

---

### 🪟 Windows (`.exe` Oluşturma)

Komut İstemi (CMD) veya PowerShell üzerinden şu komutu çalıştırın:

```cmd
pyinstaller --noconfirm --onedir --windowed ^
--collect-all customtkinter ^
--collect-all tkinterdnd2 ^
--name "PNG Optimizer" compressor.py
```

* Derleme tamamlandığında `dist/PNG Optimizer/PNG Optimizer.exe` dosyasını çalıştırabilirsiniz.

---

## 📊 Sıkıştırma Performansı

| Yöntem | Açıklama | Ortalama Tasarruf |
| :--- | :--- | :--- |
| **8-Bit Quantization** | RGBA kanallarını koruyarak renk paletini optimize eder (`method=2` Fast Octree). | **%60 - %80** |
| **WebP Conversion** | Görseli modern WebP algoritmasıyla (`method=6`) yeniden kodlar. | **%70 - %90** |

---

## 📄 Lisans (License)

Bu proje [MIT Lisansı](LICENSE) kapsamında lisanslanmıştır. Dilediğiniz gibi kullanabilir, özelleştirebilir ve dağıtabilirsiniz.
