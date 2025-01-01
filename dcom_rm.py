# Lyndon Zhang dcom_rm.py
# lzha27 251304999
import sys


# Creating a function to check a string to see if it's in the correct format for a date.
def dateFormat(string):
    # Checking if the string is the proper length of a date. If not, return false.
    if len(string) < 10:
        return False
    # Sectioning the string into day, month, and year.
    dayInt = string[:2]
    monthInt = string[3:5]
    yearInt = string[6:10]
    # Checking to see if the day, month, and year are all digits and if the slashes are in the correct locations. If it
    # is, then return the string as a valid date, otherwise return false.
    if string[2] == '/' and string[5] == '/' and dayInt.isdigit() and monthInt.isdigit() and yearInt.isdigit():
        return True
    else:
        return False


# Creating a function to process a file to remove all dated C comments. Uses an input file and creates an output file.
def processCFile(inputFile, outputFile):
    with open(inputFile, 'r') as infile, open(outputFile, 'w') as outfile:
        # Looping every line in our input file.
        previousMulti = False
        for line in infile:
            counter = 0
            singleLineComment = False
            multiLineComment = False
            skipLine = False
            tempLine = line

            # Checking to see which type of comment we are processing. Either a single line comment starting with "//"
            # or a multiline comment starting with "/*". This loops until the string is 9 chars long.
            while len(tempLine) > 9:
                if tempLine.startswith('//'):
                    singleLineComment = True
                    break
                if tempLine.startswith('/*'):
                    multiLineComment = True
                    break
                tempLine = tempLine[1:]
                counter = counter + 1

            # If we are looking at a single line comment, we remove the "//" and strip the string down. We then loop
            # through the string by removing the first character and checking if the first 10 chars are a valid date.
            # If it is, we break from the loop and set skipLine to true. Else do nothing. This loops until we find
            # a date or until the string reaches 9 in length.
            if singleLineComment and not previousMulti:
                commentString = tempLine[2:].strip()
                while len(commentString) > 9:
                    if dateFormat(commentString[:10]):
                        skipLine = True
                        break
                    commentString = commentString[1:]

            # For multi line comments, we add all the lines upcoming to the current line until we reach an ending with
            # "*/". We also add the upcoming lines to the original "line" var to properly skip the multi line comment.
            if multiLineComment and not previousMulti:
                commentString = tempLine[2:].strip()
                while len(commentString) > 9:
                    if dateFormat(commentString[:10]):
                        skipLine = True
                        while not commentString.endswith("*/"):
                            newLine = infile.readline()
                            line = line + newLine
                            commentString = commentString + newLine.strip()
                        break
                    else:
                        previousMulti = True
                    commentString = commentString[1:]

            # If we don't find a date (skipLine) we write the original line from the inputFile. Else, we will write the
            # line up to the "//" or "/*" discovered on the original line from the inputFile.
            if line.strip().endswith("*/"):
                previousMulti = False
            if not skipLine:
                outfile.write(line)
            else:
                outfile.write(line[:counter] + "\n")
                previousMulti = False


# If nothing is inputted, then print usage out. If used properly, run the code using the provided input and output
# file names.
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python dcom_rm.py cInputFileName cOutputFileName")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        processCFile(input_file, output_file)
