import sys
import os
import re
import Tag as T


def load_corpus(rootDir):
    for dirName, subdirList, fileList in os.walk(rootDir):
        # print(dirName, subdirList, fileList, rootDir)
        # curDir = os.path.join(rootDir, dirName)
        for file in fileList:
            if file.endswith('.txt'):
                curFile = os.path.join(dirName, file)
                with open(curFile, 'r') as f:
                    for line in f.readlines():
                        line = line.strip()
                        yield line


def process_Token(words):
    assert(isinstance(words, str))
    token_list = []
    word_len = len(words)
    if word_len == 1:
        token_list.append(T.Token(words[0], T.Tag_BMES.S.name))
    else:
        for i in range(word_len):
            word = words[i]
            if i == 0:
                token_list.append(T.Token(word, T.Tag_BMES.B.name))
            elif i == (word_len - 1):
                token_list.append(T.Token(word, T.Tag_BMES.E.name))
            else:
                token_list.append(T.Token(word, T.Tag_BMES.M.name))
    return token_list


def process_lines(one_line):
    '''
    @one_line: ['迈向 充满 希望 的 新 世纪 —— 一九九八年 新年 讲话 ( 附 图片 0 张 )']
    '''
    token_list = []
    line = one_line.strip().split(' ')
    # token_list.append(T.Token(one_line[0], T.Tag_BMES.S.name))
    for index, ele in enumerate(line):
        token_list.extend(process_Token(ele))
    # token_list.append(T.Token(one_line[2], T.Tag_BMES.S.name))

    string_ = T.token2String(token_list, separator='\t')
    return string_


def process_corpus(corpus):
    # pat = r'<[/]{0,1}(\w+)>'
    # pat = r'^(<\w+>)(.*)(</\w+>)$'
    # pat = re.compile(pat)
    for index, one_line in enumerate(corpus):
        # print(one_line)
        # match = pat.findall(one_line)[0]
        tagged_string = process_lines(one_line)
        if tagged_string:
            yield tagged_string


def write_file(path, data):
    with open(path, 'w') as wf:
        for line in data:
            wf.write('{}\n'.format(line))


def main(argc, argv):
    if argc < 3:
        print("Usage: {} <dir> <output>".format(argv[0]))
        sys.exit(0)

    root_Dir = argv[1]
    output_file = argv[2]
    corpus_gen = load_corpus(root_Dir)
    tagged_string_gen = process_corpus(corpus_gen)
    write_file(output_file, tagged_string_gen)
    # print('total line:{} long line:{}'.format(totalLine, longLine))


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
