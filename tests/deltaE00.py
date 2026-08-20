import csv
from pathlib import Path
from skimage.color import deltaE_ciede2000


max_allowed_error = 10**-4
csv_file = Path('tests/deltaE00_test_data.csv')

with open(csv_file, "r") as f:

    data = csv.reader(f)

    for row in data:
        lab_a = [float(r) for r in row[0:3]]
        lab_b = [float(r) for r in row[3:6]]
        delta_e_ref = float(row[6])
        delta_e = deltaE_ciede2000(lab_a, lab_b)
        abs_error = abs(delta_e_ref - delta_e)
        print(f'Colors {lab_a} and {lab_b} have an abs error in deltaE of {abs_error}')
