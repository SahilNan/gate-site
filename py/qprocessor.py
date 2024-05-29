import os
import unicodedata
import csv

class FileLineProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def process_line(self, line):
        print(line)

    def process_lines(self, lines):
        for line in lines:
            self.process_line(line)

    def process(self):
        rfile = open(self.file_path, "r")
        lines = rfile.readlines()
        rfile.close()
        self.process_lines(lines)

class DirectoryFileProcessor:
    def __init__(self, base_directory):
        self.base_directory = base_directory

    def process_file(self, file_name):
        print(file_name)

    def process(self):
        with os.scandir(self.base_directory) as entries:
            for entry in entries:
                if entry.is_file():
                    self.process_file(self.base_directory+"/"+entry.name)

class UniqueDictCounter:
    def __init__(self):
        self.dict = {}
        self.total = 0

    def add(self, line):
        pass

    def print(self, max_count):
        print("Total : ", self.total)
        print("Unique : ", len(self.dict))
        self.dict = dict(sorted(self.dict.items(), key=lambda item: item[1], reverse=True))
        for key, value in self.dict.items():
            rline = repr(key)
            if(value > max_count):
                print(f"{rline}: {value}")

class UniqueLinesCounter(UniqueDictCounter):
    def add(self, line):
        self.total += 1
        self.dict[line] = self.dict.get(line, 0) + 1

class UniqueWordsCounter(UniqueDictCounter):
    def add(self, line):
        l_words = line.split()
        self.total += len(l_words)
        for l_word in l_words:
            self.dict[l_word] = self.dict.get(l_word, 0) + 1

class NonAsciCharDetector(UniqueDictCounter):
    def add(self, line):
        for char in line:
            if 0 <= ord(char) <= 127:
                continue
            else:
                self.total += 1
                self.dict[char] = self.dict.get(char, 0) + 1

    def print(self, max_count):
        self.dict = dict(sorted(self.dict.items(), key=lambda item: item[1], reverse=True))
        print(self.dict)
        for key in self.dict:
            print(key, '%04x' % ord(key), unicodedata.category(key), end=" ")
            print(unicodedata.name(key))

class NonAsciCharFileCleaner():
    def __init__(self, file_path):
        super().__init__(file_path)
        self.replace_chars = {'〈': '{', '〉': '}', '…': '...', '⋯': '...'}

    def process(self):
        file = open(self.file_path, "r")
        data = file.read()
        file.close()
        for key, value in self.replace_chars.items():
            data = data.replace(key,value)
        wf = open(self.file_path,"w")
        wf.write(data)
        wf.close()


class FileProcessor(FileLineProcessor):
    def __init__(self, file_path,line_processors):
        super().__init__(file_path)
        self.line_processors = line_processors

    def process_line(self, line):
        for line_processor in self.line_processors:
            line_processor.add(line)

    def process(self):
        super().process()

class QuestionWriter:
    def __init__(self, file_path):
        self.file_path = file_path

    def write(self,question):
        self.wfile.write(question.content())

    def writeTxt(self,content):
        self.wfile.write(content)

    def end(self):
        self.wfile.flush()
        self.wfile.close()

    def start(self):
        self.wfile = open(self.file_path, "w")

class QuestionCSVWriter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.year = '2007'
        self.type = 'MCQ'
        self.mark = '1'
        self.answer = 'A'

    def write(self,question):
        self.csv_writer.writerow({'Year': self.year, 'Type': self.type, 'Question': 'Question', 'Qption_A': 'Qption_A', 'Qption_B': 'Qption_B', 'Qption_C': 'Qption_C', 'Qption_D': 'Qption_D', 'Category': 'Category', 'Marks': self.mark, 'Answer': self.answer})

    def end(self):
        self.wfile.flush()
        self.wfile.close()

    def start(self):
        self.wfile = open(self.file_path, 'w', newline='')
        fieldnames = ['Year', 'Type', 'Question', 'Qption_A', 'Qption_B', 'Qption_C', 'Qption_D', 'Category', 'Marks', 'Answer']
        self.csv_writer = csv.DictWriter(self.wfile, fieldnames=fieldnames)
        self.csv_writer.writeheader()


class QuestionContent:
    category_dict1 = { 
        'BCNF' : 'Databases',
        'non-planar graph' : 'EngineeringMathematics',
        'set associative cache' : 'ComputerOrganizationAndArchitecture',
        'lexical':'CompilerDesign',
        'SMTP': 'ComputerNetworks',
        'UDP': 'ComputerNetworks',
        'eigenvalue': 'EngineeringMathematics',
        '&int;':'EngineeringMathematics',
        'Newton-Raphson':'EngineeringMathematics',
        'Karnaugh':'DigitalLogic',
        'radix':'DigitalLogic',
        'multiplexer':'DigitalLogic',
        'CPU scheduling':'OperatingSystem',
        'critical section':'OperatingSystem'
    }

    category_dict = {
        'fdfaefgwefwefwefwefasdfcsd' : 'Databases'
    }

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

    def add_category(self):
        for key,value in self.category_dict.items():
            if key in self.question.content or (self.options.exist and key in self.options.content):
                print(self.question.content)
                print(self.options.content)
                return "Category:\n"+value+"\n"
        return ''

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
            elif not self.category.exist :
                ret_text += self.add_category().rstrip()
                ret_text += '\n'
            ret_text += '\n'
        return ret_text

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
        self.a = False
        self.b = False
        self.c = False
        self.d = False

    def add(self,line):
        if not self.a and line.startswith("(A) "):
            self.a = True
        elif self.a and not self.b and line.startswith("(B) "):
            self.b = True
        elif self.a and self.b and not self.c and line.startswith("(C) "):
            self.c = True
        elif self.a and self.b and self.c and not self.d and line.startswith("(D) "):
            self.d = True
        super().add(line)

    def valid(self):
        return self.exist and self.a and self.b and self.c and self.d

class QuestionCounter:
    def __init__(self):
        self.questions = 0
        self.options = 0
        self.category = 0
        self.words = 0
        self.words_dict = {}

    def count_words(self, question):
        q_words = question.question.content.split()
        self.words += len(q_words)
        if question.options.valid():
            o_words = question.options.content.split()
            q_words = q_words + o_words
        for l_word in set(q_words):
            self.words_dict[l_word] = self.words_dict.get(l_word, 0) + 1

    def count(self, question):
        self.questions += 1
        if question.category.exist :
            self.category += 1    
        if question.options.valid():
            self.options += 1
        elif question.options.exist:
            print('Not all options present',self.question.content())
        self.count_words(question)

    def aggregate(self, counter):
        self.questions += counter.questions
        self.options += counter.options
        self.category += counter.category
        self.words += counter.words
        for key, value in counter.words_dict.items():
            self.words_dict[key] = self.words_dict.get(key, 0) + value

    def print(self,topic):
        print(topic,'Question:',self.questions,'Options:',self.options,'Category:',self.category, 'words:',self.words, 'unique_words:',len(self.words_dict))

class QuestionFileProcessor(FileLineProcessor):

    def post_end_previous_question(self):
        pass

    def pre_process_lines(self):
        pass

    def post_process_lines(self):
        pass

    def end_previous_question(self):
        if self.question.question.exist :
            self.ques_counter.count(self.question)
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
        self.ques_counter = QuestionCounter()
        self.question = QuestionContent()
        super().process()
        self.ques_counter.print(os.path.basename(self.file_path))

class QuestionWriteFileProcessor(QuestionFileProcessor):

    def __init__(self, file_path, js_writer, csv_writer):
        super().__init__(file_path)
        self.js_writer = js_writer
        self.csv_writer = csv_writer

    def post_end_previous_question(self):
        self.q_writer.write(self.question)
        self.js_writer.write(self.question)
        self.csv_writer(self.question)

    def pre_process_lines(self):
        self.q_writer = QuestionWriter(self.file_path)
        self.q_writer.start()
        self.js_writer.writeTxt('const ')
        self.js_writer.writeTxt(os.path.basename(self.file_path).replace(".txt", "").replace(".js", ""))
        self.js_writer.writeTxt('=`\n')
        self.csv_writer.year = os.path.basename(self.file_path).replace(".txt", "").replace(".js", "")

    def post_process_lines(self):
        self.q_writer.end()
        self.js_writer.writeTxt('\n`;\n')

class DirectoryProcessor(DirectoryFileProcessor):
    def __init__(self, base_directory):
        super().__init__(base_directory)

    def process_file(self, file_name):
        #fp = FileProcessor(file_name,self.line_processors)
        fp = QuestionWriteFileProcessor(file_name,self.js_writer,self.csv_writer)
        fp.process()
        self.ques_counter.aggregate(fp.ques_counter)

    def process(self):
        self.js_writer = QuestionWriter("/Users/lakshmi/Documents/workspace-spring-tool-suite-4-4.12.1.RELEASE/ai/gt/html/js/qp_all.js")
        self.js_writer.start()
        self.csv_writer = QuestionCSVWriter("/Users/lakshmi/Documents/workspace-spring-tool-suite-4-4.12.1.RELEASE/ai/gt/html/js/qp_csv.csv")
        self.csv_writer.start()
        self.lines_counter = UniqueLinesCounter()
        self.words_counter = UniqueWordsCounter()
        self.line_processors = [self.lines_counter, self.words_counter]
        self.ques_counter = QuestionCounter()
        super().process()
        self.js_writer.end()
        self.csv_writer.end()
        self.ques_counter.print('Total')
        self.dict = dict(sorted(self.ques_counter.words_dict.items(), key=lambda item: item[1], reverse=True))
        for key, value in self.dict.items():
            rline = repr(key)
            if(value > 2000):
                print(f"{rline}: {value}")

directory_path = "/Users/lakshmi/Documents/workspace-spring-tool-suite-4-4.12.1.RELEASE/ai/gt/html/qp"
p = DirectoryProcessor(directory_path)
p.process()