import os
SETTINGFILE_PATH = os.path.abspath('D:\\LeaveManage\\setting\\globalsetting.ini')
TEMPLATE_PATH = os.path.abspath('..\\server\\template')

def gettemplatepath(templatename):
    return os.path.join(TEMPLATE_PATH,templatename)

def getconfig(configname):
    with open(SETTINGFILE_PATH,'r') as f:
        lines = f.readlines()
        for line in lines:
            header = line.split('=')[0]
            if header == configname:
                value = line.split('=')[1]
                if '\n' in value:
                    value = value[:-1]
                return value
        return ''