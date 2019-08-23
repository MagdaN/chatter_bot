import logging

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

from django.conf import settings

logger = logging.getLogger(__name__)


def train_file(file_name, file):
    chatbot = ChatBot(**settings.CHATTERBOT)
    trainer = ListTrainer(chatbot)

    logger.info('Train using TrainingFile "%s"', file_name)
    trainer.train(file.readlines())
    logger.info('Training complete')


def train_corpus(corpus_name):
    chatbot = ChatBot(**settings.CHATTERBOT)
    trainer = ChatterBotCorpusTrainer(chatbot)

    logger.info('Train using corpus "%s"', corpus_name)
    trainer.train(corpus_name)
    logger.info('Training complete')
