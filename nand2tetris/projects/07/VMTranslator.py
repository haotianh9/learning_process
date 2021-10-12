import os,sys

if len(sys.argv) == 2:
    filename=sys.argv[1]
    # "./MemoryAccess/BasicTest/BasicTest.vm"
# "./MemoryAccess/BasicTest/BasicTest.asm"

name=filename.split('/')[-1][:-3]
output_name=filename[:-3]+".asm"
print(output_name)
f1=open(filename,'r')
lines=[]
line=f1.readline()
# print(type(line))
# print(line)
# print(len(line))
while line :
    # print(line_num)
    # line = ''.join(line.split())
    # print(line)
    line=line[0:-1]
    flag=False
    for i in range(1,len(line)):
        if line[i] == '/' and line[i-1]== '/':
            end=i-1
            flag=True
            break
    if flag:
        line=line[0:end]
    # print(end)
    # print(line)
    if len(line) > 0:

        lines.append(line)

    line=f1.readline()
# print(lines)
f1.close()


f_out=open(output_name,"w")

map={"local":"LCL" ,"this":"THIS","that":"THAT","argument":"ARG"}
map_pointer={"0":"THIS","1":"THAT"}
map_jmp={'eq':  'JEQ',
        'lt': 'JLT',
        'gt':  'JGT'}
comp_count=0
for i,line in enumerate(lines):
    print(line)
    f_out.write("// "+line +"\n")
    seg=line.split()
    if seg[0] == "push":
        if seg[1] == "constant":
            f_out.write("@"+seg[2]+"\n")
            f_out.write("D=A\n")
            f_out.write("@SP\n")
            f_out.write("A=M\n")
            f_out.write("M=D\n")
            f_out.write("@SP\n")
            f_out.write("M=M+1\n")
        elif seg[1] in map:
            f_out.write("@"+seg[2]+"\n")
            f_out.write("D=A\n")
            f_out.write("@"+map[seg[1]]+"\n")
            f_out.write("A=M+D\n")
            f_out.write("D=M\n")
            f_out.write("@SP\n")
            f_out.write("A=M\n")
            f_out.write("M=D\n")
            f_out.write("@SP\n")
            f_out.write("M=M+1\n")
        elif seg[1] == "static":
            f_out.write("@"+name+"."+seg[2]+"\n")
            f_out.write("D=M\n")
            f_out.write("@SP\n")
            f_out.write("A=M\n")
            f_out.write("M=D\n")
            f_out.write("@SP\n")
            f_out.write("M=M+1\n")
        elif seg[1] == "temp": 
            f_out.write("@"+seg[2]+"\n")
            f_out.write("D=A\n")
            f_out.write("@5\n")
            f_out.write("A=A+D\n")
            f_out.write("D=M\n")
            f_out.write("@SP\n")
            f_out.write("A=M\n")
            f_out.write("M=D\n")
            f_out.write("@SP\n")
            f_out.write("M=M+1\n")
        elif seg[1] == "pointer":
            if seg[2] in map_pointer:
                f_out.write("@"+seg[2]+"\n")
                f_out.write("D=A\n")
                f_out.write("@3\n")
                f_out.write("A=A+D\n")
                f_out.write("D=M\n")
                f_out.write("@SP\n")
                f_out.write("A=M\n")
                f_out.write("M=D\n")
                f_out.write("@SP\n")
                f_out.write("M=M+1\n")
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError
    elif seg[0] == "pop":
        if seg[1] in map:
            f_out.write("@"+seg[2]+"\n")
            f_out.write("D=A\n")
            f_out.write("@"+map[seg[1]]+"\n")
            f_out.write("D=M+D\n")
            f_out.write("@R13\n")
            f_out.write("M=D\n")
            f_out.write("@SP\n")
            f_out.write("AM=M-1\n")
            f_out.write("D=M\n")
            f_out.write("@R13\n")
            f_out.write("A=M\n")
            f_out.write("M=D\n")
        elif seg[1] ==  "static":
            f_out.write("@SP\n")
            f_out.write("AM=M-1\n")
            f_out.write("D=M\n")
            f_out.write("@"+name+"."+seg[2]+"\n")
            f_out.write("M=D\n")
        elif seg[1] ==  "temp":
            f_out.write("@"+seg[2]+"\n")
            f_out.write("D=A\n")
            f_out.write("@5\n")
            f_out.write("D=A+D\n")
            f_out.write("@R13\n")
            f_out.write("M=D\n")
            f_out.write("@SP\n")
            f_out.write("AM=M-1\n")
            f_out.write("D=M\n")
            f_out.write("@R13\n")
            f_out.write("A=M\n")
            f_out.write("M=D\n")
        elif seg[1] ==  "pointer":
            # print( seg[2])
            if seg[2] in map_pointer:
                f_out.write("@"+seg[2]+"\n")
                f_out.write("D=A\n")
                f_out.write("@3\n")
                f_out.write("D=A+D\n")
                f_out.write("@R13\n")
                f_out.write("M=D\n")
                f_out.write("@SP\n")
                f_out.write("AM=M-1\n")
                f_out.write("D=M\n")
                f_out.write("@R13\n")
                f_out.write("A=M\n")
                f_out.write("M=D\n")
            else:
                raise NotImplementedError
    elif seg[0] == "add":
        f_out.write("@SP\n")
        f_out.write("AM=M-1\n")
        f_out.write("D=M\n")
        f_out.write("@SP\n")
        f_out.write("AM=M-1\n")
        f_out.write("M=D+M\n")
        f_out.write("@SP\n")
        f_out.write("M=M+1\n")
    elif seg[0] == "sub":
        f_out.write("@SP\n")
        f_out.write("AM=M-1\n")
        f_out.write("D=M\n")
        f_out.write("@SP\n")
        f_out.write("AM=M-1\n")
        f_out.write("M=M-D\n")
        f_out.write("@SP\n")
        f_out.write("M=M+1\n")
    elif seg[0] == "or":
        f_out.write("@SP\n")
        f_out.write("AM=M-1\n")
        f_out.write("D=M\n")
        f_out.write("@SP\n")
        f_out.write("AM=M-1\n")
        f_out.write("M=D|M\n")
        f_out.write("@SP\n")
        f_out.write("M=M+1\n")
    elif seg[0] == "and":
        f_out.write("@SP\n")
        f_out.write("AM=M-1\n")
        f_out.write("D=M\n")
        f_out.write("@SP\n")
        f_out.write("AM=M-1\n")
        f_out.write("M=D&M\n")
        f_out.write("@SP\n")
        f_out.write("M=M+1\n")
    elif seg[0] == "neg":
        f_out.write("@SP\n")
        f_out.write("A=M-1\n")
        f_out.write("M=-M\n")
    elif seg[0] == "not":
        f_out.write("@SP\n")
        f_out.write("A=M-1\n")
        f_out.write("M=!M\n")
    elif seg[0]  in map_jmp:
        label='{}{}'.format( seg[0],str(comp_count))
        comp_count+=1
        f_out.write("@SP\n")
        f_out.write("AM=M-1\n")
        f_out.write("D=M\n")
        f_out.write("@SP\n")
        f_out.write("A=M-1\n")
        f_out.write("D=M-D\n")
        f_out.write("M=-1\n")
        f_out.write("@"+label+"\n")
        f_out.write("D;"+map_jmp[seg[0]]+"\n")
        f_out.write("@SP\n")
        f_out.write("A=M-1\n")
        f_out.write("M=0\n")
        f_out.write("("+label+")\n")

