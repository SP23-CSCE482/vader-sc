from functiondefextractor import core_extractor
from transformers import RobertaTokenizer, T5ForConditionalGeneration
import inspect

# Bring in CodeT5 Model
tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-base-multi-sum')
model = T5ForConditionalGeneration.from_pretrained('Salesforce/codet5-base-multi-sum')

# Get source code
generatedCode = core_extractor.extractor(r"Sample_Code")
print(generatedCode)

# For each function, generate documentation!
for index, row in generatedCode.iterrows():
    text = row['Code']
    input_ids = tokenizer(text, return_tensors="pt").input_ids
    generated_ids = model.generate(input_ids, max_length=40)
    print("\n\nFunction: ", row['Uniq ID'])
    print("Documentation from CodeT5: ",tokenizer.decode(generated_ids[0], skip_special_tokens=True), "\n")
    