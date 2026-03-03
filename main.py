import os, re, tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw, ImageFont
from deep_translator import GoogleTranslator

# Rozmiar kartki A6 przy 300 DPI
W, H = int(148/25.4*300), int(105/25.4*300)

def nazwa_pliku(s):
    # Usuwa znaki niedozwolone w nazwach plików
    s = re.sub(r'[\\/*?:"<>|]', "", s)
    return s.strip().replace(" ", "_")[:30]

class TlumaczA6:
    def __init__(self, r):
        self.r = r
        self.r.title("Multi-Lang A6 Generator (PL + 2 Języki)")
        
        # --- UI: Wybór Języków ---
        frame_lang = tk.Frame(r)
        frame_lang.pack(pady=10, padx=10)
        
        tk.Label(frame_lang, text="Tłumacz z Polskiego na:", font=("Arial", 9, "bold")).grid(row=0, column=0, columnspan=2)
        
        tk.Label(frame_lang, text="Język 1 (np. de):").grid(row=1, column=0, sticky="e", pady=2)
        self.lang1 = tk.StringVar(value="de")
        tk.Entry(frame_lang, textvariable=self.lang1, width=10).grid(row=1, column=1, sticky="w")
        
        tk.Label(frame_lang, text="Język 2 (np. en):").grid(row=2, column=0, sticky="e", pady=2)
        self.lang2 = tk.StringVar(value="en")
        tk.Entry(frame_lang, textvariable=self.lang2, width=10).grid(row=2, column=1, sticky="w")

        # --- UI: Pole tekstowe ---
        tk.Label(r, text="Wklej listę słów (każde w nowej linii):").pack()
        self.t = tk.Text(r, height=12, width=60)
        self.t.pack(pady=10, px=10)
        
        # --- UI: Przycisk i Postęp ---
        self.btn = tk.Button(r, text="GENERUJ ETYKIETY", command=self.go, bg="#
