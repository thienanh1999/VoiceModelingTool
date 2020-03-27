from nltk.tokenize import sent_tokenize, word_tokenize

topic = 'YKien'

source = topic + '/raw.txt'

file = open(source)
content = file.read()
file.close()
lines = content.split('\n')
link = lines[0]
lines.pop(0)

data = ''
for line in lines:
    data = data + line + ' '
sents = sent_tokenize(data)

dest = topic + '/article.txt'
file1 = open(dest, "w")
file1.write(link)
count = -1


def to_string(count):
    result = str(count)
    while len(result) < 3:
        result = '0' + result
    result = result + '.wav'
    return result


for s in sents:
    file1.write('\n')
    count += 1
    file1.write(to_string(count))
    file1.write('\n')
    file1.write(s)
file1.close()
