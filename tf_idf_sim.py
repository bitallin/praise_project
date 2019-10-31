import jieba
import re
from gensim import corpora, models, similarities


def load_original_data(path):
    # load data from txt => list []
    data_list = []

    for line in open(path, 'r', encoding='utf-8'):
        line = line.strip("\n")

        data_list.append(line)

    print('length of list:', str(len(data_list)))
    # return ['句子', '句子']
    return data_list


def to_pure_chinese(text):
    text = re.findall(r'[\u4e00-\u9fa5]', text.strip())
    text = ''.join(text)
    return text


def load_data(path):
    #  1. load data
    #  return original data list
    #     and pure text data list
    original_txt_list = load_original_data(path)
    pure_cn_list = list(map(to_pure_chinese, original_txt_list))
    return original_txt_list, pure_cn_list


def sentence2words(sentence):
    # in: '我是个菜鸡'
    # out: ['我','是'，‘个’，‘菜鸡’]
    return [word for word in jieba.cut(sentence)]


def generate_dictionary(segments_list):
    dictionary = corpora.Dictionary(segments_list)
    # print(dictionary.token2id)
    print('words num:', str(len(dictionary.keys())))
    return dictionary


def find_feature_word(segments, words_num=3):
    # use global variables: tf-idf model, dictionary
    # find the feature words
    # words num: 3
    res = model[segments]
    res = sorted(res, key=lambda item: -item[1])
    feature_words = []
    for i in range(words_num):
        feature_words.append(dictionary[res[i][0]])
    return feature_words


def generate_feature_words_list():
    return list(map(find_feature_word, bow_list))


def find_sim_sentence(text, sentence_num=20):
    # use global variables: model, bow_list, dictionary
    index = similarities.SparseMatrixSimilarity(model[bow_list],
                                                num_features=len(dictionary.keys()))
    res = to_pure_chinese(text)
    res = sentence2words(res)
    res = dictionary.doc2bow(res)

    sim = index[model[res]]
    res = sorted(enumerate(sim), key=lambda item: -item[1])
    sim_sentence_list = []
    for i in range(sentence_num):
        sim_sentence_list.append(original_txt_list[res[i][0]])
    print('sim sentences:', sim_sentence_list)
    return sim_sentence_list


# 1. load data
path = 'data/praise_dataset.txt'
original_txt_list, pure_cn_list = load_data(path)
# ['您是一位有恒心有毅力的人我很佩服您', '越有内涵的人越虚怀若谷像您这样有内涵的人我十分敬佩',]

# 2. word segmentation
segments_list = list(map(sentence2words, pure_cn_list))
# [['您', '是', '一位', '有恒心', '有', '毅力', '的', '人', '我', '很', '佩服', '您'], ['越有', '内涵', '的', '人', '越', '虚怀若谷', '像', '您', '这样', '有', '内涵', '的', '人', '我', '十分', '敬佩'

# 3. create dictionary by segments_list

dictionary = generate_dictionary(segments_list)
# Dictionary(2009 unique tokens: ['一位', '人', '佩服', '很', '您']...)

# 4. generate bow_list
# BoW: Bags of Words
bow_list = [dictionary.doc2bow(item) for item in segments_list]
#  每一句话按照词的索引，并统计有多少词
# [[(0, 1), (1, 1), (2, 1), (3, 1), (4, 2), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1)] ]


# 5. generate tf-idf model
model = models.TfidfModel(bow_list)

# 6. calculate the feature word of every record
#         calculate tf-idf of each words in every segments

# feature_list = list(map(find_feature_word, bow_list))
find_sim_sentence("不想了")
