data = open('train.data', 'w')
labels = open('train.labels', 'w')

with open('raw_train_data.txt', 'r') as raw_data:
    for line in raw_data:
        if line.startswith('<COUNT>'):
            l = line.lstrip('<COUNT> ')
            data.write(l)
            print("COUNT", file=labels)
        else:
            data.write(line)
            print("LIST", file=labels)
