from config import Config
from api.models.sub_criteria import SubCriteria
from flask import current_app, abort
import re
from .test_json_blob import test_jsonb_blob
from db.queries.assessment_records.queries import get_application_jsonb_blob

def get_all_subcriteria():
    sub_criterias = []
    for section in (
        Config.COF_R2W2_ASSESSMENT_MAPPING["scored_criteria"]
        + Config.COF_R2W2_ASSESSMENT_MAPPING["unscored_sections"]
    ):
        for sub_criteria in section["sub_criteria"]:
            sub_criterias.append(sub_criteria)
    return sub_criterias

def get_matching_sub_criteria(sub_criteria_id):
    current_app.logger.info(
        f"Finding sub criteria data in config for: {sub_criteria_id}"
    )
    sub_criterias = get_all_subcriteria()
    matching_sub_criteria = list(
        filter(
            lambda sub_criteria: sub_criteria["id"] == sub_criteria_id,
            sub_criterias,
        )
    )
    if len(matching_sub_criteria) == 1:
        return matching_sub_criteria[0]
    elif len(matching_sub_criteria) > 1:
        msg="sub_criteria: '{sub_criteria_id}' duplicated."
        current_app.logger.error(msg)
        raise ValueError(msg)
    else:
        msg = f"sub_criteria: '{sub_criteria_id}' not found."
        current_app.logger.warn(msg)
        abort(404, description=msg)


def return_subcriteria_from_config(sub_criteria_id):
    sub_criteria = get_matching_sub_criteria(sub_criteria_id)
    # TODO get actual score submitted status when score table available
    score_submitted = False

    return SubCriteria.from_filtered_dict(
        {"score_submitted": score_submitted, **sub_criteria}
    )

class SubCriteriaThemes:
    
    @classmethod
    def get_themes_answers(cls, theme_id: str) -> list[dict]:
        """ function takes a theme_id arg & returns a list 
        of answers with given theme_id.
        """
        sub_criterias = get_all_subcriteria()
        return [theme['answers'] for themes in sub_criterias for theme in themes['themes'] if theme_id==theme['id']][0]
    
    @classmethod
    def get_application_form(cls, app_json_blob):
        return [questions for forms in app_json_blob['jsonb_blob']['forms'] for questions in forms['questions'] ]
       
    
    @classmethod
    def convert_boolean_values(cls,themes_answers: list[dict]) -> list[dict]:
        """ function checks boolean values in themes_answers & replace
        boolean values to string. (False -> "No", True -> "Yes")
        Args:
            themes_answers (_type_): array of dict
        """
        for answers in themes_answers:
            if 'answer' in answers.keys():
                if answers['answer']==False:
                    answers.update(answer="No")
                if answers['answer']==True:
                   answers.update(answer="Yes")
    
    
    @classmethod
    def map_add_another_component_contents(cls, themes_answers: list[dict]) -> list[dict]:
        """ function checks for special presentation_type "heading"
        in array of themes answers, if exists, adds question-value 
        to an answer key for presentation_type "heading" theme and 
        looks for presentation_type of "description" and "amount" with
        same presentation_type "heading"s field_id, retrieve words only 
        from strings of answers for presentation_type "description" theme
        & numbers only for presentation_type "amount" theme. 

        Args:
            themes_answers (_type_): array of dict
        """
        for heading in themes_answers:
            try:
                if heading['presentation_type'] == "heading":
                    heading['answer'] = heading['question']
                    for theme in themes_answers:
                        if heading["field_id"] in theme.values() and theme['presentation_type']=="description":
                            #TODO: regex to get words only
                            # description_answer = [re.sub('[^a-zA-Z]+',' ', description) for description in theme['answer']]
                            description_answer = [description.split(":")[0] for description in theme['answer']]
                        
                            theme['answer'] = description_answer
                    
                        if heading["field_id"] in theme.values() and theme['presentation_type']=="amount":
                            #TODO: regex to get currency sign (£) & numbers only
                            # amount_answer = [re.findall(r'\d+', amount) for amount in theme['answer']]
                            amount_answer = [amount.split(":")[1] for amount in theme['answer']]
                        
                            theme['answer'] = amount_answer
                            
                        else:
                            continue    
            
            except (KeyError, IndexError):
                current_app.logger.error("Incorrect field key")
                
    @classmethod
    def get_grouped_fields_answers(cls, themes_answers: list[dict], questions: dict) -> list:
        for theme in themes_answers:
                for question in questions:
                    # condition runs when field_ids are grouped together.
                    answer_list = tuple(((app['title'],app['answer']) for app in question['fields'] for field_id in theme["field_id"] if "answer" in app.keys() and app['key']==field_id))
                    if answer_list:
                        return answer_list
                    
    @classmethod
    def get_answers_for_assessors(cls,application_id: str, theme_id: str):
        themes_answers = cls.get_themes_answers(theme_id)
        application_json_blob = get_application_jsonb_blob(application_id)
        questions = cls.get_application_form(application_json_blob)
        
        for theme in themes_answers:
            if isinstance(theme["field_id"], list):
                answer_list = cls.get_grouped_fields_answers(themes_answers, questions)
                theme['answer'] = answer_list                       
            else:
                    for question in questions:
                        for app_fields in question['fields']:
                            if theme["field_id"] ==  app_fields['key']:
                                theme['answer'] = app_fields['answer']
                                                
        cls.convert_boolean_values(themes_answers)  
        cls.map_add_another_component_contents(themes_answers)                                    
        return themes_answers

   