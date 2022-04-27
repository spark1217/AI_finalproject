import os

for i in range(5):
    cmd = "pdfschedule "+"new"+str(i)+".yml"
    os.system(cmd)