"""The whole questionnaire as a .docx, read from the DB.

A reference document, not a fillable form: answer controls of the
maquetado (dropdowns, blanks for counts) are left out on purpose.
"""
from collections.abc import Iterator
from io import BytesIO

from django.db.models import Prefetch, QuerySet

from indicator.models import Axis, Component, GeneralGroup, Observable, Sector
from question.models import (
    BQuestion, GeneralQuestion, QuestionType, ReachQuestion, SpecialQuestion)

from . import texts
from .writer import DocxWriter

POPULATION_TYPE = 'population'
A_TYPE = 'a_questions'
B_TYPE = 'b_questions'

# Groups whose body is a Sector checklist instead of GeneralQuestion
# rows; mirrors GROUP_COMPONENTS of the dashboard's GeneralGroupPanel.
POPULATIONS_GROUP = 'poblaciones'
AUTHORITIES_GROUP = 'autoridades'
# The dashboard places this group's instruction after the head's radio.
OWN_INSTRUCTION_GROUPS = (AUTHORITIES_GROUP,)


def build_questionnaire_docx() -> BytesIO:
    """Returns a BytesIO positioned at 0 with the .docx content."""
    return QuestionnaireDocx().build()


def sector_label(sector: Sector) -> str:
    if not sector.description:
        return sector.name
    # Only the initial is lowered: descriptions carry acronyms («IES»).
    description = sector.description[0].lower() + sector.description[1:]
    return texts.SECTOR_WITH_DESCRIPTION.format(
        name=sector.name, description=description)


def join_names(names: list[str]) -> str:
    if len(names) < 2:
        return ''.join(names)
    return ', '.join(names[:-1]) + texts.GROUP_JOIN + names[-1]


class QuestionnaireDocx:

    def __init__(self) -> None:
        self.writer = DocxWriter()
        self.sectors = list(Sector.objects.all())
        self.main_sectors = [s for s in self.sectors if s.is_main]
        self.axes = list(Axis.objects.prefetch_related(Prefetch(
            'component_set', queryset=Component.objects.order_by('pk')
            .prefetch_related(Prefetch(
                'observables', queryset=self._observables())))))
        self.population_numbers = [
            observable.number
            for observable in self._all_observables()
            if self._has_population_type(observable)]
        self.groups = list(GeneralGroup.objects.prefetch_related(Prefetch(
            'questions', queryset=GeneralQuestion.objects.order_by('order'))))
        type_names = dict(QuestionType.objects.filter(
            name__in=(A_TYPE, B_TYPE)).values_list('name', 'public_name'))
        self.variable_a_label = (
            texts.VARIABLE_A_PREFIX + type_names.get(A_TYPE, ''))
        self.variable_b_label = (
            texts.VARIABLE_B_PREFIX + type_names.get(B_TYPE, ''))

    def build(self) -> BytesIO:
        self.writer.document.core_properties.title = texts.DOCUMENT_TITLE
        self.write_toc()
        self.write_base_info()
        self.write_checklist()
        self.write_questionnaire()
        return self.writer.save()

    # --- Sections ---------------------------------------------------------

    def write_toc(self) -> None:
        w = self.writer
        w.paragraph(texts.TOC_TITLE, 'TOC Title', page_break_before=True)
        w.toc(texts.TOC_PLACEHOLDER)

    def write_base_info(self) -> None:
        w = self.writer
        w.heading(texts.BASE_INFO_TITLE, 1)
        w.logo()
        for index, group in enumerate(self.groups):
            w.heading(
                group.title or group.public_name, 3,
                page_break_before=index == 0)
            self.write_general_group(group)

    def write_general_group(self, group: GeneralGroup) -> None:
        w = self.writer
        if group.subtitle:
            w.paragraph(group.subtitle)
        own_instruction = group.name in OWN_INSTRUCTION_GROUPS
        if group.instruction and not own_instruction:
            w.paragraph(group.instruction)
        # The instruction describes the population list, so the list goes
        # right under it and the group's own questions after.
        if group.name == POPULATIONS_GROUP:
            w.bullets(self.population_labels())
        elif group.name == AUTHORITIES_GROUP:
            self.write_authorities(group)
        for question in group.questions.all():
            self.write_general_question(question)
        if group.is_population and self.population_numbers:
            w.paragraph(
                texts.BASE_INFO_OBSERVABLE_NOTE.format(
                    numbers=', '.join(self.population_numbers)),
                'Cross Reference')

    def write_general_question(self, question: GeneralQuestion) -> None:
        w = self.writer
        if question.q_type != 'boolean':
            w.bullets([question.text])
            return
        w.paragraph(question.text, 'Question')
        options = question.addl_config.get('options')
        if not options:
            w.lettered(texts.YES_NO_OPTIONS)
            return
        w.lettered([
            texts.GENERAL_OPTION.format(**option)
            if option.get('description') else option['name']
            for option in options])

    def population_labels(self) -> list[str]:
        labels = [sector_label(s) for s in self.main_sectors]
        labels += [
            texts.POPULATION_PRESENCE_ONLY.format(name=sector_label(s))
            for s in self.sectors if s.is_standard_extra]
        return labels

    def write_authorities(self, group: GeneralGroup) -> None:
        w = self.writer
        authorities = [s for s in self.sectors if s.is_authority]
        head = next((s for s in authorities if s.is_ies_head), None)
        if head:
            w.paragraph(
                texts.IES_HEAD_LABEL.format(name=head.name), 'Question')
            w.lettered(texts.IES_HEAD_OPTIONS)
        if group.instruction:
            w.paragraph(group.instruction, 'Question Label')
        w.bullets([
            sector_label(s) for s in authorities if not s.is_ies_head])

    def write_checklist(self) -> None:
        w = self.writer
        w.heading(texts.CHECKLIST_TITLE, 1)
        w.logo()
        w.paragraph(texts.CHECKLIST_INSTRUCTION, page_break_before=True)
        for axis in self.axes:
            rows = [
                texts.CHECKLIST_ROW.format(
                    number=observable.number, name=observable.name)
                for component in axis.component_set.all()
                for observable in component.observables.all()]
            w.checklist_table(axis.name, rows)
            w.paragraph()

    def write_questionnaire(self) -> None:
        w = self.writer
        w.heading(texts.QUESTIONNAIRE_TITLE, 1)
        w.logo()
        for axis in self.axes:
            w.heading(
                texts.AXIS_HEADING.format(number=axis.order, name=axis.name),
                2)
            if axis.description:
                w.paragraph(axis.description, 'Axis Description')
            w.logo()
            for component in axis.component_set.all():
                w.heading(
                    texts.COMPONENT_HEADING.format(name=component.name), 3,
                    page_break_before=True)
                for index, observable in enumerate(
                        component.observables.all()):
                    self.write_observable(observable, first=index == 0)

    # --- Observable -------------------------------------------------------

    def write_observable(self, observable: Observable, first: bool) -> None:
        w = self.writer
        w.heading(
            texts.OBSERVABLE_HEADING.format(
                number=observable.number, name=observable.name),
            4, page_break_before=not first)
        w.paragraph(texts.INIT_QUESTION_LABEL, 'Question Label')
        w.paragraph(
            texts.INIT_QUESTION.format(
                order=observable.order, text=observable.init_question or ''),
            'Question')
        if observable.note:
            w.note(texts.OBSERVABLE_NOTE_LABEL + observable.note)
        w.lettered([texts.INIT_ANSWER_NO, texts.INIT_ANSWER_YES])
        self.write_a_block(observable)
        w.paragraph(self.variable_b_label, 'Question Label')
        for reach in observable.reachquestion_set.all():
            w.paragraph(reach.text, 'Question')
            w.bullets(self.reach_labels(reach))
        for b_question in observable.bquestion_set.all():
            w.paragraph(b_question.text, 'Question')
            w.lines(self.instance_lines(b_question))
        for plan in observable.planquestion_set.all():
            w.paragraph(plan.text, 'Question')
        for special in observable.specialquestion_set.all():
            w.paragraph(special.text, 'Question')
        if self._has_population_type(observable):
            w.paragraph(self.population_note(), 'Cross Reference')

    def write_a_block(self, observable: Observable) -> None:
        w = self.writer
        w.paragraph(self.variable_a_label, 'Question Label')
        if observable.a_main_question:
            w.paragraph(observable.a_main_question, 'Question')
        if observable.a_main_subtitle:
            w.paragraph(observable.a_main_subtitle, 'Question Hint')
        options = [a.text for a in observable.aquestion_set.all()]
        if options:
            w.option_table(options)

    def reach_labels(self, reach: ReachQuestion) -> list[str]:
        sectors = list(self.main_sectors) if reach.has_main_sectors else []
        sectors += [
            s for s in reach.others_sectors.all() if s not in sectors]
        labels = [sector_label(s) for s in sectors]
        if reach.has_general_planning:
            labels.append(texts.GENERAL_PLANNING_OPTION)
        return labels

    @staticmethod
    def instance_lines(b_question: BQuestion) -> list[str]:
        lines = []
        if b_question.includes_academic:
            lines.append(texts.ACADEMIC_INSTANCES)
        if b_question.includes_admin:
            lines.append(texts.ADMIN_INSTANCES)
        return lines

    def population_note(self) -> str:
        titles = [
            texts.GROUP_NAME.format(title=group.title or group.public_name)
            for group in self.groups if group.is_population]
        return texts.POPULATION_OBSERVABLE_NOTE.format(
            groups=join_names(titles),
            section=texts.BASE_INFO_TITLE)

    # --- Data -------------------------------------------------------------

    @staticmethod
    def _observables() -> QuerySet[Observable]:
        return Observable.objects.order_by('order').prefetch_related(
            'aquestion_set', 'planquestion_set', 'type_weights',
            Prefetch(
                'bquestion_set',
                queryset=BQuestion.objects.order_by('order', 'pk')),
            Prefetch(
                'reachquestion_set',
                queryset=ReachQuestion.objects.order_by('pk')
                .prefetch_related('others_sectors')),
            Prefetch(
                'specialquestion_set',
                queryset=SpecialQuestion.objects.order_by('pk')))

    def _all_observables(self) -> Iterator[Observable]:
        for axis in self.axes:
            for component in axis.component_set.all():
                yield from component.observables.all()

    @staticmethod
    def _has_population_type(observable: Observable) -> bool:
        return any(
            row.question_type_id == POPULATION_TYPE
            for row in observable.type_weights.all())
