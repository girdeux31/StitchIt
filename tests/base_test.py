import os
import sys
import shutil

from pathlib import Path


REF_PATH = Path('tests/ref')
TMP_PATH = Path('tests/tmp')

def compare_files(file_a: Path, file_b: Path):
    """Return True if files match, False otherwise"""
    with open(file_a, 'r', encoding="utf8") as f:
            text_a = f.read()

    with open(file_b, 'r', encoding="utf8") as f:
            text_b = f.read()

    return True if text_a == text_b else False

def assert_output(inp_name: Path, tmp_file: Path):
    """Check that output files exists and that svg and txt don't change"""
    # pdf_file = tmp_file.with_stem(f'{tmp_file.stem}_chart').with_suffix('.pdf')
    # png_file = tmp_file.with_stem(f'{tmp_file.stem}_chart').with_suffix('.png')
    svg_file = tmp_file.with_stem(f'{tmp_file.stem}_chart').with_suffix('.svg')
    txt_file = tmp_file.with_stem(f'{tmp_file.stem}_info').with_suffix('.txt')
    svg_ref_file = REF_PATH / inp_name.stem / svg_file.name
    txt_ref_file = REF_PATH / inp_name.stem / txt_file.name

    # assert pdf_file.exists()
    # assert png_file.exists()
    assert svg_file.exists()
    assert txt_file.exists()
    assert compare_files(svg_ref_file, svg_file)
    assert compare_files(txt_ref_file, txt_file)

def clean_tmp_files(tmp_file: Path):
    """Remove files generated previously by test"""
    base_name = tmp_file.with_suffix('').name
    files = os.listdir(tmp_file.parent)
    for file in files:
        if file.startswith(base_name):
             os.remove(tmp_file.parent / file)

def setup_method(request, inp_name: Path, args: dict) -> None:
    """Perform setup for all tests"""
    test_name = request.node.name.replace('test_', '')
    ref_file, tmp_file = _setup_files(inp_name, test_name)
    clean_tmp_files(tmp_file)
    shutil.copyfile(ref_file, tmp_file)
    _setup_args(tmp_file, args)
    return tmp_file

def _setup_files(inp_name: Path, test_name: str):
    """Setup input and temp file"""
    tmp_name = f'{inp_name.stem}_{test_name}{inp_name.suffix}'
    ref_file = REF_PATH / inp_name
    tmp_file = TMP_PATH / inp_name.stem / tmp_name
    return ref_file, tmp_file

def _setup_args(ref_file: Path, args: dict[str, str | int | float]) -> None:
    """Set user input parameters as sys arguments"""
    del sys.argv[1:]  # reset args
    args['input-file'] = str(ref_file)
    args['no-pdf'] = None  # do not generate pdf or png
    args['no-png'] = None
    for key, value in args.items():
        sys.argv.append(f'--{key}')
        if value is not None:
            sys.argv.append(str(value))
