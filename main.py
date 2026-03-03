import os, re, tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw, ImageFont
from deep_translator import GoogleTranslator

# Rozmiar kartki A6 przy 300 DPI
W, H = int(148/25.4*300), int(105/25.4*300)

def nazwa_pliku(s):
    s = re.sub(r'[\\/*?:"<>|]', "", s)
    return s.strip().replace(" ", "_")[:30]

class TlumaczA6:
    def __init__(self, r):
        self.r = r
        self.r.title("Multi-Lang A6 Generator")
        
        frame_lang = tk.Frame(r)
        frame_lang.pack(pady=10, padx=10)
        
        tk.Label(frame_lang, text="Tłumacz z Polskiego na:", font=("Arial", 9, "bold")).grid(row=0, column=0, columnspan=2)
        
        tk.Label(frame_lang, text="Język 1 (np. de):").grid(row=1, column=0, sticky="e", pady=2)
        self.lang1 = tk.StringVar(value="de")
        tk.Entry(frame_lang, textvariable=self.lang1, width=10).grid(row=1, column=1, sticky="w")
        
        tk.Label(frame_lang, text="Język 2 (np. en):").grid(row=2, column=0, sticky="e", pady=2)
        self.lang2 = tk.StringVar(value="en")
        tk.Entry(frame_lang, textvariable=self.lang2, width=10).grid(row=2, column=1, sticky="w")

        tk.Label(r, text="Wklej listę słów (jedno na linię):").pack()
        self.t = tk.Text(r, height=12, width=60)
        self.t.pack(pady=10, padx=10)
        
        self.btn = tk.Button(r, text="GENERUJ ETYKIETY", command=self.go, bg="green", fg="white", font=("Arial", 10, "bold"))
        self.btn.pack(pady=5, fill="x", padx=50)
        
        self.p = ttk.Progressbar(r, length=400, mode='determinate')
        self.p.pack(pady=15)

    def rysuj_sekcje(self, draw, tekst, y_range, kolor, font_size):
        try:
            fnt = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            fnt = ImageFont.load_default()
        
        y_start, y_end = y_range
        bbox = draw.textbbox((0, 0), tekst, font=fnt)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        x = (W - tw) // 2
        y = y_start + (y_end - y_start - th) // 2
        draw.text((x, y), tekst, fill=kolor, font=fnt)

    def go(self):
        surowe = self.t.get("1.0", "end").strip().split('\n')
        dane = [d.strip() for d in surowe if d.strip()]
        
        if not dane:
            messagebox.showwarning("Błąd", "Lista jest pusta!")
            return
            
        f = filedialog.askdirectory()
        if not f: return
        
        cel = os.path.join(f, "ETYKIETY_3_JEZYKI")
        os.makedirs(cel, exist_ok=True)
        self.p["maximum"] = len(dane)
        
        t1 = GoogleTranslator(source='pl', target=self.lang1.get())
        t2 = GoogleTranslator(source='pl', target=self.lang2.get())

        for i, tekst_pl in enumerate(dane, 1):
            try:
                tekst_l1 = t1.translate(tekst_pl).upper()
                tekst_l2 = t2.translate(tekst_pl).upper()
                
                img = Image.new("RGB", (W, H), "white")
                draw = ImageDraw.Draw(img)
                h_sekcji = H // 3
                
                self.rysuj_sekcje(draw, tekst_l1, (0, h_sekcji), "black", 100)
                self.rysuj_sekcje(draw, tekst_l2, (h_sekcji, 2*h_sekcji), "darkgray", 85)
                self.rysuj_sekcje(draw, tekst_pl, (2*h_sekcji, H), "gray", 75)
                
                draw.line([(80, h_sekcji), (W-80, h_sekcji)], fill="lightgray", width=3)
                draw.line([(80, 2*h_sekcji), (W-80, 2*h_sekcji)], fill="lightgray", width=3)
                draw.rectangle([15, 15, W-15, H-15], outline="black", width=5)
                
                nazwa = f"{i:03d}_{nazwa_pliku(tekst_pl)}.png"
                img.save(os.path.join(cel, nazwa), dpi=(300, 300))
                
            except Exception as e:
                print(f"Blad: {e}")
            
            self.p["value"] = i
            self.r.update()
            
        messagebox.showinfo("Sukces", "Zakończono!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TlumaczA6(root)
    root.mainloop()
