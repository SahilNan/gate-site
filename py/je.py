import os

rfile = open('/Users/lakshmi/Documents/workspace-spring-tool-suite-4-4.12.1.RELEASE/ai/gt/html/qp_keys/res.txt', "r")
lines = rfile.readlines()
rfile.close()
for line in lines:
    cols = line.split(",")
    if len(cols) > 4:
        op1 = int(cols[2])
        op2 = int(cols[3])
        op3 = int(cols[4])
        op4 = int(cols[5])
        oorder = {1: op1, 2: op2, 3: op3, 4: op4}
        opts = [op1,op2,op3,op4]
        opts.sort()
        ooorder = {opts[0]: 1, opts[1]: 2, opts[2]: 3,opts[3]: 4}
        ch = int(cols[6]) 
        print(line.strip(),",",ooorder.get(oorder.get(ch)))
    else:
        print(line.strip())