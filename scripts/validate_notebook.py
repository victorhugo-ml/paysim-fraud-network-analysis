"""Static validation for the portfolio notebook.

The full analysis downloads a large external dataset and is intentionally not
executed in CI. This script validates the committed notebook structure, code
syntax, outputs and publication-safety invariants.
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "paysim_fraud_network_analysis.ipynb"
REQUIRED_IMAGES = (
    ROOT / "docs" / "images" / "fraudes-por-tipo.png",
    ROOT / "docs" / "images" / "maior-componente.png",
    ROOT / "docs" / "images" / "subgrafo-fraudes.png",
    ROOT / "docs" / "images" / "correlacao-metricas.png",
)

REQUIRED_TEXT = (
    "Pergunta de pesquisa",
    "Limitação metodológica essencial",
    "Resultados empíricos desta execução",
    "Como apresentar este projeto",
)

FORBIDDEN_PATTERNS = {
    "portfolio placeholder": re.compile(r"preencher após executar", re.I),
    "Windows user path": re.compile(r"[A-Z]:\\\\Users\\\\", re.I),
    "Unix user path": re.compile(r"/(?:home|Users)/[^/\s]+/"),
    "credential assignment": re.compile(
        r"(?:api[_-]?key|client[_-]?secret|password|token)\s*[=:]\s*['\"][^'\"]+",
        re.I,
    ),
}


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))

    if notebook.get("nbformat") != 4:
        raise AssertionError("Expected notebook format 4")

    cells = notebook.get("cells")
    if not isinstance(cells, list) or not cells:
        raise AssertionError("Notebook has no cells")

    full_text = "\n".join("".join(cell.get("source", [])) for cell in cells)

    for required in REQUIRED_TEXT:
        if required not in full_text:
            raise AssertionError(f"Missing required section: {required}")

    for label, pattern in FORBIDDEN_PATTERNS.items():
        if pattern.search(full_text):
            raise AssertionError(f"Forbidden content found: {label}")

    for index, cell in enumerate(cells):
        if cell.get("cell_type") == "code":
            source = "".join(cell.get("source", []))
            try:
                ast.parse(source)
            except SyntaxError as error:
                raise AssertionError(
                    f"Invalid Python syntax in code cell {index}: {error}"
                ) from error

        for output in cell.get("outputs", []):
            if output.get("output_type") == "error":
                raise AssertionError(f"Error output committed in cell {index}")

    for image in REQUIRED_IMAGES:
        if not image.is_file() or image.stat().st_size == 0:
            raise AssertionError(f"Missing or empty image: {image.relative_to(ROOT)}")

    print(
        f"Notebook OK: {len(cells)} cells, "
        f"{sum(cell.get('cell_type') == 'code' for cell in cells)} code cells"
    )


if __name__ == "__main__":
    main()
