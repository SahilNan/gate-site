import file_utils

class Section:
    def __init__(self):
        self.exist = False
        self.content = ''

    def add(self, line):
        self.content = self.content + line

    def valid():
        return True

class OptionsSection(Section):
    def __init__(self):
        super().__init__()
        self.a = Section()
        self.b = Section()
        self.c = Section()
        self.d = Section()

    def add(self,line):
        if not self.a.exist and line.startswith("(A) "):
            self.a.exist = True
            self.a.add(line[4:])
        elif self.a.exist and not self.b.exist and line.startswith("(B) "):
            self.b.exist = True
            self.b.add(line[4:])
        elif self.a.exist and self.b.exist and not self.c.exist and line.startswith("(C) "):
            self.c.exist = True
            self.c.add(line[4:])
        elif self.a.exist and self.b.exist and self.c.exist and not self.d.exist and line.startswith("(D) "):
            self.d.exist = True
            self.d.add(line[4:])
        elif self.d.exist:
            self.d.add(line)
        elif self.c.exist:
            self.c.add(line)
        elif self.b.exist:
            self.b.add(line)
        elif self.a.exist:
            self.a.add(line)
        super().add(line)

    def valid(self):
        return self.exist and self.a.exist and self.b.exist and self.c.exist and self.d.exist

class QuestionContent:
    def __init__(self):
        self.question = Section()
        self.category = Section()
        self.options = OptionsSection()

    def add(self, line):
        if self.category.exist:
            self.category.add(line)
        elif self.options.exist:
            self.options.add(line)
        elif self.question.exist:
            self.question.add(line)
        else:
            print('Not valid line:',line)

    def is_present(self):
        return self.question.exist

    def content(self):
        ret_text = ''
        if self.question.exist :
            ret_text = "Question:\n"
            ret_text += self.question.content.rstrip()
            ret_text += '\n'
            if self.options.exist:
                ret_text += "Options:\n"
                ret_text += self.options.content.rstrip()
                ret_text += '\n'
            if self.category.exist:
                ret_text += "Category:\n"
                ret_text += self.category.content.rstrip()
                ret_text += '\n'
            ret_text += '\n'
        return ret_text

class QuestionFileParser(file_utils.FileLineProcessor):

    def post_end_previous_question(self):
        pass

    def pre_process_lines(self):
        pass

    def post_process_lines(self):
        pass

    def end_previous_question(self):
        if self.question.question.exist :
            self.post_end_previous_question()

    def start_question(self):
        self.end_previous_question()
        self.question = QuestionContent()
        self.question.question.exist = True

    def process_line(self, line):
        if line == 'Question:\n':
            self.start_question()
        elif line == 'Options:\n':
            self.question.options.exist = True
        elif line == 'Category:\n':
            self.question.category.exist = True
        elif line == '`;':
            pass
        else :
            self.question.add(line)

    def process_lines(self, lines):
        self.pre_process_lines()
        super().process_lines(lines)
        self.end_previous_question()
        self.post_process_lines()

    def process(self):
        self.question = QuestionContent()
        super().process()