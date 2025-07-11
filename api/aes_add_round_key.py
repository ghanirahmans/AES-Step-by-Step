# aes_add_round_key.py
import time
from colorama import Fore
from aes_reporting import print_matrix, add_matrix_to_doc, add_calculation_paragraph

def add_round_key_explain(state_hex, key_hex, round_num, doc):
    print(f"\n{Fore.MAGENTA}--- Steps: AddRoundKey ---")
    if doc: doc.add_heading(f"Steps: AddRoundKey", level=3)
    state_bytes, key_bytes = bytearray.fromhex(state_hex), bytearray.fromhex(key_hex)
    print_matrix("State Before", state_hex); add_matrix_to_doc(doc, "State Before", state_hex)
    print_matrix("Round Key", key_hex); add_matrix_to_doc(doc, "Round Key", key_hex)
    print(f"\n{Fore.BLUE}Details of XOR operation between state and round key:")
    if doc: doc.add_paragraph("Details of XOR operation between state and round key:")
    result_bytes = bytearray(16)
    for i in range(16):
        res = state_bytes[i] ^ key_bytes[i]; result_bytes[i] = res
        text_doc = f"{state_bytes[i]:02X} \u2295 {key_bytes[i]:02X} = {res:02X} ({state_bytes[i]:08b} \u2295 {key_bytes[i]:08b} = {res:08b})"
        print(f"  {Fore.GREEN}{text_doc}");add_calculation_paragraph(doc,text_doc);time.sleep(0.05)
    result_hex = result_bytes.hex()
    print_matrix(f"Result of AddRoundKey Round {round_num}", result_hex)
    add_matrix_to_doc(doc, f"Result of AddRoundKey Round {round_num}", result_hex)
    return result_hex