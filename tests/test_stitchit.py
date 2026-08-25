import os
import shutil
from pathlib import Path
from stitchit import stitchit


REF_PATH = Path('tests/ref')
TMP_PATH = Path('tests/tmp')
IN_FILE = Path('bird.jpg')
N_COLORS = 4
STITCHES_PER_ROW = 20

def compare_files(file_a: Path, file_b: Path):
    """Return True if files match, False otherwise"""
    with open(file_a, 'r', encoding="utf8") as f:
            text_a = f.read()

    with open(file_b, 'r', encoding="utf8") as f:
            text_b = f.read()

    return True if text_a == text_b else False

def assert_output(file_name: str, test_name: str):
    """Check that output files exists and that svg and txt don't change"""
    tmp_file = TMP_PATH / file_name
    pdf_file = tmp_file.with_stem(f'{tmp_file.stem}_pattern').with_suffix('.pdf')
    png_file = tmp_file.with_stem(f'{tmp_file.stem}_pattern').with_suffix('.png')
    svg_file = tmp_file.with_stem(f'{tmp_file.stem}_pattern').with_suffix('.svg')
    txt_file = tmp_file.with_stem(f'{tmp_file.stem}_info').with_suffix('.txt')
    svg_ref_file = REF_PATH / f'{svg_file.stem}_{test_name}.svg'
    txt_ref_file = REF_PATH / f'{txt_file.stem}_{test_name}.txt'

    assert pdf_file.exists()
    assert png_file.exists()
    assert svg_file.exists()
    assert txt_file.exists()
    assert compare_files(svg_ref_file, svg_file)
    assert compare_files(txt_ref_file, txt_file)

def clean_tmp_files(file_name: str):
    """Remove files generated previously by test"""
    tmp_file = TMP_PATH / file_name
    base_name = tmp_file.with_suffix('').name
    files = os.listdir(tmp_file.parent)
    for file in files:
        if file.startswith(base_name):
             os.remove(tmp_file.parent / file)     

def test_default_values(request):
    tmp_file = TMP_PATH / IN_FILE
    test_name = request.node.name.replace('test_', '')
    clean_tmp_files(IN_FILE)
    shutil.copyfile(REF_PATH / IN_FILE, tmp_file)
    stitchit(tmp_file, N_COLORS, STITCHES_PER_ROW)
    assert_output(IN_FILE, test_name)

def test_no_colors(request):
    tmp_file = TMP_PATH / IN_FILE
    test_name = request.node.name.replace('test_', '')
    clean_tmp_files(IN_FILE)
    shutil.copyfile(REF_PATH / IN_FILE, tmp_file)
    stitchit(tmp_file, N_COLORS, STITCHES_PER_ROW, show_colors=False)
    assert_output(IN_FILE, test_name)

def test_no_symbols(request):
    tmp_file = TMP_PATH / IN_FILE
    test_name = request.node.name.replace('test_', '')
    clean_tmp_files(IN_FILE)
    shutil.copyfile(REF_PATH / IN_FILE, tmp_file)
    stitchit(tmp_file, N_COLORS, STITCHES_PER_ROW, show_symbols=False)
    assert_output(IN_FILE, test_name)

def test_no_legend(request):
    tmp_file = TMP_PATH / IN_FILE
    test_name = request.node.name.replace('test_', '')
    clean_tmp_files(IN_FILE)
    shutil.copyfile(REF_PATH / IN_FILE, tmp_file)
    stitchit(tmp_file, N_COLORS, STITCHES_PER_ROW, show_legend=False)
    assert_output(IN_FILE, test_name)

def test_all_false(request):
    tmp_file = TMP_PATH / IN_FILE
    test_name = request.node.name.replace('test_', '')
    clean_tmp_files(IN_FILE)
    shutil.copyfile(REF_PATH / IN_FILE, tmp_file)
    stitchit(tmp_file, N_COLORS, STITCHES_PER_ROW, show_colors=False, show_symbols=False, show_legend=False)
    assert_output(IN_FILE, test_name)