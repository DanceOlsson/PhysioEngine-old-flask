from app.questionnaires_config import QUESTIONNAIRES

def calculate_koos_scores(responses):
    config = QUESTIONNAIRES['koos']
    subscale_scores = {}

    for section, questions in config['sections'].items():
        valid_responses = [responses.get(q, 0) for q in questions if q in responses]
        if valid_responses:
            subscale_scores[section] = 100 - (sum(valid_responses) * 100 / (4 * len(valid_responses)))

    if not subscale_scores:
        return {
            'questionnaire_name': config['name'],
            'sections': [],
            'total_score': 0,
            'interpretation': 'No valid responses received'
        }

    total_score = sum(subscale_scores.values()) / len(subscale_scores)
    
    interpretation = next((desc for range, desc in config['interpretation'].items() if range[0] <= total_score <= range[1]), 'Unable to interpret')

    return {
        'questionnaire_name': config['name'],
        'sections': [
            {'name': section, 'score': score, 'interpretation': get_interpretation(score)}
            for section, score in subscale_scores.items()
        ],
        'total_score': total_score,
        'interpretation': interpretation
    }

def get_interpretation(score):
    config = QUESTIONNAIRES['koos']
    return next((desc for range, desc in config['interpretation'].items() if range[0] <= score <= range[1]), 'Unable to interpret')
