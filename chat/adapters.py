from chatterbot.storage.django_storage import DjangoStorageAdapter

from chatterbot.logic import BestMatch


class CustomAdapter(BestMatch):

    def can_process(self, statement):
        return True

    def process(self, 
                input_statement, 
                additional_parameters):

        Statement = DjangoStorageAdapter().get_statement_model()
        in_response_to = additional_parameters['in_response_to']
        in_response_to_models = Statement.objects.filter(text=in_response_to).values_list(flat=True)
        possible_answers = Statement.objects.filter(in_response_to=input_statement.text)        

        res = possible_answers.exclude(id__in=list(in_response_to_models)).first()
                         
        if res:
            res.confidence = 1
            return res
        else:
            return super().process(input_statement, 
                additional_response_selection_parameters)            

        
