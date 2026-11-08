import os
import threading
from tkinter import filedialog, messagebox
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image

# Görünüm Ayarları
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class TkDnDCTk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


class ImageCompressorApp(TkDnDCTk):

    def __init__(self):
        super().__init__()

        self.title("PNG & WebP Optimizer")
        self.geometry("720x560")
        self.minsize(650, 500)
        self.resizable(True, True)

        self.selected_files = []

        # --- Başlık ---
        self.title_label = ctk.CTkLabel(
            self,
            text="Görsel Boyut Küçültücü",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        self.title_label.pack(pady=(12, 2))

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Web siten için PNG görsellerini hızla optimize et",
            text_color="gray",
        )
        self.subtitle_label.pack(pady=(0, 8))

        # --- Sürükle & Bırak ve Aksiyon Butonları ---
        self.drop_frame = ctk.CTkFrame(
            self,
            border_width=2,
            border_color="#3B82F6",
            fg_color="#1E293B",
            corner_radius=12,
        )
        self.drop_frame.pack(pady=6, padx=20, fill="x")

        self.drop_label = ctk.CTkLabel(
            self.drop_frame,
            text="📥 Görselleri veya Klasörü Buraya Sürükleyip Bırakın",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#93C5FD",
        )
        self.drop_label.pack(padx=10, pady=(12, 8))

        self.btn_subframe = ctk.CTkFrame(self.drop_frame, fg_color="transparent")
        self.btn_subframe.pack(pady=(0, 8))

        self.select_btn = ctk.CTkButton(
            self.btn_subframe,
            text="📁 Dosyalardan Seç",
            command=self.select_files,
            height=38,
            font=ctk.CTkFont(weight="bold"),
        )
        self.select_btn.pack(side="left", padx=6)

        self.clear_btn = ctk.CTkButton(
            self.btn_subframe,
            text="🗑️ Temizle",
            command=self.clear_files,
            height=38,
            fg_color="#EF4444",
            hover_color="#DC2626",
            width=100,
        )
        self.clear_btn.pack(side="left", padx=6)

        self.compress_btn = ctk.CTkButton(
            self.btn_subframe,
            text="🚀 Sıkıştırmayı Başlat (Oluştur)",
            command=self.start_compression_thread,
            height=38,
            fg_color="#10B981",
            hover_color="#059669",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.compress_btn.pack(side="left", padx=6)

        self.file_count_label = ctk.CTkLabel(
            self.drop_frame, text="Henüz dosya seçilmedi", text_color="gray"
        )
        self.file_count_label.pack(pady=(0, 10))

        # Sürükle-Bırak bağlaması
        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self.handle_drop)

        # --- Ayarlar Alanı ---
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.pack(pady=6, padx=20, fill="x")

        self.quality_label = ctk.CTkLabel(
            self.settings_frame, text="Sıkıştırma Gücü / Kalite Dengesi: %80"
        )
        self.quality_label.pack(pady=(10, 2), padx=15, anchor="w")

        self.quality_slider = ctk.CTkSlider(
            self.settings_frame,
            from_=10,
            to=100,
            number_of_steps=90,
            command=self.update_quality_label,
        )
        self.quality_slider.set(80)
        self.quality_slider.pack(pady=(0, 10), padx=15, fill="x")

        self.options_subframe = ctk.CTkFrame(
            self.settings_frame, fg_color="transparent"
        )
        self.options_subframe.pack(pady=(0, 10), padx=15, fill="x")

        self.quantize_var = ctk.BooleanVar(value=True)
        self.quantize_check = ctk.CTkCheckBox(
            self.options_subframe,
            text="Akıllı PNG Sıkıştırma (8-bit Renk Paleti - %70'e varan tasarruf)",
            variable=self.quantize_var,
        )
        self.quantize_check.pack(anchor="w", pady=4)

        self.webp_var = ctk.BooleanVar(value=False)
        self.webp_check = ctk.CTkCheckBox(
            self.options_subframe,
            text="Çıktıyı WebP Formatına Dönüştür (Web siteleri için en iyisi)",
            variable=self.webp_var,
        )
        self.webp_check.pack(anchor="w", pady=4)

        # --- İlerleme Çubuğu ve Log ---
        self.progressbar = ctk.CTkProgressBar(self)
        self.progressbar.pack(pady=(8, 4), padx=20, fill="x")
        self.progressbar.set(0)

        self.log_box = ctk.CTkTextbox(
            self, height=120, state="disabled", font=ctk.CTkFont(size=12)
        )
        self.log_box.pack(pady=(4, 15), padx=20, fill="both", expand=True)

    def update_quality_label(self, value):
        self.quality_label.configure(
            text=f"Sıkıştırma Gücü / Kalite Dengesi: %{int(value)}"
        )

    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "
")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def add_valid_files(self, paths):
        valid_ext = (".png", ".jpg", ".jpeg")
        added_count = 0

        for path in paths:
            if os.path.isdir(path):
                for root, _, files in os.walk(path):
                    if "compressed_images" in root:
                        continue
                    for f in files:
                        if f.lower().endswith(valid_ext):
                            full_p = os.path.join(root, f)
                            if full_p not in self.selected_files:
                                self.selected_files.append(full_p)
                                added_count += 1
            elif os.path.isfile(path) and path.lower().endswith(valid_ext):
                if path not in self.selected_files:
                    self.selected_files.append(path)
                    added_count += 1

        if added_count > 0:
            self.file_count_label.configure(
                text=f"✅ Toplam {len(self.selected_files)} görsel seçildi — Başlat butonuna basabilirsiniz",
                text_color="#10B981",
            )
            self.log(
                f"📥 {added_count} yeni görsel eklendi (Toplam: {len(self.selected_files)})."
            )
        else:
            self.log("⚠️ Geçerli bir görsel (.png, .jpg) bulunamadı veya zaten ekli.")

    def handle_drop(self, event):
        dropped_paths = self.tk.splitlist(event.data)
        self.add_valid_files(dropped_paths)

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Görselleri Seç",
            filetypes=[
                ("Görseller", "*.png *.jpg *.jpeg"),
                ("PNG Dosyaları", "*.png"),
            ],
        )
        if files:
            self.add_valid_files(list(files))

    def clear_files(self):
        self.selected_files.clear()
        self.file_count_label.configure(
            text="Henüz dosya seçilmedi", text_color="gray"
        )
        self.progressbar.set(0)
        self.log("🗑️ Seçili dosya listesi temizlendi.")

    def start_compression_thread(self):
        if not self.selected_files:
            messagebox.showwarning(
                "Uyarı", "Lütfen önce görselleri sürükleyin veya seçin!"
            )
            return

        self.compress_btn.configure(state="disabled", text="⏳ İşleniyor...")
        self.progressbar.set(0)
        threading.Thread(target=self.compress_images, daemon=True).start()

    def compress_images(self):
        total = len(self.selected_files)
        quality = int(self.quality_slider.get())
        use_quantize = self.quantize_var.get()
        convert_webp = self.webp_var.get()

        base_dir = os.path.dirname(self.selected_files[0])
        output_dir = os.path.join(base_dir, "compressed_images")
        os.makedirs(output_dir, exist_ok=True)

        total_saved_bytes = 0

        for idx, file_path in enumerate(self.selected_files):
            try:
                orig_size = os.path.getsize(file_path)
                filename = os.path.basename(file_path)
                name, ext = os.path.splitext(filename)

                img = Image.open(file_path)

                if convert_webp:
                    out_path = os.path.join(output_dir, f"{name}.webp")
                    img.save(out_path, "WEBP", quality=quality, method=6)
                else:
                    out_path = os.path.join(output_dir, f"{name}_min.png")
                    if use_quantize:
                        colors = max(32, int((quality / 100) * 256))
                        img = img.quantize(colors=colors, method=2)

                    img.save(out_path, "PNG", optimize=True)

                new_size = os.path.getsize(out_path)
                saved = orig_size - new_size
                total_saved_bytes += max(0, saved)
                percent = (saved / orig_size) * 100 if orig_size > 0 else 0

                orig_kb = orig_size / 1024
                new_kb = new_size / 1024

                self.log(
                    f"✅ {filename}: {orig_kb:.1f} KB ➔ {new_kb:.1f} KB (%{percent:.1f} küçüldü)"
                )

            except Exception as e:
                self.log(f"❌ Hata ({os.path.basename(file_path)}): {str(e)}")

            self.progressbar.set((idx + 1) / total)

        total_saved_mb = total_saved_bytes / (1024 * 1024)
        self.log("-" * 50)
        self.log(
            f"🎉 İşlem Tamamlandı! Toplam Tasarruf: {total_saved_mb:.2f} MB"
        )
        self.log(f"📁 Kayıt Yeri: {output_dir}")

        self.compress_btn.configure(
            state="normal", text="🚀 Sıkıştırmayı Başlat (Oluştur)"
        )
        
        # Cross-platform open folder
        try:
            if hasattr(os, "startfile"):
                os.startfile(output_dir)
            else:
                os.system(f'open "{output_dir}"')
        except Exception:
            pass


if __name__ == "__main__":
    app = ImageCompressorApp()
    app.mainloop()
