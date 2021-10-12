import os


symbols=["SP","LCL","ARG","THIS","THAT","SCREEN","KBD"]
symbolvalues=[0,1,2,3,4,16384,24576]
symbols.append("R0")
symbols.append("R1")
symbols.append("R2")
symbols.append("R3")
symbols.append("R4")
symbols.append("R5")
symbols.append("R6")
symbols.append("R7")
symbols.append("R8")
symbols.append("R9")
symbols.append("R10")
symbols.append("R11")
symbols.append("R12")
symbols.append("R13")
symbols.append("R14")
symbols.append("R15")
for i in range(16):
    symbolvalues.append(i)
symbol_table={}
for i in range(len(symbols)):
    symbol_table[symbols[i]]=symbolvalues[i]
filename="./pong/Pong.asm"
f1=open(filename,'r')
lines=[]
line_num=0
line=f1.readline()
# print(type(line))
# print(line)
# print(len(line))
while line :
    # print(line_num)
    line = ''.join(line.split())
    # print(line)
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
        if line[0] =="(":
            if line[-1]==")":
                symbol_table[line[1:-1]]=line_num
            else:
                print("error")
        else:
            lines.append(line)
            line_num+=1  
    line=f1.readline()
# print(lines)
f1.close()

address_used=16


# print(symbol_table)
f_out=open("./Pong.hack","w")

for i in range(len(lines)):
    print(i)
    line=lines[i]
    print(line)
    if line[0] =="@":
        # A instruction
        if line[1:].isnumeric():
            addr=int(line[1:])
            
        else:
            if line[1:] in symbol_table:
                addr=symbol_table[line[1:]]
            else:
                addr=address_used
                symbol_table[line[1:]]=address_used
                address_used+=1
        print(addr)
        temp = format(addr, "b")
        temp=str(temp).zfill(16)
        f_out.write(temp+"\n")
    else:
        # C instruction
        e_index=line.find("=")
        j_index=line.find(";")
        # print(e_index,j_index)
        if e_index == -1:
            dest="000"
        else:
            des=line[0:e_index]
            print("destination: {}".format(des))
            if des == "M":
                dest="001"
            if des == "D":
                dest="010"
            if des == "MD":
                dest="011"
            if des == "A":
                dest="100"
            if des == "AM":
                dest="101"
            if des == "AD":
                dest="110"
            if des == "AMD":
                dest="111"
        if j_index ==-1:
            jump="000"
        else:
            jmp=line[j_index+1:]
            print("jump: {}".format(jmp))
            if jmp == "JGT":
                jump="001"
            if jmp == "JEQ":
                jump="010"
            if jmp == "JGE":
                jump="011"
            if jmp == "JLT":
                jump="100"
            if jmp == "JNE":
                jump="101"
            if jmp == "JLE":
                jump="110"
            if jmp == "JMP":
                jump="111"
        print(e_index,j_index)
        if j_index == -1:
            ope=line[e_index+1:]
        else:
            ope=line[e_index+1:j_index]
        
        print(ope)
        if ope == "0":
            action="0101010"
        if ope == "1":
            action="0111111"
        if ope == "-1":
            action="0111010"
        if ope == "D":
            action="0001100"
        if ope == "A":
            action="0110000"
        if ope == "M":
            action="1110000"
        if ope == "!D":
            action="0001101"
        if ope == "!A":
            action="0110001"
        if ope == "!M":
            action="1110001"
        if ope == "-D":
            action="0001111"
        if ope == "-A":
            action="0110011"
        if ope == "-M":
            action="1110011"
        if ope == "D+1":
            action="0011111"
        if ope == "A+1":
            action="0110111"
        if ope == "M+1":
            action="1110111"
        if ope == "D-1":
            action="0001110"
        if ope == "A-1":
            action="0110010"
        if ope == "M-1":
            action="1110010"
        if ope == "D+A":
            action="0000010"
        if ope == "D+M":
            action="1000010"
        if ope == "D-A":
            action="0010011"
        if ope == "D-M":
            action="1010011"
        if ope == "A-D":
            action="0000111"
        if ope == "M-D":
            action="1000111"
        if ope == "D&A":
            action="0000000"
        if ope == "D&M":
            action="1000000"
        if ope == "D|A":
            action="0010101"
        if ope == "D|M":
            action="1010101"

        f_out.write("111"+action+dest+jump+"\n")
print(symbol_table)
f_out.close()







