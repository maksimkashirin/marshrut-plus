from sqlalchemy import select

from app.database import SessionLocal
from app.models.recommendation import Recommendation


RECOMMENDATIONS = [
    {
        "code": "adapted_program",
        "title": "Адаптированная образовательная программа",
        "description": (
            "Обучение по адаптированной образовательной программе "
            "в соответствии с рекомендациями ПМПК."
        ),
    },
    {
        "code": "speech_therapist",
        "title": "Занятия с учителем-логопедом",
        "description": (
            "Организация занятий с учителем-логопедом "
            "в соответствии с рекомендациями ПМПК."
        ),
    },
    {
        "code": "psychologist",
        "title": "Сопровождение педагога-психолога",
        "description": (
            "Психолого-педагогическое сопровождение "
            "в соответствии с рекомендациями ПМПК."
        ),
    },
    {
        "code": "special_materials",
        "title": "Специальные учебные материалы",
        "description": (
            "Использование специальных учебных или дидактических "
            "материалов, если они предусмотрены рекомендациями ПМПК."
        ),
    },
]


def seed_recommendations() -> None:
    with SessionLocal() as db:
        for item in RECOMMENDATIONS:
            recommendation = db.scalar(
                select(Recommendation).where(
                    Recommendation.code == item["code"]
                )
            )

            if recommendation is None:
                recommendation = Recommendation(**item)
                db.add(recommendation)
            else:
                recommendation.title = item["title"]
                recommendation.description = item["description"]

        db.commit()


if __name__ == "__main__":
    seed_recommendations()
    print("Recommendations seeded successfully.")