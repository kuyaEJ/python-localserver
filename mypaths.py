class Path():
    def __init__(self):
        self.__root = ''# head of path
        self.__dest = ''# tail of path
    
    def __str__(self):
        return self.__getPath()

    def setcwd(self, cwd):
        separator = self.__getsep(cwd)
        if len(cwd) < 1: return
        names = cwd.split(separator)
        if cwd[len(cwd)-1] == separator:
            names.pop()


        s = str(separator)
        # Combine paths into string
        for name in names[0:len(names) - 1]:
            s += str(name)
            s += str(separator)

        self.__root = s[0:len(s)-1]
        self.__dest = names[len(names) - 1]
        
        self.__validate()
    
    def __getsep(self, path):
        sep = ''
        if len(path.split('/')) == 1:
            sep = '\\'
        else:
            sep = '/'
        return sep

    def cwd(self):
        return self.__root
    
    def __getPath(self):
        return f'{self.__root}/{self.__dest}'
    
    def __validate(self):
        separator = self.__getsep(self.__root)
        try:
            s = ''
            w = ''
            for n in self.__root.split(separator):
                for r in ['.', ',', ':', ';', '?', '/', '\\']:
                    if r in n:
                        s += f'Not a valid sub-directory with \'{r}\' in \'{n}\'. '
                        if r in ('/', '\\') and r != separator:
                            w += f'\n[WARNING]: Did you mean to use the \'{'/' if separator =='/' else '\\'}\' operator in \'{n}\' instead of using the \'{r}\' operator? '
            if s != '':
                print(w)
                raise ValueError(s)
                
        except ValueError as e:
            raise ValueError(f'Absolute path \'{self.__root}{separator}{self.__dest}\' caught an error.', e)

        try:
            s = ''
            w = ''
            for c in self.__dest:
                for r in [',', ':', ';', '?', '/', '\\']:
                    if r == c:
                        s += f'Invalid name with \'{c}\' in {self.__dest}'
                        if c in ('/', '\\') and c != separator:
                            w += f'\n[WARNING]: Did you mean to reference a sub-directory with the \'{'/' if separator =='/' else '\\'}\' operator in \'{r}\'? '

            
            if s != '':
                print(w)
                raise ValueError(s)

        except ValueError as e:
            raise ValueError(f'Path destination \'{self.__dest}\' caught an error.', e)
    
    def __tryOpen(self, file):
        try:
            with open(file, 'r+b') as f:
                return f.read()
                
        except Exception as e:
            print(e)
            raise
        return ''