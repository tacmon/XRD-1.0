import csv
import ast
import re

def process_results(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    processed_rows = []
    for row in rows:
        phases_str = row['Predicted phases']
        confidence_str = row['Confidence']

        # Parse phases list
        if phases_str == '未知':
            processed_rows.append(row)
            continue
        try:
            phases = ast.literal_eval(phases_str)
        except:
            phases = [] # Or handle error

        # Parse confidence list (handle np.float64)
        # We extract numbers specifically from inside np.float64(...) or just the numbers that aren't '64'
        confidences = [float(x) for x in re.findall(r'np\.float64\(([\d\.]+)\)', confidence_str)]
        if not confidences: # Fallback for simple formats
             confidences = [float(x) for x in re.findall(r'\d+\.\d+|\d+', confidence_str)]
             confidences = [c for c in confidences if c != 64.0 or '.64' in confidence_str] # risky hack

        found_cr_si_te3 = False
        max_conf_cr_si_te3 = 0.0
        found_si = False
        max_conf_si = 0.0

        for p, c in zip(phases, confidences):
            if 'CrSiTe3' in p:
                found_cr_si_te3 = True
                max_conf_cr_si_te3 = max(max_conf_cr_si_te3, c)
            if p.startswith('Si_') or p == 'Si':
                found_si = True
                max_conf_si = max(max_conf_si, c)

        # Mark as unknown if:
        # 1. CrSiTe3 not found or confidence <= 50%
        # 2. OR if Si was found and its confidence > 50%
        should_mark_unknown = False
        if not found_cr_si_te3 or max_conf_cr_si_te3 <= 50.0:
            should_mark_unknown = True
        if found_si and max_conf_si > 50.0:
            should_mark_unknown = True

        if should_mark_unknown:
            row['Predicted phases'] = '未知'
            row['Confidence'] = ''
        
        processed_rows.append(row)

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(processed_rows)

if __name__ == '__main__':
    process_results('result.csv', 'result_processed.csv')
    print("Processed results saved to result_processed.csv")
