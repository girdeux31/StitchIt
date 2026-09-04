# scripts/prepare_pypi_readme.py
import re
from pathlib import Path

readme_file = Path('../README.md')
readme_pypi_file = Path('../README.pypi.md')

with open(readme_file, "r", encoding="utf-8") as f:
    content = f.read()

# Convert > [!NOTE] -> > **Note:**
# Convert > [!WARNING] -> > **Warning:**
content = re.sub(
    r">\s*\[!(NOTE|WARNING|IMPORTANT|TIP|CAUTION)\]",
    r"> **\1:**",
    content,
    flags=re.IGNORECASE
)

with open(readme_pypi_file, "w", encoding="utf-8") as f:
    f.write(content)