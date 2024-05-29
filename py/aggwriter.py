import os
import csv
import file_utils
import question

class QuestionWriter(file_utils.FileWriter):

    def write(self,question):
        self.wfile.write(question.content())

class QuestionCSVWriter(file_utils.FileWriter):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.year = '2007'
        self.type = 'MCQ'
        self.mark = '1'
        self.answer = 'A'

    def write(self,question):
        row = {}
        row['Year'] = self.year
        if question.question.exist :
            row['Question'] = question.question.content.rstrip()
            if question.options.exist:
                row['Qption_A'] = question.options.a.content.rstrip()
                row['Qption_B'] = question.options.b.content.rstrip()
                row['Qption_C'] = question.options.c.content.rstrip()
                row['Qption_D'] = question.options.d.content.rstrip()
            if question.category.exist:
                row['Category'] = question.category.content.rstrip()
        self.csv_writer.writerow(row)

    def start(self):
        super().start()
        fieldnames = ['Year', 'Type', 'Question', 'Qption_A', 'Qption_B', 'Qption_C', 'Qption_D', 'Category', 'Marks', 'Answer']
        self.csv_writer = csv.DictWriter(self.wfile, fieldnames=fieldnames)
        self.csv_writer.writeheader()

class QuestionWriteFileProcessor(question.QuestionFileParser):

    def __init__(self, file_path, js_writer, csv_writer):
        super().__init__(file_path)
        self.js_writer = js_writer
        self.csv_writer = csv_writer

    def post_end_previous_question(self):
        self.js_writer.write(self.question)
        self.csv_writer.write(self.question)

    def pre_process_lines(self):
        self.js_writer.writeTxt('const ')
        self.js_writer.writeTxt(os.path.basename(self.file_path).replace(".txt", "").replace(".js", ""))
        self.js_writer.writeTxt('=`\n')
        self.csv_writer.year = os.path.basename(self.file_path).replace(".txt", "").replace(".js", "")

    def post_process_lines(self):
        self.js_writer.writeTxt('\n`;\n')

class DirectoryProcessor(file_utils.DirectoryFileProcessor):

    def process_file(self, file_name):
        fp = QuestionWriteFileProcessor(file_name,self.js_writer,self.csv_writer)
        fp.process()

    def process(self):
        self.js_writer = QuestionWriter("/Users/lakshmi/Documents/workspace-spring-tool-suite-4-4.12.1.RELEASE/ai/gt/html/js/qp_all.js")
        self.js_writer.start()
        self.csv_writer = QuestionCSVWriter("/Users/lakshmi/Documents/workspace-spring-tool-suite-4-4.12.1.RELEASE/ai/gt/html/js/qp_csv.csv")
        self.csv_writer.start()
        super().process()
        self.js_writer.end()
        self.csv_writer.end()

directory_path = "/Users/lakshmi/Documents/workspace-spring-tool-suite-4-4.12.1.RELEASE/ai/gt/html/qp"
p = DirectoryProcessor(directory_path)
p.process()