import utils

for noun in range(0, 100):
    for verb in range(0, 100):

        for line in utils.iterstrip('input-02.txt'):
            opcode = [int(_) for _ in line.split(',')]

        opcode[1] = noun
        opcode[2] = verb

        for i in range(0, len(opcode), 4):

            op = opcode[i]
            if op == 99:
                break

            pa, pb, po = opcode[(i+1):(i+4)]

            a = opcode[pa]
            b = opcode[pb]
            if op == 1:
                opcode[po] = a + b
            elif op == 2:
                opcode[po] = a * b
            else:
                raise 'STOP'

        if opcode[0] == 19690720:
            print(noun, verb, 100 * noun + verb)
    
