from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.route_step import RouteStep
from app.models.source import Source


KHABAROVSK_SOURCE = {
    "region": "Хабаровский край",
    "title": "Что делать после ПМПК: пошаговый план для родителей",
    "url": "https://cpmpk-khv.ru/chto-delat-posle-pmpk-poshagovyj-plan-dlya-roditelej/",
}


KHABAROVSK_BASE_ROUTE = [
    {
        "step_code": "save_copy",
        "title": "Сохранить копию заключения ПМПК",
        "description": (
            "Сохраните копию заключения ПМПК до передачи "
            "документов в образовательную организацию."
        ),
    },
    {
        "step_code": "prepare_documents",
        "title": "Подготовить документы",
        "description": (
            "Подготовьте заключение ПМПК и документы, "
            "необходимые для обращения в образовательную организацию."
        ),
    },
    {
        "step_code": "submit_conclusion",
        "title": "Передать заключение образовательной организации",
        "description": (
            "Передайте заключение ПМПК в школу, детский сад "
            "или другую образовательную организацию."
        ),
    },
    {
        "step_code": "submit_application",
        "title": "Подать заявление",
        "description": (
            "Подайте заявление о создании условий "
            "в соответствии с рекомендациями ПМПК."
        ),
    },
    {
        "step_code": "confirm_registration",
        "title": "Получить подтверждение приёма документов",
        "description": (
            "Убедитесь, что заявление и заключение приняты "
            "образовательной организацией."
        ),
    },
    {
        "step_code": "get_support_plan",
        "title": "Узнать план реализации рекомендаций",
        "description": (
            "Уточните, как образовательная организация "
            "планирует реализовать рекомендации ПМПК."
        ),
    },
]


RECOMMENDATION_STEPS = {
    "adapted_program": {
        "step_code": "clarify_adapted_program",
        "title": "Уточнить организацию обучения по адаптированной программе",
        "description": (
            "Уточните в образовательной организации, "
            "как будет организовано обучение по рекомендованной программе."
        ),
    },

    "speech_therapist": {
        "step_code": "clarify_speech_therapist",
        "title": "Уточнить организацию занятий с учителем-логопедом",
        "description": (
            "Уточните расписание и порядок организации занятий "
            "с учителем-логопедом."
        ),
    },

    "psychologist": {
        "step_code": "clarify_psychologist",
        "title": "Уточнить сопровождение педагога-психолога",
        "description": (
            "Уточните, как будет организовано сопровождение "
            "педагога-психолога."
        ),
    },

    "special_materials": {
        "step_code": "clarify_special_materials",
        "title": "Уточнить обеспечение специальными учебными материалами",
        "description": (
            "Уточните, какие специальные учебные или дидактические "
            "материалы будут использоваться."
        ),
    },
}


def get_or_create_khabarovsk_source(
    db: Session,
) -> Source:
    source = db.scalar(
        select(Source).where(
            Source.url == KHABAROVSK_SOURCE["url"]
        )
    )

    if source is not None:
        return source

    source = Source(
        region=KHABAROVSK_SOURCE["region"],
        title=KHABAROVSK_SOURCE["title"],
        url=KHABAROVSK_SOURCE["url"],
    )

    db.add(source)
    db.flush()

    return source


def create_route_for_case(
    db: Session,
    case_id: int,
    region: str,
    recommendation_codes: list[str] | None = None,
) -> list[RouteStep]:

    if region != "Хабаровский край":
        raise ValueError(
            f"Route configuration for region '{region}' is not available"
        )

    source = get_or_create_khabarovsk_source(db)

    route_templates = list(KHABAROVSK_BASE_ROUTE)

    selected_codes = set(
        recommendation_codes or []
    )

    for code, template in RECOMMENDATION_STEPS.items():
        if code in selected_codes:
            route_templates.append(template)

    steps = []

    for index, template in enumerate(
        route_templates,
        start=1,
    ):
        step = RouteStep(
            case_id=case_id,
            source_id=source.id,
            step_code=template["step_code"],
            title=template["title"],
            description=template["description"],
            order_number=index,
            status="pending",
        )

        db.add(step)
        steps.append(step)

    return steps