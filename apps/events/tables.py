import django_tables as tables
from django.utils.datastructures import SortedDict
from django.utils import simplejson

def create_answer_table(jquestions):
    """
    Create answer table class
    """
    columns = SortedDict()    
    columns['member'] = tables.Column(verbose_name="Member")
    
    if jquestions != "":    
        questions = simplejson.loads(jquestions)
        
        for i, question in enumerate(questions):
            columns['question'+ str(i)] = tables.Column(verbose_name=question['title'])
    
    table = type('AnswerTable', (tables.MemoryTable,), columns)
    return table

