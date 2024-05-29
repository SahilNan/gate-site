import os

class DirectoryIterator:
    def __init__(self, base_directory):
        self.base_directory = base_directory

    
class QPMetadata:
    question_paper={
        "2013": {
            "total": 100,
            "sections": 1,
            "1 mark": "1-25,56-60",
            "2-mark":"26-55,61-65",
            "mcq":"1-65",
            "cdq":"48-49,50-51",
            "lq":"52-53,54-55"
        },
        "2014": {
            "total": 100,
            "sections": 3,
            "1 mark": "1-5,11-35",
            "2-mark":"6-10,36-65",
            "mcq":"1-65",
            "cdq":"48-49,50-51",
            "lq":"52-53,54-55"
        }
    }

    def get_metadata(self, year):
        return self.question_paper.get(year)

    def has_metadata(self, year):
        key = year.replace("g_","")
        key = key.replace(".txt","")
        if key in self.question_paper:
            return True
        else:
            return False

class TextClean:

    ignore_lines={
        "Do not delete this line simple\n":0
    }

    def __init__(self, base_directory):
        self.data = []
        self.total_lines = 0;
        self.base_directory = base_directory
        self.sentences = {}
        self.metadata = QPMetadata()
        self.consecutive_newlines = 0

    def read_file_lines(self, file_path):
        rfile = open(self.base_directory+"/"+file_path, "r")
        lines = rfile.readlines()
        rfile.close()
        return lines

    def open_write_file(self, file_path):
        self.wfile = open(self.base_directory+"/"+file_path, "w")

    def process_empty_line(self, line):
        if line == "\n" or line == "\x0c\n" or line == "   \n":
            self.consecutive_newlines += 1
            return True
        else:
            if self.consecutive_newlines > 0:
                self.wfile.write("\n")
                self.consecutive_newlines = 0
            return False

    def write_lines_to_file(self, file_path, lines):
        self.wfile = open(self.base_directory+"/"+file_path, "w")
        self.consecutive_newlines = 0
        for line in lines:
            if self.process_empty_line(line):
                continue
            if line in self.ignore_lines:
                continue
            self.wfile.write(line)
        self.wfile.flush()
        self.wfile.close()

    def clean_file(self, file_path):
        lines = self.read_file_lines(file_path)
        for line in lines:
            self.sentences[line] = self.sentences.get(line, 0) + 1
        self.write_lines_to_file(file_path, lines)
        print(file_path+ " : ",len(lines))
        self.total_lines += len(lines)

    def clean_files(self):
        with os.scandir(self.base_directory) as entries:
            for entry in entries:
                if entry.is_file() and self.metadata.has_metadata(entry.name):
                    self.clean_file(entry.name)

    def clean(self):
        self.clean_files()
        self.sentences = dict(sorted(self.sentences.items(), key=lambda item: item[1], reverse=True))
        top_count = 0
        for key, value in self.sentences.items():
            top_count += 1
            rline = repr(key)
            if(value > 1000000):
                print(f"{rline}: {value}")
        print("Totallines : ", self.total_lines)
        print("Uniquelines : ", len(self.sentences))

directory_path = "/Users/lakshmi/Documents/workspace-spring-tool-suite-4-4.12.1.RELEASE/ai/gt/html/qp"
#tc = TextClean(directory_path)
#tc.clean()
#write_lines_to_file(directory_path+"/g_2007_m.txt",read_file_lines(directory_path+"/g_2007.txt"))

file_name = "/Users/lakshmi/Documents/workspace-spring-tool-suite-4-4.12.1.RELEASE/ai/gt/html/qp/qp_2013.txt"

file = open(file_name, "r")
freq = {}
char_replace = {"𝜋": "&pi;","𝑑":"d","𝑝":"p","𝑞":"q","≠":"&ne;","𝑥":"x","𝑦":"y","𝑧":"z",
"𝐷": "D","𝐸":"E","𝐶":"C","𝐵":"B","≠":"&ne;","𝑥":"x","𝑦":"y","𝑧":"z","𝑃": "P", "𝑄": "Q",
"𝑊": "W", "𝑁": "N", "𝑀": "M","𝑚": "m", "𝑏": "b", "𝑐": "c", "𝐿": "L", "𝐺": "G","𝐹": "F", "𝐴": "A",
"𝐻": "H", "𝑉": "V", "𝑆": "S", "𝑇": "T", "∗": "*", "×": "x", "𝐾": "K", "𝑖": "i", "𝑗": "j", "𝑓": "f", "𝑣": "v",
"“": "\"", "”": "\"", "’": "'", "𝑘": "k", "𝑠": "s", "𝑡": "t", "𝑂": "O", "𝐽": "J","𝑛": "n", "𝑅": "R",
"∑": "&sum;", "𝜀": "&epsilon;", "∀": "&forall;", "θ": "&Theta;", "∃": "&exist;","⊕": "&oplus;", "∈": "&isin;",
"≡": "&equiv;", "≥": "&ge;", "≤": "&le;", "𝑤": "&omega;","⊙": "&odot;", "∠": "&ang;", "𝜓": "&psi;", "𝜑": "&Phi;",
"𝑢":"u","𝑎":"a","𝑟":"r", "‘": "'", "⋅": ".","⋈": "&bowtie;","𝜎": "&sigma;","𝑙": "l"
}
while 1:     
    # read by character
    char = file.read(1)          
    if not char: 
        break
    if 0 <= ord(char) <= 127:
        continue
    elif char not in char_replace:
        freq[char] = freq.get(char, 0) + 1        
file.close()

file = open(file_name, "r")
data = file.read()
file.close()
for key, value in char_replace.items():
    data = data.replace(key,value)
wf = open(file_name,"w")
wf.write(data)
wf.close()
print(freq)
print(len(freq))
