from functools import partial
import json

class Features:

    @staticmethod
    def __emit_word_features(rel_pos, word):
        features = {}
        for f in Features.__word_feature_functions().items():
            features.update({str(rel_pos) + ":" + f[0]: f[1](word)})
        return features

    @staticmethod
    def get_word_features(sentence,i):
        features = {}
        for x in range(i - 2, i + 3):
            if 0 <= x < len(sentence):
                features.update(Features.__emit_word_features(-(i - x), sentence[x][0]))
        if i == 0:
            features.update({'BOS' : True})
        if i == len(sentence) - 1:
            features.update({'EOS': True})
        return features

    @staticmethod
    def __word_feature_functions():
        return {
                "token.has.special.character" : Features.__has_special_character,
                "token.has.only.numbers" : Features.__only_contains_numbers,
                "token.has.some.numbers" : Features.__contains_some_numbers,
                "token.is.status" : Features.__is_status,
                "token.has.capital.letter" : Features.__has_capital_letter,
                "token.has.only.capital.letters" : Features.__has_only_capital_letters,
                "token.has.capital.letter" : Features.__has_capital_letter,
                "token.has.no.capital.letters" : Features.__has_no_captital_letters,
                "token.is.HISCO.approved" : Features.__is_listed_in_HISCO,
                "token.contains.punctuation" : Features.__contains_punctuation,
                "token.is.start" : Features.__is_start,
                "token.is.end" : Features.__is_end,   
                "token.is.seperator" : Features.__is_seperator,
                "token.last.3.characters" : partial(Features.__get_the_last_characters, 3),
                "token.last.2.characters" : partial(Features.__get_the_last_characters, 2),
                "token.last.2.characters" : partial(Features.__get_the_last_characters, 1)
        }

    @staticmethod
    def get_sentence_features(sentence):
        return [Features.get_word_features(sentence, i) for i in range(len(sentence))]

    @staticmethod
    def get_sentence_labels(sentence):
        return [label for token, label in sentence]

    @staticmethod
    def get_sentence_tokens(sentence):
        return [token for token, label in sentence]

    @staticmethod
    def __has_special_character(token):
        # List can be extended for other purposes
        special_character_list = ['*']
        return token in special_character_list
    @staticmethod
    def __only_contains_numbers(token):
         return token.isdigit()
    @staticmethod
    def __contains_some_numbers(token):
        return any(char.isdigit() for char in token)
    @staticmethod
    def __is_status(token):
        with open("cdparser/features/statuses.json", 'r') as file:
            status_map = json.load(file)
        print(token in status_map.values())
        return token in status_map.values()
    @staticmethod
    # Will be implemented at a later stage
    def __is_listed_in_HISCO(token):
        return False
    @staticmethod
    def __has_capital_letter(token):
        return any(char.isupper() for char in token)
    @staticmethod
    def __has_only_capital_letters(token):
        return token.isupper()
    @staticmethod
    def __has_no_captital_letters(token):
        return token.islower()
    @staticmethod
    def __is_start(token):
        return token == 'START'
    @staticmethod
    def __is_end(token):
        return token == 'END'
    @staticmethod
    def __is_seperator(token):
        return token == ' ' or token == ','
    @staticmethod
    def __contains_punctuation(token):
        return '.' in token
    @staticmethod
    def __get_the_last_characters(amount, token):
        return str(token)[-amount:]