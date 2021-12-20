import psutil

def printStats():
    length = 20
    #print resource usage
    info = ''
    prog = ''
    percent = int(psutil.cpu_percent()/100*length)
    for i in range(percent):
        prog += '█'
    for i in range(length-percent):
        prog += '░'


    info = 'cpu: ' + str(psutil.cpu_percent()) + '% ' + prog + ' | '
    prog = ''
    svmem = psutil.virtual_memory()
    percent = int(svmem.used/svmem.total*length)
    for i in range(percent):
        prog += '█'
    for i in range(length-percent):
        prog += '░'
    info += 'memory: ' + str(int(svmem.used/svmem.total*100)) + '% ' + prog
    print(info, end='\r')
