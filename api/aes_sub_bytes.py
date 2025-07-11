# api/aes_sub_bytes.py
import time
from colorama import Fore
# DIUBAH: Gunakan relative import
from .aes_constants import S_BOX
from .aes_reporting import print_matrix, add_matrix_to_doc, add_calculation_paragraph

# ... sisa kode di file ini sama persis ...
def sub_bytes_explain(state_hex, doc):
    print(f"\n{Fore.MAGENTA}--- Steps: SubBytes ---");
    if doc: doc.add_heading("Steps: SubBytes", level=3)
    state_bytes = bytearray.fromhex(state_hex)
    for i in range(16):
        old_val, new_val = state_bytes[i], S_BOX[state_bytes[i]]; state_bytes[i] = new_val
        text_doc = f"The value [{old_val:02X}] is replaced with {new_val:02X} (Via S-Box)"; print(f"  {text_doc}"); add_calculation_paragraph(doc, text_doc); time.sleep(0.01)
    result_hex = state_bytes.hex()
    print_matrix("SubBytes Result", result_hex); add_matrix_to_doc(doc, "SubBytes Result", result_hex);
    return result_hex