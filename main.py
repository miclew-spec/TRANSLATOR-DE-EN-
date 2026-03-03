import os, re, tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw, ImageFont
import textwrap # Dodajemy nową bibliotekę do zawijania
from deep_translator import GoogleTranslator

W, H = int(148/25.4*300), int(105/25.4*300)

def nazwa_pliku(s):
    s = re.sub(r'[\\/*?:"<>|]', "", s)
    return s.strip().replace(" ", "_")[:30]

class TlumaczA6:
    def __init__(self, r):
        self.r = r
        self.r.title("Multi-Lang A6 Generator - Naprawa Tekstu")
        
        frame_lang = tk.Frame(r)
        frame_lang.pack(pady=10, padx=10)
        
        tk.Label(frame_lang, text="Język 1 (np. de):").grid(row=0, column=0, pady=2)
        self.lang1 = tk.StringVar(value="de")
        tk.Entry(frame_lang, textvariable=self.lang1, width=10).grid(row=0, column=1)
        
        tk.Label(frame_lang, text="Język 2 (np. en):").grid(row=1, column=0, pady=2)
        self.lang2 = tk.StringVar(value="en")
        tk.Entry(frame_lang, textvariable=self.lang2, width=10).grid(row=1, column=1)

        self.t = tk.Text(r, height=10, width=50)
        self.t.pack(pady=10, padx=10)
        
        self.btn = tk.Button(r, text="GENERUJ POPRAWIONE ETYKIETY", command=self.go, bg="green", fg="white")
        self.btn.pack(pady=5)
        
        self.p = ttk.Progressbar(r, length=300, mode='determinate')
        self.p.pack(pady=10)

    def rysuj_zawiniety_tekst(self, draw, tekst, y_range, kolor, max_font_size):
        try:
            fnt = ImageFont.truetype("arialbd.ttf", max_font_size)
        except:
            fnt = ImageFont.load_default()

        # Marginesy (zostawiamy po 100 pikseli z każdej strony)
        max_width = W - 200
        
        # Obliczamy ile znaków średnio mieści się w linii dla danej czcionki
        # Używamy bezpiecznego przybliżenia
        avg_char_width = draw.textbbox((0,0), "W", font=fnt)[2]
        chars_per_line = max(1, max_width // avg_char_width)
        
        # Rozbijamy tekst na linie
        linie = textwrap.wrap(tekst, width=chars_per_line)
        
        # Obliczamy całkowitą wysokość bloku tekstu
        line_heights = [draw.textbbox((0,0), l, font=fnt)[3] for l in linie]
        total_text_height = sum(line_heights) + (10 * (len(linie)-1))
        
        y_start, y_end = y_range
        current_y = y_start + (y_end - y_start - total_text_height) // 2

        for linia in linie:
            bbox = draw.textbbox((0, 0), linia, font=fnt)
            tw = bbox[2] - bbox[0]
            draw.text(((W - tw) // 2, current_y), linia, fill=kolor, font=fnt)
            current_y += (bbox[3] - bbox[1]) + 10 # Odstęp między liniami

    def go(self):
        dane = [d.strip() for d in self.t.get("1.0", "end").split('\n') if d.strip()]
        if not dane: return
        f = filedialog.askdirectory()
        if not f: return
        
        cel = os.path.join(f, "ETYKIETY_NAPRAWIONE")
        os.makedirs(cel, exist_ok=True)
        self.p["maximum"] = len(dane)
        
        t1 = GoogleTranslator(source='pl', target=self.lang1.get())
        t2 = GoogleTranslator(source='pl', target=self.lang2.get())

        for i, pl in enumerate(dane, 1):
            try:
                txt_l1 = t1.translate(pl).upper()
                txt_l2 = t2.translate(pl).upper()
                
                img = Image.new("RGB", (W, H), "white")
                draw = ImageDraw.Draw(img)
                h3 = H // 3
                
                # Używamy nowej funkcji z zawijaniem
                self.rysuj_zawiniety_tekst(draw, txt_l1, (0, h3), "black", 90)
                self.rysuj_zawiniety_tekst(draw, txt_l2, (h3, 2*h3), "#444444", 75)
                self.rysuj_zawiniety_tekst(draw, pl, (2*h3, H), "gray", 60)
                
                draw.line([(100, h3), (W-100, h3)], fill="lightgray", width=2)
                draw.line([(100, 2*h3), (W-100, 2*h3)], fill="lightgray", width=2)
                draw.rectangle([15, 15, W-15, H-15], outline="black", width=5)
                
                img.save(os.path.join(cel, f"{i:03d}_{nazwa_pliku(pl)}.png"), dpi=(300, 300))
            except: pass
            
            self.p["value"] = i
            self.r.update()
        messagebox.showinfo("OK", "Gotowe!")

if __name__ == "__main__":
    root = tk.Tk(); TlumaczA6(root); root.mainloop()
