from chatterbot.logic import BestMatch
from chatterbot.conversation import Statement


class ChatAdapter(BestMatch):

    def process(self, input_statement, additional_response_selection_parameters):
        # get the previous statement
        previous_id = additional_response_selection_parameters.pop('previous', None)
        try:
            previous = next(self.chatbot.storage.filter(pk=previous_id))
            search_parameters = {

            }
        except StopIteration:
            previous = None
            search_parameters = {
                'tags': ['start']
            }

        # Search for the closest match to the input statement
        search_results = self.search_algorithm.search(input_statement, **search_parameters)
        closest_match = None

        for result in search_results:
            if result.confidence >= self.maximum_similarity_threshold:
                closest_match = result
                break

        # check if any match to the input statement was found
        if not closest_match:
            self.chatbot.logger.info(
                'Could not find statement for input statement "{}" with enough confidence.'.format(
                    input_statement.text
                )
            )
            return self.get_unsure_response()
        else:
            self.chatbot.logger.info('Using "{}" as a close match to "{}" with a confidence of {}'.format(
                closest_match.text, input_statement.text, closest_match.confidence
            ))

        response_selection_parameters = {
            'search_in_response_to': closest_match.search_text
        }

        if additional_response_selection_parameters:
            response_selection_parameters.update(additional_response_selection_parameters)

        # Get all statements that are in response to the closest match
        response_list = list(self.chatbot.storage.filter(**response_selection_parameters))

        # check if any response was found
        if not response_list:
            self.chatbot.logger.info('No responses found.')
            return self.get_no_response()

        self.chatbot.logger.info(
            'Selecting response from {} optimal responses.'.format(
                len(response_list)
            )
        )

        response = self.select_response(
            input_statement,
            response_list,
            self.chatbot.storage
        )

        response.confidence = closest_match.confidence

        self.chatbot.logger.info('Response selected. Using "{}"'.format(response.text))

        return response

    def get_unsure_response(self):
        return Statement(
            id=None,
            text='Sorry, I\'m not sure what that means.'
        )

    def get_no_response(self):
        return Statement(
            id=None,
            text='Sorry, I have no answer to this.'
        )
