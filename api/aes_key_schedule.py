# api/aes_key_schedule.py
# VERSI FINAL: Menambahkan pemeriksaan 'if doc:' untuk kompatibilitas web.
import time
from colorama import Fore
# DIUBAH: Gunakan relative import
from .aes_constants import S_BOX, RCON
from .aes_reporting import (
    print_matrix, add_matrix_to_doc, add_bold_paragraph,
    add_calculation_paragraph, print_interim_matrix
)

def key_schedule_explain(initial_key_hex, doc):
    print(f"\n{Fore.YELLOW}===== PROCESS KEY SCHEDULE =====")
    if doc: doc.add_heading("Process Key Schedule", level=2)
    initial_key_bytes = bytearray.fromhex(initial_key_hex); round_keys_bytes = [initial_key_bytes]
    print_matrix("Inital Key (Round 0)", initial_key_hex)
    if doc: add_matrix_to_doc(doc, "Inital Key (Round 0)", initial_key_hex) # Perbaikan
    time.sleep(0.1)
    for round_num in range(1, 11):
        print(f"\n{Fore.MAGENTA}=== Round Key Generation Process {round_num} ===")
        if doc: doc.add_paragraph(); doc.add_heading(f"Round Key Generation Process {round_num}", level=3)
        prev_key = round_keys_bytes[-1]
        
        title = f"--- 1: Creating a Temporary Word ---"
        print(f"\n{Fore.CYAN}{title}");
        if doc: add_bold_paragraph(doc, title.strip(" -"))

        temp_word = prev_key[12:16]; text_doc = f"Last Column of Round {round_num-1} Key: {' '.join(f'{b:02X}' for b in temp_word)}"; print("  "+text_doc)
        if doc: add_calculation_paragraph(doc, text_doc) # Perbaikan
        
        temp_word = temp_word[1:] + temp_word[:1]; text_doc = f"RotWord: {' '.join(f'{b:02X}' for b in temp_word)}"; print("  "+text_doc)
        if doc: add_calculation_paragraph(doc, text_doc) # Perbaikan
        
        temp_word = bytearray(S_BOX[b] for b in temp_word); text_doc = f"SubBytes: {' '.join(f'{b:02X}' for b in temp_word)}"; print("  "+text_doc)
        if doc: add_calculation_paragraph(doc, text_doc) # Perbaikan
        
        rcon_word = bytearray([RCON[round_num], 0, 0, 0])
        
        transformed_word = bytearray(temp_word)
        for i in range(4): temp_word[i] ^= rcon_word[i]
        
        t1_combined = f"  Temporary Word : {' '.join(f'{b:02X}' for b in transformed_word)} ({' '.join(f'{b:08b}' for b in transformed_word)})"
        print(f"    {Fore.GREEN}{t1_combined}")
        if doc: add_calculation_paragraph(doc, t1_combined) # Perbaikan
        
        t2_combined = f"  Rcon Word[{round_num}]   : {' '.join(f'{b:02X}' for b in rcon_word)} ({' '.join(f'{b:08b}' for b in rcon_word)})"
        print(f"    {Fore.RED}{t2_combined}")
        if doc: add_calculation_paragraph(doc, t2_combined) # Perbaikan
        
        print("    --------------------------------------------- (XOR)")
        if doc: doc.add_paragraph("  --------------------------------------------- (XOR)") # Perbaikan
        
        t3_combined = f"  Hasil: {' '.join(f'{b:02X}' for b in temp_word)} ({' '.join(f'{b:08b}' for b in temp_word)})"
        print(f"    {Fore.YELLOW}{t3_combined}")
        if doc: add_calculation_paragraph(doc, t3_combined) # Perbaikan

        new_key = bytearray(16)
        print(f"\n{Fore.CYAN}--- 2: Calculating New Key Columns ---");
        if doc: add_bold_paragraph(doc, "\n2: Calculating New Key Columns")
        for col in range(4):
            col_desc = f"Calculating Column {col}"; print(f"\n{Fore.BLUE}{col_desc}:");
            if doc: add_bold_paragraph(doc, col_desc)
            for i in range(4):
                if col == 0: val1, val2 = prev_key[i], temp_word[i]
                else: idx, prev_new_idx = col*4+i, (col-1)*4+i; val1, val2 = prev_key[idx], new_key[prev_new_idx]
                res = val1 ^ val2; new_key[col*4+i] = res

                combined_text = f"{val1:02X} \u2295 {val2:02X} = {res:02X} ({val1:08b} \u2295 {val2:08b} = {res:08b})"
                print(f"  {Fore.GREEN}{combined_text}")
                if doc: add_calculation_paragraph(doc, combined_text) # Perbaikan
            if col < 3: 
                print_interim_matrix("Temporary key status", new_key, col + 1)
                interim_hex = ''.join(f'{b:02x}' for b in new_key[:(col+1)*4])+'XX'*(12-col*4)
                if doc: add_matrix_to_doc(doc, "Temporary key status", interim_hex) # Perbaikan
        round_keys_bytes.append(new_key)
        print_matrix(f"Round Key {round_num}", new_key.hex())
        if doc: add_matrix_to_doc(doc, f"Round Key {round_num}", new_key.hex()) # Perbaikan
        time.sleep(0.1)
    return [key.hex() for key in round_keys_bytes]