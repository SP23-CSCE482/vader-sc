# Vader-SC
This is the repository for VADER-SC - A project to increase source code readability. <br />
VaderSC is an automatic source code comment generation tool that leverages transformer-based and LLM models such as T5 and GPT. It generates human-readable and meaningful comments for various programming languages such as Python, C++, and Java.


## Installation Script
* Make sure you are not in any existing python environments and that you atleast have python 3.6 installed
* To install using the script you must be root and you must run ```chmod +x install.sh && sudo ./install.sh``` inside the folder.
* You must download the model when prompted so the program runs properly (~800+ MB).
* You can add alias to the program by running ```alias vader-sc='$PWD/SC_Venv/bin/python3 $PWD/vader.py'``` so it can be used anywhere
* To run the program without an alias you can do ```source SC_Venv/bin/activate``` and then use ```python3 vader.py```.
* If you can't get our custom Vader model to work, please rerun the installation script and download the model when prompted or get it [here](https://storage.googleapis.com/model_bucket_for_capstone_tamu/pytorch_model.bin) and place it in ```models/custom_t5```
* if you have any issues with the Installation script please do a manual installation.

## Manual Installation
* If you don't have ctags installed (which is a system requirement to run the philips parser), run ```sudo apt-get install exuberant-ctags```
* To run the gui, you need to install python3-tk as well
* Run ```sudo apt-get install python3-tk```
* cd into the directory vader-sc 
* create a virtual environment, and install the requirements. 
  * Run ```python3 -m venv SC_Venv && source SC_Venv/bin/activate && python -m pip install --upgrade pip && pip install -r requirements.txt -vvv```  
* Download the model from [here](https://storage.googleapis.com/model_bucket_for_capstone_tamu/pytorch_model.bin) and place it in ```models/custom_t5```


## Usage

To use VaderSC, follow these steps:

1. Navigate to the project directory in your command prompt or terminal.

2. Run the program with the following command, replacing `<directory>` with the path to your source code directory: <br />
```python vader.py <directory>```

You can also use the following optional flags to customize the tool's behavior:

- `--ignore-documented`: Ignore functions that already have comments (default: False).
- `--remove-cpp-signatures`: Remove C++ function signatures before processing (default: False).
- `--overwrite-files`: Overwrite original files with generated comments instead of creating new ones (default: False).
- `--non-recursive`: Only generate comments for files in the immediate directory, not subdirectories (default: False).
- `--verbose`: Display verbose output during program execution (default: False).
- `--new-output`: Create a new folder with the code and generated comments (default: False).
- `--cuda`: Use NVIDIA GPU for inference (default: False).
- `--custom-t5-model`: Customize the T5 model used for inference (default: T5-Base). Can be a local path or HugginFace model.
- `--custom-llm-model`: Customize the LLM (GPT-2) model used for inference (default: None). Can be a local path or HugginFace model.
- `--llm-style`: Change the comment style for LLM models (default: DOCSTYLE).
- `--out-name`: Specify the output folder name for the generated comments and code (default: VaderSC_Commented).

## Customization

You can customize the behavior of VaderSC by modifying the options as described above. For example, you can choose between using a T5 or LLM model for inference, decide whether to overwrite original files or create new ones, and more. Here are some tips.

* The CLI will automatically default to our Custom T5 model if downloaded correctly, if not the CLI will automatically install Salesforce's T5-Base.
* If you have trained a T5 or LLM model (that is compatible with HugginFace Transformers) you can put it in models and select with the `--custom-t5-model` or the `--custom-llm-model` arguments.
* You can easily use pretrained HugginFace CasualLM and T5Conditional models using `--custom-t5-model` and `--custom-llm-model` arguments.
* If you would like to speedup inferences and have correctly installed CUDA drivers, you can use `--cuda` flag to use it for inference.
* The CLI has built in multishot learning for LLM. This will allow the model copy the style based on its learning set. You can define your own set in `multishot.py`. Note you will have to share tokens with the code and generated comment. This means if your multishot set is 1500 tokens and your model's max tokens is 2048. Then you will have only 248 tokens left for code since generation takes up to 300 tokens. 
* The CLI supports LLaMa models, although since it is only in bleeding edge "main" version of HugginFace Transformers it may not be stable. There might be some extra output due to some inconsistencies. 
* For CodeT5 models and C++ code, it may be better to remove function signatures since the training data did not have any C++ code.
## Examples

Here are some examples of the comments generated using our CLI with GPTJ, Custom T5 model, LlaMa-14b, and CodeT5. Docstring.ai is also shown for comparison.

1. `python vader.py 441-code/ --new-output --cuda --out-name "./Results/T5Custom"`<br />
```CODE ```
2. `python vader.py 441-code/ --new-output --cuda --out-name "./Results/T5Base" --custom-t5-model "Salesforce/codet5-base-multi-sum"`<br />
 ```CODE ```
3. `python vader.py 441-code/ --new-output --cuda --out-name "./Results/gptj" --custom-llm-model "EleutherAI/gpt-j-6B"`<br />
```CODE ```
4. `python vader.py 441-code/ --new-output --cuda --out-name "./Results/gptjaiStyle" --custom-llm-model "EleutherAI/gpt-j-6B" --llm-style "DOCSTRING.AI"`<br />
```CODE ```
5. `python vader.py 441-code/ --new-output --cuda --out-name "./Results/llama" --custom-llm-model "decapoda-research/llama-13b-hf"`<br />
```CODE ```
6. `python vader.py 441-code/ --new-output --cuda --out-name "./Results/llamaaiStyle" --custom-llm-model "decapoda-research/llama-13b-hf" --llm-style "DOCSTRING.AI"`<br />
```CODE ```
7. `DOCSTRING.ai`<br />
```CODE ```

## Limitations and Issues

1.	Training Data: The performance of these models heavily depends on the quality and variety of the training data. If the training data is biased or lacks representation from certain programming languages or coding styles, the generated comments may not be accurate or helpful.
2.	Multishot Learning: While multishot learning allows the model to leverage previous examples to generate better output, it may not always produce the desired results. If the provided context is not sufficient or is irrelevant, the model might generate comments that are not helpful or even incorrect.
3.	CodeT5 Flexibility: CodeT5 is specifically designed for code understanding tasks, and while it is powerful in many aspects, it may lack the flexibility to adapt to different commenting styles or conventions. This could result in generated comments that may not adhere to a specific style guide or match the preferences of individual developers.
4.	Incomplete or Incorrect Understanding: Language models may sometimes fail to understand complex or unique code structures, resulting in comments that do not accurately describe the code's purpose or functionality. This limitation can be more prominent if the code uses non-standard or domain-specific libraries, techniques, or conventions.
5.	Token Limitations: Models like GPT-J have token limitations (e.g., 2048 tokens for GPT-J). This constraint can impact the quality and accuracy of generated comments, especially when processing long code snippets or when the total number of tokens, including input and output, exceeds the model's limit.
6.	Computational Resources: Generating comments using large models can be resource-intensive, requiring powerful hardware and potentially long processing times. This can limit the practicality of using these models for real-time code commenting or in resource-constrained environments.

## Future
One possible direction for improvement is to curate and expand the training data, ensuring a diverse and representative sample of programming languages, coding styles, and commenting conventions. This will improve the model's ability to generate accurate and helpful comments across various programming scenarios.

Exploring alternative models or fine-tuning the existing models, such as CodeT5 or GPT-J, with domain-specific knowledge or custom training data can also lead to better performance in code commenting tasks. Continuous research in the field of natural language processing and code understanding will likely yield new models and techniques that can be incorporated into the CLI program for improved results.

Another potential enhancement is transitioning from a CLI-based program to an online service. By offering the code commenting functionality as a web-based service or API, users would no longer be limited by their local computational resources. Instead, the service could leverage powerful cloud-based infrastructure to provide faster and more efficient code commenting capabilities. This would also make it easier to integrate the service with popular code editors, IDEs, or development platforms, further streamlining the code commenting process for developers.

## License
None for now, FYI we used PhillipsExtractor which is under MIT license.
