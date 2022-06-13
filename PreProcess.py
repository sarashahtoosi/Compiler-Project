import re


def name_files(i):
    in_file = "files/files_0/f_0_{num}.txt".format(num=i)
    out_file = "files/files_1/f_1_{num}.txt".format(num=i)
    temp_file = "files/files_0/t_0_{num}.txt".format(num=i)
    return in_file, out_file, temp_file


def include_add(temp_file):
    ftemp = open(temp_file, "r")
    temp = ""
    for line in ftemp.readlines():
        sline = line.split()
        if re.search("#\s*include", line):
            path = "files/files_0/" + sline[-1][1:-1]
            tt = open(path, "r")
            temp += tt.read()
            temp += '\n'
            # print(temp)
        else:
            temp += line
    ftemp.close()
    ftemp = open(temp_file, "w")
    ftemp.write(temp)
    ftemp.close()

    return


def defines_to_dictionary(file_name):
    dit = {}
    ftemp = open(file_name, "r")
    temp = ""
    lineNum = 0
    for line in ftemp.readlines():
        # print(line)
        sline = line.split()
        if re.search("#\s*define", line):
            idx = 0
            for i in range(len(sline)):
                if i == "#define" or i == "define":
                    idx = i + 1
            tkey = sline[idx + 1]
            tvalue = ' '.join(sline[idx + 2:])
            # print(tkey)
            # print(tvalue)
            startLineNum = lineNum
            dit[tkey] = [tvalue, startLineNum, 10000000]

        elif re.search("#\s*undef", line):
            idx = 0
            for i in range(len(sline)):
                if i == "#undef" or i == "undef":
                    idx = i + 1
            tkey = sline[idx + 1]

            endLineNum = lineNum
            dit[tkey][2] = endLineNum
        else:
            temp += line
            lineNum += 1

    ftemp.close()
    ftemp = open(file_name, "w")
    ftemp.write(temp)
    ftemp.close()

    return dit


def replace_defines(file_name, def_di):
    ftemp = open(file_name, "r")
    temp = ""
    lineNo = 0
    for line in ftemp.readlines():
        for key, value in def_di.items():
            # print(key,value)
            startLineNo = value[1]
            endLineNo = value[2]
            val = value[0]
            if lineNo >= startLineNo and lineNo <= endLineNo:
                line = line.replace(key, val)
        temp += line
        lineNo += 1
    ftemp.close()
    ftemp = open(file_name, "w")
    ftemp.write(temp)
    ftemp.close()

    return


def temp_to_output(temp_file, output_file):
    ftemp = open(temp_file, "r")
    temp = ftemp.read()
    fout = open(output_file, "w")
    fout.write(temp)
    ftemp.close()
    fout.close()
    return


# code idea from a question in stackover flow
def remove_comments(file_name):
    ftemp = open(file_name, "r")
    temp = ftemp.read()

    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " "
        else:
            return s

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )

    res = re.sub(pattern, replacer, temp)
    ftemp.close()
    ftemp = open(file_name, "w")
    ftemp.write(res)
    ftemp.close()

    return


def input_to_temp(in_file, temp_file):
    fin = open(in_file, "r")
    temp = fin.read()
    ftemp = open(temp_file, "w")
    ftemp.write(temp)
    ftemp.close()
    fin.close()
    return


# Becuse of dynamic version of def/undef we can not seperate them
def undef_hedder(def_di, temp_file):
    return


number_of_files = 2
for i in range(number_of_files):
    # Declare pathes for the input, output and temp files
    in_file_name, out_file_name, temp_file_name = name_files(i + 1)

    # Write all the input file data into the temp file
    input_to_temp(in_file_name, temp_file_name)

    # remove all the comments from the input file and write them on temp file
    remove_comments(temp_file_name)

    # Find include files, append the files on the temp file and add other lines to temp file
    include_add(temp_file_name)

    # Find all the defines and make a dictionary from them with pairs of keys and values
    define_dictionary = defines_to_dictionary(temp_file_name)

    # Delete all undefs from the defien dictionary and return the modified dictionary
    # undef_hedder(define_dictionary,temp_file_name)

    # Replace all defines with their values
    replace_defines(temp_file_name, define_dictionary)

    # Write the temp file on the output file
    temp_to_output(temp_file_name, out_file_name)

# These lines of codes were our first attempt to preprocessing but it had a lot of bugs, so we designed it compeletly new
'''
    while True:
        # Get next line from file
        line = file.readline()
        my_file.write(line)
        # if line is empty
        # end of file is reached
        if not line:
            break
    file.close()
    my_file = open("preprocessed.txt", "r")
    # ----- delete includes -----
    while True:
        my_file_line = my_file.readline()
        line = my_file_line.split()
        for i in range(len(line)):
            if line[i] == '#' and line[i+1] == 'include':
                var = line[i: len(line) + 1] == ''
        listToStr = ''.join([str(elem) for elem in line])
        my_file.writelines(listToStr)
        if not line:
            break
    # ----- delete multi line & single line comments -----
    while True:
        my_file_line = my_file.readline()
        line = my_file_line.split()
        for i in range(len(line)):
            if line[i] == '/*' or line[i] == '//':
                var = line[i: len(line) + 1] == ''
            if line[i] == '*/':
                var = line[0: i + 1] == ''
        istToStr = ''.join([str(elem) for elem in line])
        my_file.writelines(listToStr)
        if not line:
            break

    # ----- defines -----
    while True:
        list_of_defines = []
        my_file_line = my_file.readline()
        line = my_file_line.split()
        for i in range(len(line)):
            if line[i] == '#' and line[i+1] == 'define':
                list_of_defines.append([line[i+2],line[i+3)
'''