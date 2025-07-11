# aes_mix_columns.py
# VERSI FINAL REVISI 3: Mengembalikan print 'Step: Multiply' ke sini untuk format yang presisi.
from colorama import Fore
from aes_constants import MIX_COLUMNS_MATRIX
from aes_reporting import (
    add_bold_paragraph, add_calculation_paragraph, add_constant_matrix_to_doc,
    print_constant_matrix, print_matrix, add_matrix_to_doc,
    add_poly_text_to_paragraph
)
from aes_polynomial import explain_gmul_poly

def mix_columns_poly_explain(state_hex, doc):
    print(f"\n{Fore.MAGENTA}--- Steps: MixColumns ---");
    if doc:
        doc.add_heading("Steps: MixColumns", level=3)
        add_constant_matrix_to_doc(doc, "Constant Matrix Used:", MIX_COLUMNS_MATRIX)
    print_constant_matrix("Constant Matrix Used:", MIX_COLUMNS_MATRIX)

    state_bytes = bytearray.fromhex(state_hex);
    new_state_bytes = bytearray(16)
    
    for c in range(4):
        print(f"\n{Fore.BLUE}Step: Mixing Column {c}:")
        if doc: doc.add_paragraph().add_run(f"\nStep: Mixing Column {c}:").bold = True

        s_col = state_bytes[c*4 : c*4+4]
        res_col_bytes = bytearray(4)

        for r in range(4):
            m_row = MIX_COLUMNS_MATRIX[r]
            print(f"\n{Fore.CYAN}Calculation for New Bytes in Row {r}:")
            if doc: add_bold_paragraph(doc, f"Calculation for New Bytes in Row {r}:")

            summary_parts = [f"({m_row[i]:02X} * {s_col[i]:02X})" for i in range(4)]
            summary_line = " \u2295 ".join(summary_parts)
            print(f"{Fore.MAGENTA}{summary_line}")
            if doc: add_calculation_paragraph(doc, summary_line)
            
            gmul_results = []
            for i in range(4):
                s_val = s_col[i]
                m_val = m_row[i]
                
                # Print judul 'Step' di sini, sebelum memanggil fungsi penjelasan
                print(f"Step: Multiply {s_val:02X} by {m_val:02X}")
                if doc: add_bold_paragraph(doc, f"Step: Multiply {s_val:02X} by {m_val:02X}")

                result_byte = explain_gmul_poly(s_val, m_val, doc)
                gmul_results.append(result_byte)

            final_byte = gmul_results[0] ^ gmul_results[1] ^ gmul_results[2] ^ gmul_results[3]
            res_col_bytes[r] = final_byte

            print(f"{Fore.CYAN}--- Final Step: Calculate New Bytes ---")
            sum_parts_hex = [f"{val:02X}" for val in gmul_results]
            sum_str = " \u2295 ".join(sum_parts_hex) + f" = {final_byte:02X}"
            print(f"      {Fore.GREEN}{sum_str}\n")
            if doc: add_calculation_paragraph(doc, sum_str)
        
        for i in range(4): new_state_bytes[c*4+i] = res_col_bytes[i]

    result_hex = new_state_bytes.hex()
    print_matrix("MixColumns Final Result", result_hex); add_matrix_to_doc(doc, "MixColumns Final Result", result_hex)
    return result_hex