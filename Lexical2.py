class lexical:
    operator_signs = ['!', '%', '^', '*', '+', '/', '-', '<', '>', '=']
    special_signs = ['(', ')', '[', ']', '{', '}', ';']
    key_words = ["long", "char", "float", "short", "unsigned", "signed", "int", "double",
                 "else", "break", "for", "if", "while", "continue", "void", "return"]

    ans = ("", "")

    def is_char(self, i):
        return ('a' <= s[i] and s[i] <= 'z') or ('A' <= s[i] and s[i] <= 'Z') or s[i] == '_'

    def is_number(self, i):
        return i < len(s) and '0' <= s[i] and s[i] <= '9'

    def continuee(self, i):
        tmp1 = i < len(s)
        tmp2 = not (s[i] in self.operator_signs)
        tmp3 = not (s[i] in self.special_signs)
        tmp4 = not (s[i] == " ")
        tmp5 = not (s[i] == ".") and not (s[i] == "&") and not (s[i] == "|")

        return tmp1 and tmp2 and tmp3 and tmp4 and tmp5

    def find_word(self, i):
        word = ""
        while self.continuee(i):
            if self.is_char(i) or self.is_number(i):
                word += s[i]
                i += 1
            else:
                self.ans = ("ERROR", "ERROR")
                return i

        if word in self.key_words:
            self.ans = ("KEY_WORD", word)
            return i
        else:
            self.ans = ("ID", word)
            return i

    def find_number(self, i):
        number = ""
        dot = 0
        while self.continuee(i) or s[i] == '.':
            if s[i] == '.' or self.is_number(i):
                if s[i] == '.':
                    dot += 1
                number += s[i]
                i += 1
            else:
                self.ans = ("ERROR", "ERROR")
                return i

        if dot == 0:
            self.ans = ("NUMBER int", number)
            return i
        if dot == 1:
            self.ans = ("NUMBER double", number)
            return i
        if dot > 1:
            self.ans = ("ERROR", "ERROR")
            return i

    def find_operator(self, i):
        tmp = "" + s[i]

        if i + 1 < len(s) and s[i + 1] == '=':
            tmp += s[i + 1]
            self.ans = ("OPERATOR", tmp)
            return i + 2
        else:
            self.ans = ("OPERATOR", tmp)
            return i + 1

    def find_special(self, i):
        tmp = "" + s[i]
        self.ans = ("SPECIAL_KEY", tmp)
        return i + 1

    def dot(self, i):
        if i + 1 < len(s) and self.is_char(i + 1):
            self.ans = ("OPERATOR", ".")
            return i + 1
        if i + 1 < len(s) and self.is_number(i + 1):
            return self.find_number(i)

        self.ans = ("ERROR", "ERROR")
        return i + 1

    def AND(self, i):
        if i + 1 < len(s) and s[i + 1] == '&':
            self.ans = ("OPERATOR", "&&")
            return i + 2
        else:
            self.ans = ("ERROR", "ERROR")
            return i + 1

    def OR(self, i):
        if i + 1 < len(s) and s[i + 1] == '|':
            self.ans = ("OPERATOR", "||")
            return i + 2
        else:
            self.ans = ("ERROR", "ERROR")
            return i + 1

    def plus(self, i):
        if i + 1 < len(s) and s[i + 1] == '+':
            self.ans = ("OPERATOR", "++")
            return i + 2

        self.ans = ("OPERATOR", "+")
        return i + 1

    def mines(self, i):
        if i + 1 < len(s) and s[i + 1] == '-':
            self.ans = ("OPERATOR", "--")
            return i + 2

        self.ans = ("OPERATOR", "-")
        return i + 1

    def find_string(self, i):
        str = ""
        i += 1
        while s[i] != '"':
            if i == len(s) - 1:
                self.ans = ("ERROR", "ERROR")
                return i
            str += s[i]
            i += 1

        self.ans = ("string", str)

        return i + 1

    def get_next_token(self, i):
        if s[i] == '.':
            return self.dot(i)

        if s[i] == '&':
            return self.AND(i)

        if s[i] == '|':
            return self.OR(i)

        if s[i] == '+':
            return self.plus(i)

        if s[i] == '-':
            return self.mines(i)

        if s[i] == '"':
            return self.find_string(i)

        if self.is_char(i):
            return self.find_word(i)

        if self.is_number(i):
            return self.find_number(i)

        if s[i] in self.operator_signs:
            return self.find_operator(i)

        if s[i] in self.special_signs:
            return self.find_special(i)

        else:
            self.ans = ("ERROR", "ERROR")
            return i + 1


lx = lexical()
number_of_files = 1

for i in range(number_of_files):

    in_file_name = "files/files_1/f_1_{num}.txt".format(num=i + 1)
    out_file_name = "files/files_2/f_2_{num}.txt".format(num=i + 1)

    fin = open(in_file_name, "r")
    fout = open(out_file_name, "w")

    line_number = 0
    for s in fin.readlines():
        line_number += 1
        # print(s)
        i = 0
        while i < len(s):
            while s[i] == ' ':
                i += 1

            if i == len(s) - 1:
                break

            i = lx.get_next_token(i)

            if lx.ans == ("ERROR", "ERROR"):
                print("ERROR at character : ", line_number, " - ", i - 1)
                break

            # print(lx.ans)
            fout.write(' : '.join(lx.ans))
            fout.write("\n\n")
    fin.close()
    fout.close()