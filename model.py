reserved_words = {

    "instructions": {

        "commands": [
            "M",
            "R",
            "C",
            "B",
            "c",
            "b",
            "P",
            "assignTo",
            "goto",
            "move",
            "turn",
            "face",
            "put",
            "pick",
            "moveToThe",
            "moveInDir",
            "jumpToThe",
            "jumpInDir",
            "nop"
        ],

        "control_structures": [
            "if",
            "then",
            "else",
            "while",
            "do",
            "repeat"
        ],

        "procedures": [

        ]

    },

    "keywords": [
        "ROBOT_R",
        "VARS",
        "PROCS"
    ],

    "conditions": [
        "facing",
        "canput",
        "canpick",
        "canmoveindir",
        "canjumpindir",
        "canmovetothe",
        "canjumptothe"
    ],

    "directions": [
        "north",
        "south",
        "east",
        "west",
        "front",
        "back",
        "left",
        "right",
        "around"
    ],

    "objects": [
        "Balloons",
        "Chips"
    ],

    "variables": [

    ]

}

procedures_arguments_receiving = {}

def load_file()->list:
    location = "./program.txt"
    file = open(location)
    line = file.readline()
    lines = []
    while line != "":
        line = line.replace("\n", "").replace("\t", "n")
        lines.append(line)
        line = file.readline()
    return lines

def load_program(program:list)->None:

    n_line = 0
    while n_line <= len(program) - 1:
        element = program[n_line]
        element = element.split(" ")

        if element[0] == "VARS":
            save_variables_names(element)

        elif element[0] == "PROCS":
            n_line += 1
            searching_procs = True
            while searching_procs:
                element = program[n_line].split(" ")
                brackets = {"opened": 0, "closed": 0}
                subelement_pos = 0
                for subelement in element:
                    if subelement == "[":
                        brackets["opened"] = brackets["opened"] + 1
                    elif subelement == "]":
                        brackets["closed"] = brackets["closed"] + 1
                    if subelement_pos == 0 and brackets["opened"] == brackets["closed"]:
                        reserved_words["instructions"]["procedures"].append(subelement.lower())
                    subelement_pos += 1        
                n_line += 1
                if program[n_line+1][0] == "[":
                    searching_procs = False
            reserved_words["instructions"]["procedures"] = save_procs_names(reserved_words["instructions"]["procedures"])

        n_line += 1

    save_arguments_recieiving(program, reserved_words["instructions"]["procedures"])

def save_procs_names(procs:list)->list:
    pos = 0
    while pos <= len(procs)-1:
        proc = procs[pos]
        if proc in reserved_words["instructions"]["commands"] or proc in reserved_words["instructions"]["control_structures"] or proc in reserved_words["keywords"] or proc in reserved_words["conditions"] or proc in reserved_words["directions"] or proc in reserved_words["objects"] or proc in reserved_words["variables"]:
            procs.pop(pos)
        pos += 1
    return procs

def save_variables_names(line:str):
    for element in line:
        if element != "VARS" and element != "," and element != ";":
            valid_name = True
            found_letter = False
            character_position = 0
            for character in element:
                if character.isdigit() and found_letter == False:
                    valid_name = False
                if not character.isdigit() and character_position == 0:
                    found_letter = True
                character_position += 1
            if valid_name:
                reserved_words["variables"].append(element.lower())

def find_program(program:list)->bool:
    output = False
    for line in program:
        if "ROBOT_R" in line:
            output = True
    return output

def validate_variables_and_procs_name(variables:list, procs:list)->bool:
    output = True
    for variable in variables:
        if variable in reserved_words["instructions"]["commands"] or variable in reserved_words["instructions"]["control_structures"] or variable in reserved_words["instructions"]["procedures"] or variable in reserved_words["keywords"] or variable in reserved_words["conditions"] or variable in reserved_words["directions"] or variable in reserved_words["objects"]:
            output = False
    for procedure in procs:
        if procedure in reserved_words["instructions"]["commands"] or procedure in reserved_words["instructions"]["control_structures"] or procedure in reserved_words["variables"] or procedure in reserved_words["keywords"] or procedure in reserved_words["conditions"] or procedure in reserved_words["directions"] or procedure in reserved_words["objects"]:
            output = False
    return output

def save_arguments_recieiving(program:list, procs:list):
    serachin_procs = False
    for line in program:
        opened_arguments = False
        closed_arguments = False
        opened_arguments_pos = 0
        closed_arguments_pos = 0
        symbol_aparition = 0
        if "PROCS" in line:
            serachin_procs = True
        if line[0] == "[":
            serachin_procs = False
        if serachin_procs:
            splited_line = line.split(" ")
            proc = splited_line[0].lower()
            if proc in procs:
                pos = 0
                for char in line:
                    if char == "|":
                        opened_arguments = True
                        opened_arguments_pos = pos
                        symbol_aparition += 1
                    if char == "|" and symbol_aparition == 1:
                        closed_arguments = True
                        closed_arguments_pos = pos
                    pos += 1
                if opened_arguments and closed_arguments:
                    arguments = line[closed_arguments_pos:opened_arguments_pos+1]
                    if "," not in arguments:
                        procedures_arguments_receiving[proc] = 0
                    else:
                        arguments = arguments.split(",")
                        procedures_arguments_receiving[proc] = len(arguments)

def validate_arguments_recieiving(program:list, procs:list)->bool:
    output = True
    executing_instructions_block = False
    for line in program:
        if line[0] == "[":
            executing_instructions_block = True
            continue
        if line[0] == "]":
            executing_instructions_block = False
            continue
        if executing_instructions_block:
            splitted_line = line.split(" ")
            proc = splitted_line[0].lower()
            if proc in procs:
                if "," not in line:
                    if procedures_arguments_receiving[proc] != 0:
                        output = False
                    else:
                        splitted_line = line.split(":")
                        if "" in splitted_line:
                            splitted_line.remove("")
                        if len(splitted_line)-1 != procedures_arguments_receiving[proc]:
                            output = False
                else:
                    splitted_line = line.split(",")
                    if len(splitted_line) != procedures_arguments_receiving[proc]:
                        output = False
    return output

def validate_available_instructions(program:list)->bool:
    output = True
    executing_instructions_block = False
    for line in program:
        if line[0] == "[":
            executing_instructions_block = True
            continue
        if line[0] == "]":
            executing_instructions_block = False
            continue
        if executing_instructions_block:
            splitted_line = line.split(" ")
            instruction = splitted_line[0]
            if (instruction not in reserved_words["instructions"]["commands"] and instruction not in reserved_words["instructions"]["control_structures"] and instruction not in reserved_words["instructions"]["procedures"] and instruction not in reserved_words["instructions"]["control_structures"] and instruction not in reserved_words["keywords"]) and (instruction.lower() not in reserved_words["instructions"]["commands"] and instruction.lower() not in reserved_words["instructions"]["control_structures"] and instruction.lower() not in reserved_words["instructions"]["procedures"] and instruction.lower() not in reserved_words["instructions"]["control_structures"] and instruction.lower() not in reserved_words["keywords"]):
                output = False
    return output

def list_instructions_in_procs(program:list)->list:
    output = []
    serachin_procs = False
    opened = 0
    closed = 0
    procs_unified = []
    individual_proc = []
    for line in program:
        if "PROCS" in line:
            serachin_procs = True
            continue
        if line[0] == "[":
            serachin_procs = False
        if serachin_procs:
            individual_proc.append(line)
            opened += line.count("[")
            closed += line.count("]")
            if opened == closed:
                procs_unified.append(individual_proc)
                individual_proc = []
    for proc in procs_unified:
        proc_list = "".join(proc).split(";")
        first = proc_list[0]
        cut_pos = 0
        symbol_aparitions = 0
        for character in first:
            if character == "|":
                symbol_aparitions += 1
            if symbol_aparitions == 2:
                first = first[cut_pos:len(first)] + ";"
                proc[0] = first.replace("|", "")
                symbol_aparitions = 0
            cut_pos += 1
        string_proc = " ".join(proc).split(" ")
        string_proc.pop(len(string_proc)-1)
        string_proc = " ".join(string_proc)
        instructions = string_proc.split(";")
        if len(instructions) == 2:
            instructions.pop(1)
        output.append(instructions)
    return output

def validate_instructions_block(instruction:list)->bool:
    output = True
    validations = []
    if instruction[0].lower() == "assignto":
        validations.append(validate_assignTo(instruction))
    elif instruction[0].lower() == "goto":
        validations.append(validate_goto(instruction))
    elif instruction[0].lower() == "move":
        validations.append(validate_move(instruction))
    elif instruction[0].lower() == "turn" or instruction[0].lower() == "face":
        validations.append(validate_turn_and_face_and_facing(instruction))
    elif instruction[0].lower() == "put" or instruction[0].lower() == "pick":
        validations.append(validate_put_and_pick_and_canPut_and_canPick(instruction))
    elif instruction[0].lower() == "movetothe" or instruction[0].lower() == "moveindir" or instruction[0].lower() == "jumptothe" or instruction[0].lower() == "jumpindir":
        instruction_copy = instruction
        instruction_copy.pop(0)
        validations.append(validate_moveToThe_and_moveInDir_and_jumpToThe_and_jumpInDir_and_canMoveToThe_and_canMoveInDir_and_canJumpToThe_and_canJumpInDir(instruction))
    elif instruction[0].lower() == "nop":
        validations.append(validate_nop(instruction))
    elif instruction[0].lower() == "if":
        validations.append(validate_if(instruction))
    else:
        if instruction[0].capitalize() != "M" and instruction[0].capitalize() != "R" and instruction[0].capitalize() != "C" and instruction[0] != "c" and instruction[0].capitalize() != "B" and instruction[0].lower() != "b" and instruction[0].capitalize() != "P" and instruction[0].capitalize() != "J" and instruction[0].capitalize() != "G":
            validations.append(False) 
    if False in validations:
        output = False
    return output

def validate_instructions_in_procs(instructions_list:list)->bool:
    output = True
    validations = []
    for instruction_list_elemet in instructions_list:
        for instruction in instruction_list_elemet:
            instruction = instruction.split(" ")
            instruction = [ele for ele in instruction if ele != ""]
            if instruction[0].lower() == "assignto":
                validations.append(validate_assignTo(instruction))
            elif instruction[0].lower() == "goto":
                validations.append(validate_goto(instruction))
            elif instruction[0].lower() == "move":
                validations.append(validate_move(instruction))
            elif instruction[0].lower() == "turn" or instruction[0].lower() == "face":
                validations.append(validate_turn_and_face_and_facing(instruction))
            elif instruction[0].lower() == "put" or instruction[0].lower() == "pick":
                validations.append(validate_put_and_pick_and_canPut_and_canPick(instruction))
            elif instruction[0].lower() == "movetothe" or instruction[0].lower() == "moveindir" or instruction[0].lower() == "jumptothe" or instruction[0].lower() == "jumpindir":
                instruction_copy = instruction
                instruction_copy.pop(0)
                validations.append(validate_moveToThe_and_moveInDir_and_jumpToThe_and_jumpInDir_and_canMoveToThe_and_canMoveInDir_and_canJumpToThe_and_canJumpInDir(instruction))
            elif instruction[0].lower() == "nop":
                validations.append(validate_nop(instruction))
            elif instruction[0].lower() == "if":
                validations.append(validate_if(instruction))
    if False in validations:
        output = False
    return output             

def validate_assignTo(line:list)->bool:
    output = True
    if line[1] != ":":
        output = False
    if not line[2].isdigit():
        output = False
    if line[3] != ",":
        output = False
    if line[4] not in reserved_words["variables"]:
        output = False
    return output

def validate_goto(line:list)->bool:
    output = True
    if line[1] != ":":
        output = False
    if not line[2].isdigit() and line[2] not in reserved_words["variables"]:
        output = False
    if line[3] != ",":
        output = False
    if not line[4].isdigit() and line[4] not in reserved_words["variables"]:
        output = False
    return output

def validate_move(line:list)->bool:
    output = True
    if line[1] != ":":
        output = False
    if not line[2].isdigit() and line[2] not in reserved_words["variables"]:
        output = False
    return output

def validate_turn_and_face_and_facing(line:list)->bool:
    output = True
    if line[1] != ":":
        output = False
    if line[2].lower not in reserved_words["directions"]:
        output = False
    return output

def validate_put_and_pick_and_canPut_and_canPick(line:list)->bool:
    output = True
    if line[1] != ":":
        output = False
    # if not line[2].isdigit() or line[2] not in reserved_words["variables"]:
    #     output = False
    if line[3] != ",":
        output = False
    if line[4].lower().capitalize() not in reserved_words["objects"]:
        output = False
    return output

def validate_moveToThe_and_moveInDir_and_jumpToThe_and_jumpInDir_and_canMoveToThe_and_canMoveInDir_and_canJumpToThe_and_canJumpInDir(line:list)->bool:
    if len(line) == 4:
        line = [" "] + line
    output = True
    if line[1] != ":":
        output = False
    if not line[2].isdigit() and line[2] not in reserved_words["variables"]:
        output = False
    if line[3] != ",":
        output = False
    if line[4].lower() not in reserved_words["directions"]:
        output = False
    return output

def validate_nop(line:list)->bool:
    output = True
    if line[0] != "nop":
        output = False
    return output

def validate_not(condition:list)->bool:
    output = True
    if condition[1] != ":":
        output = False
    if condition[2].lower() == "facing":
        if not validate_turn_and_face_and_facing(condition):
            output = False
    if condition[2].lower() == "canput" or condition[2].lower() == "canpick":
        if not validate_put_and_pick_and_canPut_and_canPick(condition):
            output = False
    if condition[2].lower() == "canmoveindir" or condition[2].lower() == "canjumpindir" or condition[2].lower() == "canmovetothe" or condition[2].lower() == "canjumptothe":
        if not validate_moveToThe_and_moveInDir_and_jumpToThe_and_jumpInDir_and_canMoveToThe_and_canMoveInDir_and_canJumpToThe_and_canJumpInDir(condition):
            output = False
    return output

def validate_if(line:list)->bool:

    output = True

    pos = 0
    while pos <= len(line)-1:
        if line[pos].lower() == "then:" or line[pos].lower() == "then":
            break
        pos += 1
    if pos == len(line)-1:
        output = False
    condition = line[3:pos]
    if line[2].lower() == "facing":
        if not validate_turn_and_face_and_facing(condition):
            output = False
    if line[2].lower() == "canput" or line[2].lower() == "canpick":
        if not validate_put_and_pick_and_canPut_and_canPick(condition):
            output = False
    if line[2].lower() == "canmoveindir" or line[2].lower() == "canjumpindir" or line[2].lower() == "canmovetothe" or line[2].lower() == "canjumptothe":
        if not validate_moveToThe_and_moveInDir_and_jumpToThe_and_jumpInDir_and_canMoveToThe_and_canMoveInDir_and_canJumpToThe_and_canJumpInDir(condition):
            output = False
    if line[2].lower() == "not":
        if not validate_not(condition):
            output = False

    if line[1] != ":":
        output = False
    if not line[2].lower() in reserved_words["conditions"]:
        output = False
    if line[pos].lower() != "then" and line[pos].lower() != "then:":
        output = False
    
    pos_2 = pos + 1
    if line[pos+1].lower() != "[":
        output = False
    else:
        then_finished_pos = 0
        pos_2 += 1
        while pos_2 <= len(line):
            if line[pos_2] == "]":
                then_finished_pos = pos_2 - 1
                break
            pos_2 += 1
        then = line[pos+2: then_finished_pos+1]
        then = "".join(then)
        then = then.split(":")
        arguments = then[1]
        arguments = arguments.split(",")
        copy = []
        copy.append(then[0])
        copy.append(":")
        for argument in arguments:
            copy.append(argument)
            copy.append(",")
        copy.pop(len(copy)-1)
        if not validate_instructions_block(copy):
            output = False
    
    if line[then_finished_pos+2].lower() != "else":
        output = False
    
    if line[then_finished_pos+3].lower() != ":":
        output = False

    else_block_start = 0
    else_block_end = 0
    if line[then_finished_pos+4].lower() != "[":
        output = False
    else:
        else_block_start = then_finished_pos+4
        pos_2 = else_block_start
        while pos_2 <= len(line):
            if line[pos_2] == "]":
                else_block_end = pos_2 - 1
                break
            pos_2 += 1
        else_instructions_block = line[else_block_start+1:else_block_end+1]
        if not validate_instructions_block(else_instructions_block):
            output = False
        
    return output

def validate_program()->bool:
    program = load_file()
    load_program(program)
    output = False
    if find_program(program) and validate_variables_and_procs_name(reserved_words["variables"], reserved_words["instructions"]["procedures"]) and validate_arguments_recieiving(program, reserved_words["instructions"]["procedures"]) and validate_available_instructions(program) and validate_instructions_in_procs(list_instructions_in_procs(program)):
        output = True
    return output
  

print(validate_program())