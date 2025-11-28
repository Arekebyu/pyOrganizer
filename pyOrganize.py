import typer
import os
from typing_extensions import Annotated
from organize import sortFolders

def pyOrganize(
        path: Annotated[str, typer.Argument(help="Path to folder to organize")],
        instructions: Annotated[str, typer.Argument(help="additional sorting instructions enclosed by double quotes (\"\")")]
):
    directory_content = os.listdir(path)
    files = [f for f in directory_content if os.path.isfile(os.path.join(path, f))]
    folders = [f for f in directory_content if os.path.isdir(os.path.join(path, f))]
    
    sortFolders(files, folders, instructions)




