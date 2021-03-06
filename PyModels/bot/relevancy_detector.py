# -*- coding: utf-8 -*-

from model_applicator import ModelApplicator


class RelevancyDetector(ModelApplicator):
    """
    Класс предназначен для скрытия деталей вычисления релевантности
    предпосылок и вопроса.
    """
    def __init__(self):
        pass

    def get_most_relevant(self, probe_phrase, phrases, text_utils, word_embeddings, nb_results=1):
        raise NotImplemented()

    def calc_relevancy1(self, premise, question, text_utils, word_embeddings):
        raise NotImplemented()

    def get_w2v_path(self):
        return None
