from FunctionExtract import core_extractor
from transformers import GPTJForCausalLM, GPT2Tokenizer
import inspect
import sys
import typer
from pathlib import Path
from rich import print as pprint, console
from rich.progress import Progress, SpinnerColumn, TextColumn, track
from multishot import multi_shot_primer
import pandas as pd
import os
import torch

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
        non_recursive: bool = typer.Option(False, "--non-recursive", help = "Default False; only generate comments for files in immediate directory and not children directories")
        ):

    use_mps = False
    device = None
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    pprint(f"Using [bold green]{device}[/bold green] for inference")
    
    
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
        code_info_df = core_extractor.extractor(directory, ignoreDocumented = ignore_documented, removeCppSignatures = remove_cpp_signatures, non_recursive = non_recursive)
        parsed_dict = parse_df_to_dict(code_info_df)

    pprint(f"Found [bold green]{code_info_df.shape[0]}[/bold green] functions in [bold green]{len(parsed_dict.keys())}[/bold green] files")
    
    # Retrieve Model
    tokenizer = None
    model = None

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"))  as progress_model:
        progress_model.add_task(description="Setting up Model (This may take a while)", total=None)
        if use_mps:
            model = GPTJForCausalLM.from_pretrained('EleutherAI/gpt-j-6B', torch_dtype=torch.float16).to(device)
        else:
            model = GPTJForCausalLM.from_pretrained('EleutherAI/gpt-j-6B', torch_dtype=torch.float16).to(device)
        tokenizer = GPT2Tokenizer.from_pretrained('EleutherAI/gpt-j-6B')
    

    # Inference
    for key in track(parsed_dict.keys(), "Generating Comments..."):
        for index, code_info in enumerate(parsed_dict[key]):
            input_ids = tokenizer.encode(multi_shot_primer+code_info["code"][:1250]+"\n<--CODE_END 3-->\n<--COMMENT 3-->\n", return_tensors="pt").to(device)
            generated_ids = model.generate(input_ids, max_new_tokens=300)
            generated_comment = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
            print(generated_comment)
            generated_comment = generated_comment[generated_comment.find("<--COMMENT 3-->")+len("<--COMMENT 3-->"):generated_comment.find("<--COMMENT_END 3-->")]
            parsed_dict[key][index]["generated_comment"] = generated_comment
            del input_ids
    
    # Saving File
    for key in track(parsed_dict.keys(), "Saving Comments..."):
        parsed_dict[key].sort(key=lambda x: x["line_no"])
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
            if(overwrite_files):
                os.remove(key)
                os.rename(mod_file_name, key)
    
    pprint(f"Created [bold green]{len(parsed_dict)}[/bold green] files")


if __name__ == '__main__':
    typer.run(main)
