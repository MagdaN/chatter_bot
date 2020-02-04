import logging

from django.conf import settings
from django.contrib.postgres.search import TrigramSimilarity

logger = logging.getLogger(__name__)


class LogicAdapte():

    def process(self, request, responses):
        raise NotImplementedError


class LevenshteinDistance():

    def process(self, request, statements):
        from Levenshtein import ratio

        best_similarity = settings.LOGIC_THRESHOLD
        best_statement = None
        for statement in statements:
            similarity = ratio(request, statement.request)

            if similarity > best_similarity:
                best_similarity = similarity
                best_statement = statement

        return best_statement, best_similarity

class NaturalLanguageProcessor():

    def get_lem_tokens(self, tokens):
        from nltk.stem import WordNetLemmatizer
        lemmer = WordNetLemmatizer()
        return [lemmer.lemmatize(token) for token in tokens]

    def normalize_lem(self,text):
        import nltk
        import string
        remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
        return self.get_lem_tokens(
            nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

    def process(self, request, statements):
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        request_tokens = list(statements.values_list('request', flat=True))
        request_tokens.append(request)
        TfidfVec = TfidfVectorizer(tokenizer=self.normalize_lem, stop_words='english')
        tfidf = TfidfVec.fit_transform(request_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        return statements.get(request=request_tokens[idx]), req_tfidf


class PostgresTrigramSimilarity():

    def process(self, request, statements):
        ordered_responses = statements.annotate(similarity=TrigramSimilarity('request', request)) \
                                      .filter(similarity__gt=settings.LOGIC_THRESHOLD) \
                                      .order_by('-similarity')

        if ordered_responses:
            response = ordered_responses.first()
            return response, response.similarity
        else:
            return None
