import sys
import io
import re
from flask import Flask, render_template_string, request

# Impor semua fungsi dari modul AES yang ada di folder yang sama
from aes_key_schedule import key_schedule_explain
from aes_sub_bytes import sub_bytes_explain
from aes_shift_rows import shift_rows_explain
from aes_mix_columns import mix_columns_poly_explain
from aes_add_round_key import add_round_key_explain

# Inisialisasi Flask
app = Flask(__name__)

# Fungsi "pembungkus" untuk menangkap output print() menjadi string
def run_aes_function(func, *args):
    # ... (Isi fungsi ini sama persis seperti di jawaban PythonAnywhere)
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    try:
        func(*args, doc=None)
    except Exception as e:
        print(f"Terjadi error: {e}")
    finally:
        sys.stdout = old_stdout
    output_str = captured_output.getvalue()
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    output_str = ansi_escape.sub('', output_str)
    return output_str

# Template HTML
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>AES Step-by-Step Vercel</title>
        <style>
            body { font-family: sans-serif; margin: 2em; background-color: #f4f4f4; }
            .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            pre { background-color: #e9ecef; padding: 15px; border-radius: 4px; white-space: pre-wrap; word-wrap: break-word; font-family: monospace; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>AES Step-by-Step (Vercel)</h1>
            <form method="post">
                <select name="operation" id="operation">
                    <option value="mix_columns">Uji MixColumns</option>
                    <option value="add_round_key">Uji AddRoundKey</option>
                    <option value="sub_bytes">Uji SubBytes</option>
                    <option value="shift_rows">Uji ShiftRows</option>
                    <option value="key_schedule">Uji Key Schedule</option>
                </select>
                <br><br>
                <label for="input1">Input 1 (State / Kunci Awal):</label>
                <input type="text" id="input1" name="input1" style="width: 95%;" required>

                <label for="input2">Input 2 (Round Key, untuk AddRoundKey):</label>
                <input type="text" id="input2" name="input2" style="width: 95%;">

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
    # ... (Isi fungsi ini sama persis seperti di jawaban PythonAnywhere)
    result_text = ""
    if request.method == 'POST':
        operation = request.form['operation']
        input1 = request.form['input1']
        input2 = request.form.get('input2', '')

        if operation == 'mix_columns': result_text = run_aes_function(mix_columns_poly_explain, input1)
        elif operation == 'sub_bytes': result_text = run_aes_function(sub_bytes_explain, input1)
        elif operation == 'shift_rows': result_text = run_aes_function(shift_rows_explain, input1)
        elif operation == 'key_schedule': result_text = run_aes_function(key_schedule_explain, input1)
        elif operation == 'add_round_key': result_text = run_aes_function(add_round_key_explain, input1, input2, 0)

    return render_template_string(HTML_TEMPLATE, result=result_text)