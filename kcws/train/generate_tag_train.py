# -*- coding: utf-8 -*-
# get each word or char's vector index in word_vec.txt and char.txt
# outfile contains vector index instead of word vector
import sys
import os
import w2v

totalLine = 0
longLine = 0

MAX_LEN = 140
totalChars = 0


class Sentence:
	def __init__(self):
		self.tokens = []
		self.markWrong = False

	def addToken(self, token):
		self.tokens.append(token)

	def generate_train_line(self, out, word_vob):
		'''
		store word/char 's vector index in each line
		'''
		def split_long_token():
			index_list = []
			split_token_list = []
			for index, ele in enumerate(self.tokens):
				if ele.token in ['。', '！', '？']:
					index_list.append(index)
			for i, split_index in enumerate(index_list):
				if i == 0:
					split_tokens = self.tokens[:split_index + 1]
				else:
					split_tokens = self.tokens[index_list[i - 1]:split_index + 1]
				split_token_list.append(split_tokens)
			return split_token_list



		nl = len(self.tokens)
		if nl < 2:
			return
		token_list = []
		if nl > MAX_LEN:
			token_list = split_long_token()
		else:
			token_list.append(self.tokens)

		for tokens in token_list:
			nl = len(tokens)
			nl = MAX_LEN if nl > MAX_LEN else nl
			wordi = []
			# chari = []
			labeli = []
			for ti in range(nl):
				t = tokens[ti]
				idx = word_vob.GetWordIndex(t.token)
				wordi.append(str(idx))
				labeli.append(str(t.Tag))

			for i in range(nl, MAX_LEN):
				wordi.append("0")
				labeli.append("0")
			# print(len(wordi), len(labeli))
			line = " ".join(wordi)
			line += " "
			# line += " ".join(chari)  # lengh = 10
			# line += " "
			line += " ".join(labeli)
			ss = line.split(' ')
			assert(len(ss) == MAX_LEN * 2), 'line len:{}, MAX_LEN {}'.format(len(ss), MAX_LEN * 2)
			
			out.write("%s\n" % (line))


class Token:  # add token token's char and tag information
	def __init__(self, token, Tag):
		self.token = token
		self.Tag = Tag


def processToken(token, sentence, tag_vob):
	token = token.split('/')
	assert(len(token) == 2), token
	tag = token[1]
	word = token[0]
	if not tag.isalpha() or not tag.isupper():
		sentence.markWrong = True
		return False
	if tag not in tag_vob:
		print("mark wrong for:[%s]" % (tag))
		sentence.markWrong = True
		return False

	word = word.strip()
	sentence.addToken(Token(word, tag_vob[tag]))
	return True


def processLine(line, out, vec_vob, tag_vob):
	line = line.strip()
	line = line.split('\t')

	sentence = Sentence()
	for token in line:
		processToken(token, sentence, tag_vob)
	if (not sentence.markWrong) and len(sentence.tokens) > 0:
		sentence.generate_train_line(out, vec_vob)


def loadtagVob(path, vob):
	fp = open(path, "r")
	for line in fp.readlines():
		line = line.strip()
		if not line:
			continue
		ss = line.split("\t")
		vob[ss[0]] = int(ss[1])
	pass


def split_train_testing(data_path):
	def get_traingin_testing_data(data_path):
		with open(data_path, 'r') as fp:
			all_text = fp.readlines()
			file_len = len(all_text)
			training_text = all_text[: (8 * file_len) / 10]
			testing_text = all_text[(8 * file_len) / 10:]
		return training_text, testing_text

	def write_to_file(file_path, data_lines):
		with open(file_path, 'w') as wf:
			for line in data_lines:
				line = line.strip()
				wf.write('{}\n'.format(line))

	train, test = get_traingin_testing_data(data_path)
	file_name = data_path.split('.')
	write_to_file(file_name[0] + '_for_train.' + file_name[1], train)
	write_to_file(file_name[0] + '_for_test.' + file_name[1], test)



def main(argc, argv):
	global totalLine
	global longLine
	global totalChars
	if argc < 5:
		print("Usage:%s <vec_vob> <tag_vob> <corpus> <output>" %
					(argv[0]))
		sys.exit(1)
	# wvobPath = argv[1]
	cvobpath = argv[1]
	pvobPath = argv[2]
	corpusPath = argv[3]
	vec_vob = w2v.Word2vecVocab()
	vec_vob.Load(cvobpath)
	tagVob = {}
	loadtagVob(pvobPath, tagVob)
	out = open(argv[4], "w")
	with open(corpusPath, 'r') as fp:
		all_text = fp.readlines()
		file_len = len(all_text)
		for count, line in enumerate(all_text):
			line = line.strip()

			if count % 1000 == 0:
				print(count, file_len)
			processLine(line, out, vec_vob, tagVob)

	out.close()
	print("total:%d, long lines:%d, chars:%d" %
				(totalLine, longLine, totalChars))

	split_train_testing(argv[4])

if __name__ == '__main__':
	main(len(sys.argv), sys.argv)
