import logging

from chatterbot import ChatBot, utils
from chatterbot.trainers import Trainer
from chatterbot.conversation import Statement

from django.conf import settings

logger = logging.getLogger(__name__)


def train_file(file_name, file):
    chatbot = ChatBot(**settings.CHATTERBOT)
    trainer = ChatTrainer(chatbot)
    statements = file.readlines()

    logger.info('training file = "%s"', file_name)
    logger.debug('training lines = %s', statements)
    trainer.train(statements)
    logger.info('training complete')


class ChatTrainer(Trainer):

    def train(self, conversation):
        previous_statement_text = None
        previous_statement_search_text = ''

        statements_to_create = []

        for conversation_count, text in enumerate(conversation):
            if self.show_training_progress:
                utils.print_progress_bar(
                    'List Trainer',
                    conversation_count + 1, len(conversation)
                )

            if conversation_count % 2:
                persona = 'client:ChatTrainer'
            else:
                persona = 'bot:ChatTrainer'

            statement_search_text = self.chatbot.storage.tagger.get_bigram_pair_string(text)

            statement = self.get_preprocessed_statement(
                Statement(
                    text=text,
                    search_text=statement_search_text,
                    in_response_to=previous_statement_text,
                    search_in_response_to=previous_statement_search_text,
                    conversation='training',
                    persona=persona
                )
            )

            previous_statement_text = statement.text
            previous_statement_search_text = statement_search_text

            statements_to_create.append(statement)

        self.chatbot.storage.create_many(statements_to_create)
