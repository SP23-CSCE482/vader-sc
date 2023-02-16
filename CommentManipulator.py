'''
Inserts specified comments into a specified file at a specified line number. 
It will insert a new line before and after each one so 
that they are guaranteed to be on their own line.
'''
def insertCommentsAtLines(filename, lines, comments):
    print(filename)
    print(lines)
    print(comments)
    commentStarter = "// "
    if(filename[filename.rfind("."):] == ".py"):
        commentStarter = "# "
    if(len(lines) != len(comments)):
        print("Should be the same number of line numbers as comments, but isn't")

    curComment = 0
    with open(filename, 'r+') as openedFile:
        readLines = openedFile.readlines()
        for i, linenum in enumerate(lines):
            if(i < len(comments)):
                readLines.insert(linenum + i, "\n" + commentStarter + comments[i] + "\n")
    
    with open(filename[:filename.rfind("/")] + "_Results" + filename[filename.rfind("/"):filename.rfind(".")] + "_COMMENTED" + filename[filename.rfind("."):], 'w') as openedFile:
        openedFile.writelines(readLines)