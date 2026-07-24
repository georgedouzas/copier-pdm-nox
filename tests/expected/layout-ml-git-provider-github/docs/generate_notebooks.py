"""Copy the notebooks into the documentation tree so they render as pages.

The notebooks live at the repository root, where they are worked in and where the test suite
executes them. Documentation can only reference files under `docs`, so they are copied into
the virtual documentation tree at build time rather than duplicated on disk.
"""

from pathlib import Path

import mkdocs_gen_files

for notebook in sorted(Path('notebooks').glob('*.ipynb')):
    with mkdocs_gen_files.open(f'notebooks/{notebook.name}', 'wb') as destination:
        destination.write(notebook.read_bytes())
    mkdocs_gen_files.set_edit_path(f'notebooks/{notebook.name}', Path('../') / notebook)
