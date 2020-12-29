def iterstrip(filename='input.txt'):
    with open(filename) as infile:
        for line in infile:
            yield line.strip()
