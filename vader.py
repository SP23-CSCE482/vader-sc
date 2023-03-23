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
        overwrite_files: bool = typer.Option(False, "--overwrite-files", help = "Default False; overwrites original files with generated comments instead of creating new ones"),
        non_recursive: bool = typer.Option(False, "--non-recursive", help = "Default False; only generate comments for files in immediate directory and not children directories"),
        verbose: bool = typer.Option(False, "--verbose", help = "Default False; display verbose output during program execution"),
        new_directories: bool = typer.Option(False, "--new-directories", help = "Default False; creates new directories within which to put code with generated comments")
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
        code_info_df = core_extractor.extractor(directory, ignoreDocumented = ignore_documented, removeCppSignatures = remove_cpp_signatures, non_recursive = non_recursive, verbose=verbose)
        parsed_dict = parse_df_to_dict(code_info_df)

    pprint(f"Found [bold green]{code_info_df.shape[0]}[/bold green] functions in [bold green]{len(parsed_dict.keys())}[/bold green] files")


    # Retrieve Model
    tokenizer = None
    model = None

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), redirect_stdout=verbose)  as progress_model:
        progress_model.add_task(description="Setting up Model (This may take a while)", total=None)
        tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-base-multi-sum')
        model = T5ForConditionalGeneration.from_pretrained('.')
    

    # Inference
    for key in track(parsed_dict.keys(), "Generating Comments..."):
        for index, code_info in enumerate(parsed_dict[key]):
            input_ids = tokenizer(code_info["code"][:512], return_tensors="pt").input_ids
            generated_ids = model.generate(input_ids, max_length=512)
            parsed_dict[key][index]["generated_comment"] = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
            if(verbose): pprint(f"Comment generated for " + key)  

    # Saving File
    for key in track(parsed_dict.keys(), "Saving Comments..."):
        parsed_dict[key].sort(key=lambda x: x["line_no"])
        if(new_directories):
            if (not (os.path.isdir(key[:key.rfind("/")] + "/VaderSC_Commented"))):
                os.mkdir(key[:key.rfind("/")] + "/VaderSC_Commented")
            mod_file_name = key[:key.rfind("/")] + "/VaderSC_Commented" + key[key.rfind("/") : key.rfind(".")] + "_mod" + key[key.rfind("."):]
        else:
            mod_file_name = key[:key.rfind(".")] + "_mod" + key[key.rfind("."):]
        line_counter = 1
        array_counter = 0
        if (os.path.isfile(key)):
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
                    if(verbose): pprint(f"Comment inserted for " + key)
            if(overwrite_files):
                os.remove(key)
                os.rename(mod_file_name, key)
    
    pprint(f"Created [bold green]{len(parsed_dict)}[/bold green] files")


if __name__ == '__main__':
    typer.run(main)