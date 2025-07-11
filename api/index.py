# api/index.py
# VERSI FINAL: Menggunakan relative import (.) untuk mengatasi ModuleNotFoundError di Vercel.

import sys
import io
import re
from flask import Flask, render_template_string, request

# ======================================================================
# BAGIAN YANG DIPERBAIKI: Menggunakan Relative Import (tanda titik di depan)
# ======================================================================
from .aes_key_schedule import key_schedule_explain
from .aes_sub_bytes import sub_bytes_explain
from .aes_shift_rows import shift_rows_explain
from .aes_mix_columns import mix_columns_poly_explain
from .aes_add_round_key import add_round_key_explain

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Fungsi "pembungkus" untuk menangkap output print() menjadi string
def run_aes_function(func, *args):
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    try:
        func(*args, doc=None) # Kita tidak membuat docx di web
    except Exception as e:
        print(f"Terjadi error: {e}")
    finally:
        sys.stdout = old_stdout
    
    output_str = captured_output.getvalue()
    # Hapus ANSI color codes dari colorama
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    output_str = ansi_escape.sub('', output_str)
    return output_str


# Template HTML untuk form dan hasil
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AES Step-by-Step Online</title>
    <style>
        body { font-family: sans-serif; margin: 2em; background-color: #f4f4f4; color: #333; }
        .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1, h2 { color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; }
        label { display: block; margin-top: 15px; font-weight: bold; }
        input[type="text"], select { width: 98%; padding: 8px; margin-top: 5px; border: 1px solid #ddd; border-radius: 4px; }
        button { background-color: #007BFF; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; margin-top: 20px; font-size: 16px; }
        button:hover { background-color: #0056b3; }
        pre { background-color: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 4px; white-space: pre-wrap; word-wrap: break-word; font-family: 'Courier New', Courier, monospace; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AES Step-by-Step Online</h1>
        <form method="post">
            <h2>Pilih Operasi</h2>
            <select name="operation" id="operation">
                <option value="mix_columns">Uji MixColumns</option>
                <option value="add_round_key">Uji AddRoundKey</option>
                <option value="sub_bytes">Uji SubBytes</option>
                <option value="shift_rows">Uji ShiftRows</option>
                <option value="key_schedule">Uji Key Schedule</option>
            </select>
            
            <label for="input1">Input 1 (State / Kunci Awal):</label>
            <input type="text" id="input1" name="input1" placeholder="cth: 5BFE07003BAD5909F2CBFC053100D6C5" required>

            <label for="input2">Input 2 (Round Key, hanya untuk AddRoundKey):</label>
            <input type="text" id="input2" name="input2" placeholder="cth: A088232A851ED034B0018974B0012B5E">

            <button type="submit">Jalankan</button>
        </form>

        {% if result %}
        <h2>Hasil:</h2>
        <pre>{{ result }}</pre>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    result_text = ""
    if request.method == 'POST':
        operation = request.form['operation']
        input1 = request.form['input1']
        input2 = request.form.get('input2', '')

        try:
            if operation == 'mix_columns': result_text = run_aes_function(mix_columns_poly_explain, input1)
            elif operation == 'sub_bytes': result_text = run_aes_function(sub_bytes_explain, input1)
            elif operation == 'shift_rows': result_text = run_aes_function(shift_rows_explain, input1)
            elif operation == 'key_schedule': result_text = run_aes_function(key_schedule_explain, input1)
            elif operation == 'add_round_key': result_text = run_aes_function(add_round_key_explain, input1, input2, 0)
        except Exception as e:
            result_text = f"Terjadi kesalahan pada saat eksekusi fungsi: {e}"

    return render_template_string(HTML_TEMPLATE, result=result_text)