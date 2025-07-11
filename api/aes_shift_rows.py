# api/aes_shift_rows.py
import time
from colorama import Fore
# DIUBAH: Gunakan relative import
from .aes_reporting import print_matrix, add_matrix_to_doc, add_calculation_paragraph

# ... sisa kode di file ini sama persis ...
def shift_rows_explain(state_hex, doc):
    print(f"\n{Fore.MAGENTA}--- Steps: ShiftRows ---");
    if doc: doc.add_heading("Steps: ShiftRows", level=3)
    s = bytearray.fromhex(state_hex)
    print_matrix("State Before ShiftRows", state_hex); add_matrix_to_doc(doc, "State Before ShiftRows", state_hex)
    time.sleep(0.1)
    final_s = bytearray(s)
    final_s[1],final_s[5],final_s[9],final_s[13] = s[5],s[9],s[13],s[1]; final_s[2],final_s[6],final_s[10],final_s[14] = s[10],s[14],s[2],s[6]; final_s[3],final_s[7],final_s[11],final_s[15] = s[15],s[3],s[7],s[11]
    print(f"\n{Fore.BLUE}Explanation of row shifts:")
    if doc: doc.add_paragraph("Explanation of row shifts:")
    for r in range(4):
        before = [s[c*4+r] for c in range(4)]; after = [final_s[c*4+r] for c in range(4)]
        text_doc = f"- Row {r}: {'Not shifted' if r==0 else f'Shifted {r} bytes to the left'}: {' '.join(f'{b:02X}' for b in before)} becomes {' '.join(f'{b:02X}' for b in after)}"
        print(f"  {text_doc}"); add_calculation_paragraph(doc, text_doc); time.sleep(0.1)
    result_hex = final_s.hex()
    print_matrix("ShiftRows Result", result_hex); add_matrix_to_doc(doc, "ShiftRows Result", result_hex)
    return result_hex