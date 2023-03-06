from FunctionExtract import core_extractor
from transformers import RobertaTokenizer, T5ForConditionalGeneration
import inspect
import sys
import typer
from pathlib import Path
from rich import print as pprint, console
from rich.progress import Progress, SpinnerColumn, TextColumn, track
import pandas as pd
import os
import itertools


def parse_df_to_dict(code_dataframe: pd.DataFrame):
    """ Function Makes the Pandas DataFrame into something more parsable
        @parameters
        code_dataframe: the dataframe generated by the extractor
        @return
        This function returns a dictionary where the keys are the filepaths and the values are dictionaries of
        the code and line numbers
    """
    parsed_data = {}
    for file_id, code, line in zip(code_dataframe["Uniq ID"], code_dataframe["Code"], code_dataframe["Line"]):
        og_file_name = file_id[:file_id.find("_", file_id.rfind("."))]
        if og_file_name in parsed_data:
            parsed_data[og_file_name].append({"code":code, "line_no":line})
        else:
            parsed_data[og_file_name] = [{"code":code, "line_no":line}]
    return parsed_data

#languages
COMMENT_MAP = {
    ".PY": "#",
    ".CPP": "//",
    ".JAVA": "//"
}


def main(
        directory: Path = typer.Argument(..., help="Directory of Source code to Parse"),
        ignore_documented: bool = typer.Option(False, "--ignore-documented", help = "Default False; ignores documented functions"),
        remove_cpp_signatures: bool = typer.Option(False, "--remove-cpp-signatures", help = "Default False; removes signatures of C++ functions before processing"),
        create_ml_dataset: bool = typer.Option(False, "--create-ml-dataset", help = "Default False; creates an ML dataset of the given directory"),
        overwrite_files: bool = typer.Option(False, "--overwrite-files", help = "Default False; overwrites original files with generated comments instead of creating new ones"),
        non_recursive: bool = typer.Option(False, "--non-recursive", help = "Default False; only generate comments for files in immediate directory and not children directories")
        ):
    
    if not directory.is_dir():
        pprint("[bold red]Must be a directory[/bold red]")
        raise typer.Exit()
    # Code Extracting
    code_info_df = None

    # Transform Data
    parsed_dict = {}

    pprint(f"Generating comments for [bold green]{directory}[/bold green]")

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"))  as progress_parsing:
        progress_parsing.add_task(description="Extracting Functions", total=None)
        progress_parsing.add_task(description="Parsing Functions", total=None)
        code_info_df = core_extractor.extractor(directory, ignoreDocumented = ignore_documented, removeCppSignatures = remove_cpp_signatures) if not create_ml_dataset else core_extractor.extractor(directory, ignoreDocumented = ignore_documented, removeCppSignatures = remove_cpp_signatures)
        # print(code_info_df)
    parsed_dict = parse_df_to_dict(code_info_df) if not create_ml_dataset else code_info_df.loc[:,"Code"]
    # print(parsed_dict)

    pprint(f"Found [bold green]{code_info_df.shape[0]}[/bold green] functions in [bold green]{len(parsed_dict.keys())}[/bold green] files")

    if(create_ml_dataset):
        linenums = code_info_df.loc[:,"Line"]
        funcnames = code_info_df.loc[:,"Uniq ID"]
        curFunc = 0
        if (os.path.isfile("ML_CodeComments.txt")): os.remove("ML_CodeComments.txt")
        with open("ML_CodeComments.txt", "w") as txt_file:
            for key in track(parsed_dict.keys(), "Saving Code/Comment pairs..."):
                filet = funcnames[curFunc][ : funcnames[curFunc].find("_", funcnames[curFunc].rfind("."))]
                # print(funcnames[curFunc])
                with open(filet, "r") as curFile:
                    # fromLineNum = list(itertools.islice(curFile, (max(linenums[curFunc] - 14, 0))))
                    fromLineNum = curFile.readlines()[(max(linenums[curFunc] - 14, 0)) : linenums[curFunc]]
                    comment = ""
                    breakNext = False
                    for line in fromLineNum:
                        if line[0:3] == "///":
                            comment += line
                            breakNext = True
                        elif breakNext == True:
                            break
                if(comment != ""):
                    txt_file.write("CODE:\n")
                    txt_file.write(parsed_dict[key])
                    txt_file.write("COMMENT:\n")
                    txt_file.write(comment)
                    txt_file.write("\n\n\n")
                curFunc += 1
        return

    # Retrieve Model
    tokenizer = None
    model = None

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"))  as progress_model:
        progress_model.add_task(description="Setting up Model (this may take a while)", total=None)
        tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-large')
        model = T5ForConditionalGeneration.from_pretrained('Salesforce/codet5-large')
    

    # Inference
    for key in track(parsed_dict.keys(), "Generating Comments..."):
        for index, code_info in enumerate(parsed_dict[key]):
            input_ids = tokenizer(code_info["code"][:512], return_tensors="pt").input_ids
            generated_ids = model.generate(input_ids, max_length=512)
            parsed_dict[key][index]["generated_comment"] = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    
    # Saving File
    for key in track(parsed_dict.keys(), "Saving Comments..."):
        parsed_dict[key].sort(key=lambda x: x["line_no"])
        mod_file_name = key[:key.rfind(".")] + "_mod" + key[key.rfind("."):]
        line_counter = 1
        array_counter = 0
        with open(key, "r") as og_file:
            with open(mod_file_name, "w") as mod_file:
                while(array_counter != len(parsed_dict[key])):
                    file_ending = Path(key).suffix.upper()
                    if(parsed_dict[key][array_counter]["line_no"] == line_counter):
                        mod_file.write(f"{COMMENT_MAP[file_ending]} Generated: {parsed_dict[key][array_counter]['generated_comment']}\n")
                        array_counter +=1
                    else:
                        mod_file.write(og_file.readline())
                        line_counter +=1
                mod_file.write(og_file.read())
    
    pprint(f"Created [bold green]{len(parsed_dict)}[/bold green] files")


if __name__ == '__main__':
    typer.run(main)