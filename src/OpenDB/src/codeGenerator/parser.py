import re


def _findIndex(_list, _object, startIndex=0):
    index = startIndex
    while index < len(_list):
        line = _list[index].strip()
        line = line.replace(' ', '')
        if line == _object:
            return index
        index += 1
    return -1


def _getSections(lines, tag, sections=None, remove=False):
    if sections is None:
        sections = {}
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        line = line.replace(' ', '')
        if re.match(tag, line):
            name = line[len(tag):]

            if name in sections:
                raise Exception(f"Duplicate Tag: {name}")

            end = _findIndex(lines, line.replace('Begin', 'End', 1), i)
            if end == -1:
                print(f'Could not find an End for tag {name}\n')
                return False
            if remove:
                del lines[i+1:end]
            else:
                sections.setdefault(name, [])
                if end > i+1:
                    sections[name].extend(lines[i+1:end])
        i += 1
    return True


class Parser:

    def __init__(self, fileName):
        with open(fileName, 'r') as file:
            self.lines = file.readlines()
        self.generatorCode = {}
        self.userCodeTag = '//UserCodeBegin'
        self.generatorCodeTag = '//GeneratorCodeBegin'

    def setCommentStr(self, comment):
        self.userCodeTag = f'{comment}UserCodeBegin'
        self.generatorCodeTag = f'{comment}GeneratorCodeBegin'

    def parseUserCode(self):
        self.userCode = {}
        return _getSections(self.lines, self.userCodeTag, self.userCode)

    def parseSourceCode(self, fileName):
        with open(fileName, 'r') as sourceFile:
            db_lines = sourceFile.readlines()
        return _getSections(db_lines, self.generatorCodeTag, self.generatorCode)

    def cleanCode(self):
        return _getSections(self.lines, self.generatorCodeTag, remove=True)

    def writeInFile(self, fileName):
        for section in self.generatorCode:
            db_lines = self.generatorCode[section]
            j = 0
            while j < len(db_lines):
                line = db_lines[j].strip().replace(' ', '')
                if re.match(self.userCodeTag, line):
                    name = line[len(self.userCodeTag):]
                    if name in self.userCode:
                        db_lines[j+1:j+1] = self.userCode[name]
                j += 1
            self.generatorCode[section] = db_lines
        i = 0
        while i < len(self.lines):
            line = self.lines[i].strip()
            line = line.replace(' ', '')
            if re.match(self.generatorCodeTag, line):
                name = line[len(self.generatorCodeTag):]
                self.generatorCode.setdefault(name, [])
                self.lines[i+1:i+1] = self.generatorCode[name]
            i += 1
        with open(fileName, 'w') as out:
            out.write(''.join(self.lines))
        return True
