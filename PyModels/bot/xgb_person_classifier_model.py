# -*- coding: utf-8 -*-

import os
import json
import logging
import xgboost
from scipy.sparse import lil_matrix

from person_classifier_model import PersonClassifierModel


class XGB_PersonClassifierModel(PersonClassifierModel):
    def __init__(self):
        super(XGB_PersonClassifierModel, self).__init__()
        self.logger = logging.getLogger('XGB_PersonClassifierModel')

    def load(self, models_folder):
        self.logger.info('Loading XGB_PersonClassifierModel model files')

        with open(os.path.join(models_folder, 'xgb_person_classifier.config'), 'r') as f:
            model_config = json.load(f)

        self.xgb_person_classifier_shingle_len = model_config['shingle_len']
        self.xgb_person_classifier_shingle2id = model_config['shingle2id']
        self.xgb_person_classifier_nb_features = model_config['nb_features']
        self.xgb_person_classifier = xgboost.Booster()
        self.xgb_person_classifier.load_model(self.get_model_filepath(models_folder, model_config['model_filename']))

    def detect_person(self, sentence_str, text_utils, word_embeddings):
        words = text_utils.tokenize(sentence_str)

        # Ищем глагол в личной форме по результатам частеречной разметки
        tags = text_utils.tag(words)
        verb_person = None
        for tag in tags:
            if tag[1].startswith('VERB'):
                tx = tag[1].split('|')
                num = ''
                if 'Number=Sing' in tx:
                    num = 's'
                elif 'Number=Plur' in tx:
                    num = 'p'

                if 'Person=1' in tx:
                    verb_person = '1'+num
                    break
                elif 'Person=2' in tx:
                    verb_person = '2'+num
                    break
                elif 'Person=3' in tx:
                    verb_person = '3'+num
                    break

        if verb_person:
            return verb_person

        wx = text_utils.words2str(words)
        shingles = text_utils.ngrams(wx, self.xgb_person_classifier_shingle_len)
        X_data = lil_matrix((1, self.xgb_person_classifier_nb_features), dtype='bool')
        for shingle in shingles:
            if shingle in self.xgb_person_classifier_shingle2id:
                X_data[0, self.xgb_person_classifier_shingle2id[shingle]] = True
        D_data = xgboost.DMatrix(X_data)
        y = self.xgb_person_classifier.predict(D_data)
        person = ['1s', '2s', '3'][int(y[0])]
        return person
