def parsefile(filename):
    file = open(filename)

    current_indent_level = 0

    current_character = ""
    current_buffer = ""

    conversations = []

    for line in file:
        line = line.replace("\r", "")
        line = line.replace("\n", "")

        indent_level = 0
        while (indent_level < len(line) and line[indent_level] == "\t"):
            indent_level += 1

        append = current_indent_level == indent_level

        if not append and current_buffer != "":
            conversation = {
                'character': current_character,
                'text': current_buffer
            }
            current_buffer = ""
            conversations.append(conversation)

        current_indent_level = indent_level
        line = line.replace("\t", "")
        if indent_level == 5:
            current_character = line
        elif indent_level == 3:
            current_buffer += " " + line
        
    file.close()
    return conversations