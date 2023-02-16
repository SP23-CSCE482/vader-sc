from functiondefextractor import core_extractor
from transformers import RobertaTokenizer, T5ForConditionalGeneration
import inspect
import CommentManipulator

def commentWholeDirectory(directoryName):
    print("Commenting whole directory")
    # Bring in CodeT5 Model
    tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-base-multi-sum')
    model = T5ForConditionalGeneration.from_pretrained('Salesforce/codet5-base-multi-sum')

    # Get source code
    generatedCode = core_extractor.extractor(directoryName)
    print(generatedCode)

    # For each function, generate documentation!
    generatedComments = []
    filenames = [] 
    linenums = [[3, 5, 12], [4, 9, 24, 31], [8, 28, 46, 58, 63]] # These should come from the functiondefextractor below obviously, just hardcoded now to check
    
    for index, row in generatedCode.iterrows():
        text = row['Code']

        # See which function it belongs to
        funcName = row['Uniq ID']
        fileName = funcName[ : funcName.find("_", funcName.rfind("/"))]
        if(len(filenames) == 0):
            filenames.append(fileName)
            generatedComments.append([])
        elif(filenames[-1] != fileName):
            filenames.append(fileName)
            generatedComments.append([])

        input_ids = tokenizer(text, return_tensors="pt").input_ids
        generated_ids = model.generate(input_ids, max_length=40)
        print("\n\nFunction: ", funcName)
        generatedComments[-1].append(tokenizer.decode(generated_ids[0], skip_special_tokens=True))
        print("Documentation from CodeT5: ", generatedComments[-1][-1], "\n")
        
    print("\nNow inserting these generated comments into the files!")

    for curFile in range(len(generatedComments)):
        CommentManipulator.insertCommentsAtLines(filenames[curFile], linenums[curFile], generatedComments[curFile])
