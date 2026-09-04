import csv
from pathlib import Path

from skimage.color import deltaE_ciede2000

REF_PATH = Path(__file__).parent / 'ref'
MAX_ALLOWED_ERROR = 10**-4
CSV_FILE = REF_PATH / 'deltaE00_test_data.csv'  # data obtained in https://hajim.rochester.edu/ece/sites/gsharma/ciede2000/dataNprograms/ciede2000testdata.txt


def test_detae00():

    with open(CSV_FILE, "r") as f:
        data = csv.reader(f)
        for row in data:
            lab_a = [float(r) for r in row[0:3]]
            lab_b = [float(r) for r in row[3:6]]
            delta_e_ref = float(row[6])
            delta_e = deltaE_ciede2000(lab_a, lab_b)
            abs_error = abs(delta_e_ref - delta_e)
            assert abs_error <= MAX_ALLOWED_ERROR
