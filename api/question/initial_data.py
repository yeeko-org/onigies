from .models import QuestionType


class InitQuestionTypes:
    """`public_name`, `default_weight`, `icon` y `color` solo se
    escriben al crear: el dashboard es dueño de los cuatro. El resto se
    re-afirma cada corrida."""

    def __init__(self):
        initial_data = [
            ('a_questions', 'Armonización e institucionalización',
             'AQuestion', 'AResponse', 5, 1, True, 'gavel', 'indigo'),
            ('reach', 'Transversalidad sectorial',
             'ReachQuestion', 'ReachResponse', 2.5, 2, False,
             'groups', 'indigo'),
            ('b_questions', 'Transversalidad orgánica',
             'BQuestion', 'BResponse', 2.5, 3, True,
             'account_tree', 'indigo'),
            ('plans', 'Planes de estudio',
             'PlanQuestion', 'PlanResponse', None, 4, False,
             'menu_book', 'deep-purple'),
            ('special', 'Pregunta especial',
             'SpecialQuestion', 'SpecialResponse', None, 5, False,
             'star', 'deep-purple'),
            ('population', 'Distribución de población',
             None, None, None, 6, False, 'diversity_3', 'deep-purple'),
        ]

        for (name, public, m_question, m_response, weight_value, order,
             required, icon, color) in initial_data:
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
                    'icon': icon,
                    'color': color,
                },
            )
