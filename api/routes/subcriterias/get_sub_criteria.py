from config import Config
from api.models.sub_criteria import SubCriteria
from flask import current_app, abort
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


def get_themes_answers(theme_id: str) -> list:
    """ function takes a theme_id arg & returns a list 
    of answers for the given theme_id.
    """
    sub_criterias = get_all_subcriteria()
    return [theme['answers'] for themes in sub_criterias for theme in themes['themes'] if theme_id==theme['id']][0]
 
def replace_boolean_values(themes_answers):
    for answers in themes_answers:
        if 'answer' in answers.keys():
            if answers['answer']==False:
                answers.update(answer="No")
            if answers['answer']==True:
               answers.update(answer="Yes")

       
def get_answers_for_assessors(application_id: str, theme_id: str):
    themes_answers = get_themes_answers(theme_id)
    application_json_blob = get_application_jsonb_blob(application_id)
    
    for themes_answer in themes_answers:
        for forms in application_json_blob['jsonb_blob']['forms']:
            for questions in forms['questions']:
                if isinstance(themes_answer["field_id"], list):
                    answer_list = tuple(((app['title'],app['answer']) for app in questions['fields'] for field_id in themes_answer["field_id"] if "answer" in app.keys() and app['key']==field_id))
                    if answer_list:
                        themes_answer['answer'] = answer_list                     
                else:
                    for app_fields in questions['fields']:
                        if themes_answer["field_id"] ==  app_fields['key']:
                            themes_answer['answer'] = app_fields['answer']
                                    
    replace_boolean_values(themes_answers)    
                                                             
    return themes_answers
