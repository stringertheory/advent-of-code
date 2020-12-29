import utils

DIVIDE = 20201227

def find_ls(pk, subject_number=7, divide=DIVIDE, max_iter=10000000000):
    index = 1
    value = 1
    while True and index < max_iter:
        value *= subject_number
        value = value % divide
        if value == pk:
            return index
        # print(index, value)
        index += 1

def key(subject_number, loop_size, divide=DIVIDE, max_iter=10000000000):
    value = 1
    for i in range(loop_size):
        value *= subject_number
        value = value % divide
    return value

pk1, pk2 = list(int(i) for i in utils.iterstrip('input-25.txt'))
print(pk1, pk2)

        
# value = 1
# card_loop_size = 1
# card_public_key = 1
# door_loop_size = 1
# door_public_key = 1
# subject_number = 7


loopsize1 = find_ls(pk1)
loopsize2 = find_ls(pk2)
print(loopsize1, loopsize2)
print(key(pk1, loopsize2))
print(key(pk2, loopsize1))
