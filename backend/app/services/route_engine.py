from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.route_step import RouteStep
from app.models.source import Source


KHABAROVSK_SOURCE = {
    "region": "Хабаровский край",
    "title": "Что делать после ПМПК: пошаговый план для родителей",
    "url": "https://cpmpk-khv.ru/chto-delat-posle-pmpk-poshagovyj-plan-dlya-roditelej/",
}


KHABAROVSK_ROUTE = [
    {
        "step_code": "save_copy",
        "title": "Сохранить копию заключения ПМПК",
        "description": (
            "Сохраните копию заключения ПМПК до передачи "
            "оригинала в образовательную организацию."
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
            "Передайте заключение ПМПК в школу или другую "
            "образовательную организацию."
        ),
    },
    {
        "step_code": "submit_application",
        "title": "Подать заявление",
        "description": (
            "Подайте заявление о создании рекомендованных "
            "специальных образовательных условий."
        ),
    },
    {
        "step_code": "confirm_registration",
        "title": "Получить подтверждение приёма документов",
        "description": (
            "Убедитесь, что заявление и заключение приняты "
            "и зарегистрированы образовательной организацией."
        ),
    },
    {
        "step_code": "get_support_plan",
        "title": "Получить информацию о плане сопровождения",
        "description": (
            "Уточните, как образовательная организация планирует "
            "реализовать рекомендации ПМПК."
        ),
    },
    {
        "step_code": "clarify_conditions",
        "title": "Уточнить организацию рекомендованных условий",
        "description": (
            "Уточните программу, специалистов, занятия и другие "
            "предусмотренные условия сопровождения."
        ),
    },
]


def get_or_create_khabarovsk_source(db: Session) -> Source:
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
) -> list[RouteStep]:
    if region != "Хабаровский край":
        raise ValueError(
            f"Route configuration for region '{region}' is not available"
        )

    source = get_or_create_khabarovsk_source(db)

    steps = []

    for index, template in enumerate(
        KHABAROVSK_ROUTE,
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