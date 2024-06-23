from dataclasses import dataclass,field
from typing import List
import os

@dataclass
class File:
    filename:str=field(default_factory=str)
    file:str=field(default_factory=str)
    types:str=field(default_factory=str)
    size:str=field(default_factory=str)

class FileHandler:

    def __init__(self,request) -> None:
        self.request=request
    
    def get_files(self)->List[File]:
        file=self.request.files
        files=[]
        for key,values in file.items():
            files.append(
                File(
                    filename=values['filename'],
                    file=values['file'],
                    types=values['type'],
                    size=values['size']
                )
            )
        return files
    
    def write_file(self,file:File,write_mode:str="wb",dir:str="media")->None:
        file_binary=file.file
        if not os.path.exists(dir):
            os.makedirs(dir) 
        file_path=dir+"/"+file.filename
        with open(file_path,write_mode) as f:
            f.write(file_binary)
        return