# endure - make html MORE easier
import sys
from os import getcwd
from subprocess import check_output
from termcolor import cprint
from random import randint
ENDURE_CV = 1
ENDURE_ARGS = sys.argv[1:]
ENDURE_DOC = ""
backslashn = '\n'
whereto = ""
ENDURE_BODYTEMP = ""
ENDURE_BODYBACK = "#FFFFFF"
ticktock = 0
ENDURE_HEADTEMP = ""
ENDURE_OTHERTEMP = ""
packed = "packed"
embedded = "embedded"
ENDURE_PROJNAME = "noname"
ENDURE_PROJTYPE=embedded
ENDURE_DATA = "data/"
ENDURE_IMG = ENDURE_DATA+"img/"
ENDURE_SCRIPTS = ENDURE_DATA+"scripts/"
ENDURE_IMAGELIST = []
ENDURE_SCRIPTSLIST = []

def project(name, typeof):
    global ENDURE_PROJNAME, ENDURE_PROJTYPE
    ENDURE_PROJTYPE = typeof
    ENDURE_PROJNAME = name
def loadf(mod):
    global ticktock
    with open(mod) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
    for command in content:
        ticktock+=1
        exec(command)
def cc_err(error):
    cprint("error: "+error+" at line "+str(ticktock), 'red')
    exit(1)
def write_doc():
    if whereto == "/dev/tty":
        print(ENDURE_DOC)
        exit()
    o = open(whereto, "w+")
    o.write(ENDURE_DOC)
    o.close()
def generate():
    global ENDURE_DOC
    ENDURE_DOC = "<!DOCTYPE HTML>\n"
    ENDURE_DOC = ENDURE_DOC+"<html>\n"
    ENDURE_DOC = ENDURE_DOC+"<!--Autogenerated html with endure, DO NOT EDIT -->"+backslashn
    ENDURE_DOC = ENDURE_DOC+"<head>\n"
    ENDURE_DOC = ENDURE_DOC+ENDURE_HEADTEMP
    ENDURE_DOC = ENDURE_DOC+"</head>\n"
    ENDURE_DOC = ENDURE_DOC+'<body bgcolor="{}">\n'.format(ENDURE_BODYBACK)
    ENDURE_DOC = ENDURE_DOC+ENDURE_BODYTEMP
    ENDURE_DOC = ENDURE_DOC+"</body>\n"
    ENDURE_DOC = ENDURE_DOC+ENDURE_OTHERTEMP
    ENDURE_DOC = ENDURE_DOC + "</html>\n"
def setcharset(charset):
    global ENDURE_HEADTEMP
    ENDURE_HEADTEMP = ENDURE_HEADTEMP + '<meta charset="{}">'.format(charset) 
def header(*arg):
    global ENDURE_BODYTEMP
    arlen = len(arg)
    text = arg[0]
    align = 'left'
    size = "1"
    color = "black"
    ide = "ffff"
    if arlen > 1:
        size = arg[1]
    if arlen > 2:
        align = arg[2]
    if arlen > 3:
        color = arg[3]
    if arlen > 4:
        ide = arg[4]
    if size > 8 or size < 1:
        cc_err("bad <h> size: "+str(int(size)))
    if align == 'left' or align == 'right' or align == 'center':
        pass
    else:
        cc_err("bad align: "+align)
    if not ide == "ffff":
        ENDURE_BODYTEMP = ENDURE_BODYTEMP + '<h{} align={} style="color:{}" id="{}">{}</h{}>\n'.format(size, align, color, ide, text, size)
    else:
        ENDURE_BODYTEMP = ENDURE_BODYTEMP + '<h{} align={} style="color:{}">{}</h{}>\n'.format(size, align, color, text, size)
def background(cl):
    global ENDURE_BODYBACK
    ENDURE_BODYBACK = cl
def paragraph(*arg):
    global ENDURE_BODYTEMP
    arlen = len(arg)
    align = "left"
    text = arg[0]
    color = "black"
    ide = "ffff"
    if arlen > 1:
        align = arg[1]
    if arlen > 2:
        color = arg[2]
    if arlen > 3:
        ide = arg[3]
    if align == 'left' or align == 'right' or align == 'center':
        pass
    else:
        cc_err("bad align: "+align)
    if not ide == "ffff":
        ENDURE_BODYTEMP = ENDURE_BODYTEMP + '<p align={} style="color:{}" id="{}">'.format(align, color, ide)+text+"</p>"+backslashn
    else:
        ENDURE_BODYTEMP = ENDURE_BODYTEMP + '<p align={} style="color:{}">'.format(align, color)+text+"</p>"+backslashn
def title(hdr):
    global ENDURE_HEADTEMP
    ENDURE_HEADTEMP = ENDURE_HEADTEMP + "<title>"+hdr+"</title>\n"
def button(*arg):
    global ENDURE_BODYTEMP
    action = "ffff"
    align = "left"
    arlen = len(arg)
    text = arg[0]
    if arlen > 1:
        action = arg[1]
    if arlen > 2:
        align = arg[2]
    if align == 'left' or align == 'right' or align == 'center':
        pass
    else:
        cc_err("bad align: "+align)
    ENDURE_BODYTEMP = ENDURE_BODYTEMP + "<button align={}".format(align)
    if not action == "ffff":
        ENDURE_BODYTEMP = ENDURE_BODYTEMP + 'onclick="{}">{}</button>\n'.format(action, text)
    else:
        ENDURE_BODYTEMP = ENDURE_BODYTEMP + '>{}</button>\n'.format(text)
def html(code):
    global ENDURE_OTHERTEMP
    ENDURE_OTHERTEMP = ENDURE_OTHERTEMP + code
def insert_img(*args):
    global ENDURE_BODYTEMP
    imgpath = args[0]
    align = "left"
    argslen = len(args)
    if argslen > 1:
        align = args[1]
    if align == 'left' or align == 'right' or align == 'center':
        pass
    else:
        cc_err("bad align: "+align)
    ENDURE_BODYTEMP = ENDURE_BODYTEMP + '<img src="{}" align="{}">'
    ENDURE_IMAGELIST[len(ENDURE_IMAGELIST)] = imgpath
def href(*a):
    global ENDURE_BODYTEMP
    alen = len(a)
    text = "ffff"
    hreff = a[0]
    if alen > 1:
        text = a[1]
    if not text == "ffff":
        ENDURE_BODYTEMP = ENDURE_BODYTEMP + '<p><a href="{}">{}</a></p>\n'.format(hreff, text)
    else:
        ENDURE_BODYTEMP = ENDURE_BODYTEMP + '<p><a href="{}"></a></p>\n'.format(hreff)
def dino():
    global whereto
    if "-o" in ENDURE_ARGS:
        if ENDURE_PROJTYPE == embedded:
            whereto = getcwd()+"/"+ENDURE_ARGS[ENDURE_ARGS.index("-o")+1]
            endfile = getcwd()+"/"+ENDURE_ARGS[0]
            loadf(endfile)
            generate()
            write_doc()
        else:
            check_output("mkdir -p "+ENDURE_PROJNAME)
            check_output("mkdir -p "+ENDURE_PROJNAME+"/"+ENDURE_DATA)
            check_output("mkdir -p "+ENDURE_PROJNAME+"/"+ENDURE_IMG)
            check_output("mkdir -p "+ENDURE_PROJNAME+"/"+ENDURE_SCRIPTS)
            whereto = getcwd()+"/"+ENDURE_PROJNAME+"/"+ENDURE_ARGS[ENDURE_ARGS.index("-o")+1]
            loadf(endfile)
            generate()
            write_doc()
            for image in ENDURE_IMAGELIST:
                check_output("cp {} {}".format(image, ENDURE_IMG))
            for script in ENDURE_IMAGELIST:
                check_output("cp {} {}".format(script, ENDURE_SCRIPTS))
    else:
        whereto = "/dev/tty"
        endfile = getcwd()+"/"+ENDURE_ARGS[0]
        loadf(endfile)
        generate()
        write_doc()
if __name__ == "__main__":
    dino()