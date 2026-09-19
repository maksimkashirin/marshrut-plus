from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CaseRecommendation(Base):
    __tablename__ = "case_recommendations"

    case_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("cases.id", ondelete="CASCADE"),
        primary_key=True,
    )

    recommendation_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("recommendations.id", ondelete="CASCADE"),
        primary_key=True,
    )