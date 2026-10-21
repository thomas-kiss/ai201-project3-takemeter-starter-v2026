"""
Executes only the Unit 5 portion (cells 0-16) of takemeter.ipynb, using
nbclient, then writes the executed cells' outputs back into the real
notebook file, leaving Unit 6+ cells untouched (not needed this unit).
"""
import nbformat
from nbclient import NotebookClient

NB_PATH = "takemeter.ipynb"
UNIT5_END = 17  # cell 17 is the "unit 6 starts here" marker, exclusive

nb = nbformat.read(NB_PATH, as_version=4)
sub_nb = nbformat.v4.new_notebook()
sub_nb.cells = nb.cells[:UNIT5_END]
sub_nb.metadata = nb.metadata

client = NotebookClient(sub_nb, timeout=900, kernel_name="takemeter-venv")
client.execute()

for i in range(UNIT5_END):
    nb.cells[i] = sub_nb.cells[i]

nbformat.write(nb, NB_PATH)
print("Executed and saved Unit 5 cells (0-16) back into takemeter.ipynb.")
