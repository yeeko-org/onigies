from .models import QuestionType


class InitQuestionTypes:
    """`public_name` y `default_weight` solo se escriben al crear: el
    dashboard es dueño de ambos. El resto se re-afirma cada corrida."""

    def __init__(self):
        initial_data = [
            ('a_questions', 'Armonización e institucionalización',
             'AQuestion', 'AResponse', 60, 1, True),
            ('reach', 'Transversalidad sectorial',
             'ReachQuestion', 'ReachResponse', 0, 2, False),
            ('b_questions', 'Transversalidad orgánica',
             'BQuestion', 'BResponse', 40, 3, True),
            ('plans', 'Planes de estudio',
             'PlanQuestion', 'PlanResponse', 0, 4, False),
            ('special', 'Pregunta especial',
             'SpecialQuestion', 'SpecialResponse', 0, 5, False),
            ('population', 'Distribución de población',
             None, None, 0, 6, False),
        ]

        for (name, public, m_question, m_response, weight_value, order,
             required) in initial_data:
            structure = {
                'model_question': m_question,
                'model_response': m_response,
                'order': order,
                'required': required,
            }
            QuestionType.objects.update_or_create(
                name=name,
                defaults=structure,
                create_defaults={
                    **structure,
                    'public_name': public,
                    'default_weight': weight_value,
                },
            )
