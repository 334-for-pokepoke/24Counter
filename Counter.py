import os
import sys
import re
import tkinter as tk

OBJ_TYPE_BUTTON  = 'button'
OBJ_TYPE_TEXTBOX = 'textbox'
VAR_TYPE_INT     = 'int'
VAR_TYPE_TEXT    = 'text'
FUNC_SAVE        = 'save()'

def calcform(form, vars):
    if (len(form) == 0):
        return 0.0
    
    m = re.fullmatch('\d+\.?\d*|\.\d+', form)
    if (m != None):
        return float(form)

    if (form in vars.keys()):
        return float(vars[form][0])
    
    m = re.search(r'\(.*\)', form)
    if (m != None):
        return calcform(form[:m.start()] + str(calcform(m.group()[1:-1]), vars) + form[m.end():], vars)
    
    m = re.search(r'\+', form)
    if (m != None):
        span = m.start()
        return calcform(form[:span], vars) + calcform(form[span+1:], vars)
    
    m = form.rfind('-')
    if (m != -1):
        span = m
        return calcform(form[:span], vars) - calcform(form[span+1:], vars)
    
    m = re.search(r'\*', form)
    if (m != None):
        span = m.start()
        return calcform(form[:span], vars) * calcform(form[span+1:], vars)
    
    m = form.rfind('/')
    if (m != -1):
        span = m
        return calcform(form[:span], vars) / calcform(form[span+1:], vars)
    
    m = re.search(r'\^', form)
    if (m != None):
        span = m.start()
        return calcform(form[:span], vars) ** calcform(form[span+1:], vars)
    
    return None

def joinText(form, vars):
    if (len(form) == 0):
        return ''

    m = re.search(r'".*"', form)
    if (m!=None):
        return m.group()[1:-1]
    
    m = re.search(r'[a-z_A-Z][a-z_A-Z0-9]+', form)
    if (m!=None):
        return str(vars[m.group()][0])
    
    m = re.search(r'\+', form)
    if (m != None):
        span = m.start()
        return joinText(form[:span], vars) + joinText(form[span+1:], vars)
    return None

def readtext(path, prefix):
    prefix_len = len(prefix)
    textdata = None
    var      = {}
    try:
        with open(path + os.sep + 'default.txt', 'r') as f:
            textdata = f.read()
    except:
        return textdata, var
    
    for value in re.findall(r''+prefix+'.*?'+prefix, textdata):
        if (len(value) and value not in var):
            var[value[prefix_len:-prefix_len]] = [0, VAR_TYPE_INT]

    return textdata, var

def readvars(path, var):
    pattern_variable = r'[a-z_A-Z][a-z_A-Z0-9]+'
    objects   = {}
    lines = ''
    try:
        with open(path + os.sep + 'variable.txt', 'r') as f:
            lines = f.read()
    except:
        return None
    
    for line in lines.split('\n'):
        line_list = line.split(':')
        head = line_list[0].lower()
        if (head == OBJ_TYPE_BUTTON):
            for e in line_list[2].split(','):
                if (e!=FUNC_SAVE):
                    vars = re.findall(pattern_variable, e)
                    for v in vars:
                        if (v not in var.keys()):
                            return None
            objects[line_list[1]] = [OBJ_TYPE_BUTTON]+[''.join(e.split()) for e in line_list[2].split(',')]
        
        if (head == 'textbox' or head == 'input'):
            vars = re.findall(r'[a-z_A-Z][a-z_A-Z0-9]+', line_list[2])
            if (vars[0]==line_list[2] and line_list[2] in var.keys()):
                objects[line_list[2]] = [OBJ_TYPE_TEXTBOX, line_list[2]] 

        elif (re.fullmatch(pattern_variable, head)):
            if (len(line_list) == 2):
                if (line_list[1].lower() == VAR_TYPE_INT):
                    var[line_list[0]] = [0, VAR_TYPE_INT]
                if (line_list[1].lower() == VAR_TYPE_TEXT):
                    var[line_list[0]] = ['', VAR_TYPE_TEXT]
            if (len(line_list) == 3):
                if (line_list[1].lower() == VAR_TYPE_INT):
                    var[line_list[0]] = [int(line_list[2]), VAR_TYPE_INT]
                if (line_list[1].lower() == VAR_TYPE_TEXT):
                    var[line_list[0]] = [int(line_list[2]), VAR_TYPE_TEXT]
        elif (len(head)):
            return None
    return objects

class TextOnlyWindow(tk.Frame):
    def __init__(self, path, master, text, vars, prefix, win_x, win_y, title_name = "Main"):
        super().__init__(master)
        self.pack()
        master.geometry(f'{win_x}x{win_y}')
        master.title(title_name)

        self.labels = []
        self.path = path
        self.master = master
        self.text = text
        self.vars = vars
        self.prefix = prefix
        self.pt_object = None

        self.print_init()

    def print_init(self):
        text = self.text
        for x in self.vars.keys():
            text=text.replace(f'{prefix}{x}{prefix}', str(self.vars[x][0]))

        self.text = self.text.split('\n')
        for l in text.split('\n'):
            self.labels.append(tk.Label(self.master, text=l, wraplength=0))
            self.labels[-1].pack(anchor=tk.NW, side='top', pady=0, ipady =0)
        return

    def Save(self, objects):
        try:
            with open(self.path + os.sep + 'bkp.txt', 'w') as f:
                for x in self.vars:
                    f.write(f'{x}:{self.vars[x][1]}:{self.vars[x][0]}\n')
            return True
        except:
            return False

    def Update_text(self, instructions, objects):
        key = self.vars.keys()
        for x in objects.textboxs.keys():
            v = objects.textboxs[x].get()
            if (self.vars[x][1] == VAR_TYPE_INT):
                try:
                    self.vars[x][0] = int(v)
                except:
                    self.vars[x][0] = 0
            elif (self.vars[x][1] == VAR_TYPE_TEXT):
                self.vars[x][0] = v

        for Sub_formula in instructions:
            if (Sub_formula == FUNC_SAVE):
                if(self.Save(objects)):
                    print("Saved.")
                else:
                    print("Save Failed.")
                continue
            if (Sub_formula[-2:] == '++' and Sub_formula[:-2] in key):
                self.vars[Sub_formula[:-2]][0] += 1
                continue
            if (Sub_formula[-2:] == '--' and Sub_formula[:-2] in key):
                self.vars[Sub_formula[:-2]][0] -= 1
                continue
            if ('+=' in Sub_formula):
                m1 = re.match(r'[a-z_A-Z][a-z_A-Z0-9]+\+=', Sub_formula)
                left  = m1.group()[:-2]
                right = Sub_formula[m1.end():]
                if (self.vars[left][1] == VAR_TYPE_INT):
                    self.vars[left][0] += int(calcform(right, self.vars))
                if (self.vars[left][1] == VAR_TYPE_TEXT):
                    self.self.vars[left][0] += joinText(right, self.vars)
                continue
            if ('-=' in Sub_formula):
                m1 = re.match(r'[a-z_A-Z][a-z_A-Z0-9]+\+=', Sub_formula)
                left  = m1.group()[:-2]
                right = Sub_formula[m1.end():]
                if (self.vars[left][1] == VAR_TYPE_INT):
                    self.vars[left][0] -= int(calcform(right, self.vars))
                continue
            if ('=' in Sub_formula):
                m1 = re.match(r'[a-z_A-Z][a-z_A-Z0-9]+=', Sub_formula)
                left  = m1.group()[:-1]
                right = Sub_formula[m1.end():]
                if (self.vars[left][1] == VAR_TYPE_INT):
                    self.vars[left][0] = int(calcform(right, self.vars))
                if (self.vars[left][1] == VAR_TYPE_TEXT):
                    self.vars[left][0] = joinText(right, self.vars)
            
        for i in range(len(self.labels)):
            text = self.text[i]
            for x in self.vars.keys():
                text = text.replace(f'{prefix}{x}{prefix}', str(self.vars[x][0]))
            self.labels[i]["text"] = text
        return

class Button(tk.Frame):
    def __init__(self,master, mainwin, objects, win_x, win_y, title_name = "Objects"):
        super().__init__(master)
        self.pack()
        master.geometry(f'{win_x}x{win_y}')
        master.title(title_name)

        self.buttons  = []       # [Button_Object, cmd]
        self.textboxs = {}       #key = name;
        self.mainwin = mainwin
        button_size_x = 10
        button_size_y = 1

        for b in objects.keys():
            if (objects[b][0] == OBJ_TYPE_BUTTON):
                inst = []
                if (len(objects[b]) > 1):
                    inst = objects[b][1:]

                button_size_y = len(b.split('\\n'))
                self.buttons.append(tk.Button(master,text=b.replace('\\n', '\n'), command=self.buttonClick(inst), width = button_size_x, height=button_size_y))
                #self.buttons[-1].place(x=pos_, y=pos_y)
                self.buttons[-1].config(fg="black", bg="pink")
                self.buttons[-1].pack(anchor=tk.W, side='top', pady=5)

            elif (objects[b][0] == OBJ_TYPE_TEXTBOX):
                self.textboxs[b] = tk.Entry(master)
                self.textboxs[b].insert(tk.END, b)
                self.textboxs[b].pack(anchor=tk.W, side='top', pady=5)

    def buttonClick(self, instruction):
        def func():
            self.mainwin.Update_text(instruction, self)
        return func

if __name__ == '__main__':
    prefix = '//'
    title_text   = 'Counter'
    title_Objects = '操作側ウインドウ'
    win_x = 300
    win_y = 300

    this_dir           = os.path.dirname(sys.argv[0])
    textdata, variable = readtext(this_dir, prefix)
    objects            = readvars(this_dir, variable)
    if (textdata==None):
        print('error:Can\'t open default.txt')
        sys.exit()
    if (objects==None):
        print('error:Error in variable.txt')
        sys.exit()
    text_win = tk.Tk()
    text_Window = TextOnlyWindow(this_dir,  text_win, textdata, variable, prefix, win_x, win_y, title_name = title_text)
    
    if (len(objects)):
        button_win = tk.Tk()
        Button_Window = Button(button_win, text_Window, objects, win_x, win_y, title_name = title_Objects)

    text_Window.mainloop()
