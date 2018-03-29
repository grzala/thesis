# This script parses the script into a data structure usable by other modules

def parsefile(filename):
    # Open the file
    file = open(filename)

    current_indent_level = 0 # Remember the indentation level

    current_character = "" 
    current_buffer = "" # Append dialogue line until indentation level changes

    conversations = [] # The result

    for line in file:
        # Remove newline characters
        line = line.replace("\r", "")
        line = line.replace("\n", "")

        # Find out the indentation level of the current line
        indent_level = 0
        while (indent_level < len(line) and line[indent_level] == "\t"):
            indent_level += 1

        # If indentation level does not change, append text to dialogue line
        append = current_indent_level == indent_level

        # if indentation level changes, save the current buffer of dialogue line and attach character to it
        if not append and current_buffer != "":
            conversation = {
                'character': current_character,
                'text': current_buffer
            }
            current_buffer = ""
            conversations.append(conversation)

        current_indent_level = indent_level
        line = line.replace("\t", "")
        if indent_level == 5: # Characters are specified at level 5 of indentation
            current_character = line
        elif indent_level == 3: # Dialogue is specified at level 3 of indentation
            current_buffer += " " + line
        
    file.close()
    return conversations