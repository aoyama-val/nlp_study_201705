# -*- coding: utf-8 -*-

import zipfile, io
import pandas as pd
import glob
from dnn_model import create_model_example3
from ai_check import print_predict_result, evaluate_regression
from data_set import yahoo_reviews, tokenize_reviews

from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer

from ex_word2vec import word2vec_model
import numpy as np
from keras.models import load_model
from mecab_wakati import wakati

w2v_model = word2vec_model()

def create_sentence_vector(X, max_word_length, word_embedding_dim):
    """
    文章ベクトルを生成する
    """

    fill_vector = np.empty((0, max_word_length, word_embedding_dim))

    for words in X:
        vector = sentence_2D_vector(words, word_embedding_dim)
        vector_padding = padding_zero(vector, max_word_length, word_embedding_dim)
        vector_reshaped = vector_padding.reshape(1, max_word_length, word_embedding_dim)

        fill_vector = np.vstack((fill_vector, vector_reshaped))
    return fill_vector

def padding_zero(sentence_vector, max_sentence, word_embedding_dim):
    """
    文長の違いを吸収する。
    短い文は0ベクトルを入れ、末尾に実ベクトルを入れる。
    """
    zero_vector = np.zeros((max_sentence, word_embedding_dim))
    offset = max_sentence - sentence_vector.shape[0]
    zero_vector[offset:, :] = sentence_vector
    return zero_vector


def sentence_2D_vector(words, word_embedding_dim):
    """
    １文のベクトル表現を得る
    """
    sentence_vector = np.empty((0, word_embedding_dim)) # 50と言う数字は学習済みのword2vecが50次元でoutされているため。
    for word in words.split():
        # 単語の分散ベクトル
        try:
            word_vector = w2v_model.wv[word]
            sentence_vector = np.vstack((sentence_vector, word_vector))
        except Exception as e:
            pass

    return sentence_vector

def max_length_in_sentence_vectors(X):
    """
    最大文書長はいくつか？
    """
    sentence_vectors_length = [len(vectors.split()) for vectors in X]
    return np.max(sentence_vectors_length)

def free_input_to_vector(word):
    """
    自由入力をベクトル化する。
    """



"""
example_2で十分な性能が出なかった場合、NNを調整して精度をあげてみる
"""

word_embedding_dim = 50

X, Y = yahoo_reviews()
max_length = max_length_in_sentence_vectors(X)

X_size = len(X) # 学習データ数
max_words_count = max_length + 10 # 最大文長

X_sentence = create_sentence_vector(X, max_words_count, word_embedding_dim)

# model = create_model_example3(input_shape=(max_words_count, word_embedding_dim))
model = load_model("my_nlp_model.hdf5")

free_words = ["素晴らしいWebサイト", "人と話せて面白い", "中傷が酷い"]
free_word_vectors = create_sentence_vector(free_words, max_words_count, word_embedding_dim)
result = model.predict(free_word_vectors)

"""
実際にどういう評価となるか確かめてみる
"""
print(result)
