import shlex

# goal: network > getDevice 9 R1 > getCommandLine > enterCommand 8 "conf t"   
# trace: network\0 0 \0getDevice\09\0R1\0 0 \0getCommandLine\0 0 \0

#        network\0 0 \0getDevice\09\0R1\0 0 \0moveToLocationCentered\04\0200\04\0200\0 0 \0

# find a way to insert arguments dynamically.

# network getDevice 9 R1 getCommandLine enterCommand 8 "conf t"
string = 'network > getDevice 9 "R1" > getCommandLine > enterCommand 8 "conf t"'
tokens = shlex.split(string)

print(tokens)
temp = []

for i in range(len(tokens)):
    if tokens[i] == ">":
        temp.pop()
        temp.append(r"\0 0 \0")
    else:
        temp.append(tokens[i])
        temp.append(r'\0')

    if i == len(tokens) - 1:
        temp.pop()
        temp.append(r"\0 0 \0")

command = "".join(temp)

print(temp)
print(command)

    