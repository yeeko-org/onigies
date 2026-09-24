from .models import QuestionType


class InitQuestionTypes:
    """`public_name`, `default_weight`, `icon`, `color` y `description`
    solo se escriben al crear: el dashboard es dueño de los cinco. El
    resto se re-afirma cada corrida."""

    def __init__(self):
        initial_data = [
            ('a_questions', 'Armonización e institucionalización',
             'AQuestion', 'AResponse', 5, 1, True, 'gavel', 'indigo',
             'Normas, instancias y procedimientos con los que la '
             'institución formaliza la medida.'),
            ('reach', 'Transversalidad sectorial',
             'ReachQuestion', 'ReachResponse', 2.5, 2, False,
             'groups', 'indigo',
             'A qué poblaciones de la comunidad alcanza la medida.'),
            ('b_questions', 'Transversalidad orgánica',
             'BQuestion', 'BResponse', 2.5, 3, True,
             'account_tree', 'indigo',
             'En cuántas de sus instancias académicas y administrativas '
             'opera la medida.'),
            ('plans', 'Planes de estudio',
             'PlanQuestion', 'PlanResponse', None, 4, False,
             'menu_book', 'deep-purple',
             'Cuántos planes de estudio, por nivel, incorporan la '
             'medida.'),
            ('special', 'Pregunta especial',
             'SpecialQuestion', 'SpecialResponse', None, 5, False,
             'star', 'deep-purple',
             'Dato propio de este observable que no cabe en los demás '
             'grupos.'),
            ('population', 'Distribución de población',
             None, None, None, 6, False, 'diversity_3', 'deep-purple',
             'Composición sexo-género capturada en Información base y '
             'calificada aquí.'),
        ]

        for (name, public, m_question, m_response, weight_value, order,
             required, icon, color, description) in initial_data:
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
                    'description': description,
                },
            )
