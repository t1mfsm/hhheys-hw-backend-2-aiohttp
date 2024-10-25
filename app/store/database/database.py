from dataclasses import dataclass, field

from app.admin.models import Admin
from app.quiz.models import Theme, Question
from app.web.config import BotConfig


@dataclass
class Database:
    # TODO: добавить поля admins и questions
    themes: list[Theme] = field(default_factory=list)
    admins: list[Admin] = field(default_factory=list)
    questions: list[Question] = field(default_factory=list)
    bot: BotConfig = field(default_factory=BotConfig)

    @property
    def next_theme_id(self) -> int:
        return len(self.themes) + 1

    @property
    def next_admin_id(self) -> int:
        return len(self.admins) + 1

    @property
    def next_question_id(self) -> int:
        return len(self.questions) + 1

    def clear(self):
        self.themes = []
        self.questions = []
        self.admins = []
