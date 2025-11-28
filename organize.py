from pydantic import BaseModel, Field
from typing import List
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import shutil

class FileCategory(BaseModel):
    """A single file mapped to its categorized folder name."""
    file_name: str = Field(description="The exact name of the file provided in the input list.")
    destination_folder: str = Field(description="A concise, logical folder name (category) for this file.")

class SortingResult(BaseModel):
    """The complete result containing a list of all categorized files."""
    categorized_files: List[FileCategory] = Field(
        description="A list of objects, where each object maps an input file name to its suggested folder."
    )

def sortFolders(files: list[str], folders: list[str], instructions: str):
    parser = PydanticOutputParser(pydantic_object=SortingResult)
    format_instructions = parser.get_format_instructions()
    load_dotenv()
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature = 0.2360679775,
        api_key=os.getenv('GROQ_API_KEY'),
    )
    parser = PydanticOutputParser(pydantic_object=SortingResult)
    format_instructions = parser.get_format_instructions()

    prompt = PromptTemplate(
        template="You are a file organizer, analyze the following request and generate appropriate folder names, then sort the files into appropriate folders.\n\n{format_instructions}\n\n files to categorize: {file_list}\n\n existing folders: {existing_folders}, \n\n user requests: {user_request}",
        input_variables=["file_list", "user_request", "existing_folders"],
        partial_variables={"format_instructions": format_instructions},
    )

    folder_chain = prompt | llm | parser

    ingest = ""
    for file in files:
        ingest += file+"?"
    
    result: SortingResult = folder_chain.invoke({"file_list": ingest, "user_request": instructions, "existing_folders": folders})
    
    for item in result.categorized_files:
        os.mkdir(item.destination_folder)
        shutil.move(item.file_name, item.destination_folder+"/"+item.file_name)
