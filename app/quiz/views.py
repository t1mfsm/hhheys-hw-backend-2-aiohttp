from aiohttp_apispec import request_schema, response_schema, docs, querystring_schema

from app.quiz.models import Question
from app.quiz.schemes import ThemeSchema, QuestionSchema, ListQuestionSchema
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.schemes import OkResponseSchema
from app.web.utils import json_response

from aiohttp.web_exceptions import HTTPConflict, HTTPBadRequest, HTTPNotFound


class ThemeAddView(View, AuthRequiredMixin):

    @request_schema(ThemeSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        await self.check_auth(self.request)
        data = await self.request.json()
        title = data["title"]
        if await self.request.app.store.quizzes.get_theme_by_title(title) is not None:
            raise HTTPConflict
        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(View, AuthRequiredMixin):
    async def get(self):
        await self.check_auth(self.request)
        raw_data = await self.request.app.store.quizzes.list_themes()
        data = []
        for theme in raw_data:
            data.append({
                "id":theme.id,
                "title":theme.title
            })
        return json_response(data={"themes":data})


class QuestionAddView(View, AuthRequiredMixin):
    @request_schema(QuestionSchema)
    @response_schema(OkResponseSchema)
    async def post(self):
        await self.check_auth(self.request)
        data = await self.request.json()
        correct_ans = 0
        for answers in data["answers"]:
            if answers["is_correct"]:
                correct_ans += 1
        if correct_ans != 1 or len(data["answers"]) < 2:
            raise HTTPBadRequest

        if await self.request.app.store.quizzes.get_theme_by_id(data["theme_id"]) is None:
            raise HTTPNotFound

        if await self.request.app.store.quizzes.get_question_by_title(data["title"]) is not None:
            raise HTTPConflict

        question = await self.request.app.store.quizzes.create_question(title=data["title"], theme_id=data["theme_id"], answers=data["answers"])

        return json_response(data={
                      "id": question.id,
                      "title": question.title,
                      "theme_id": question.theme_id,
                      "answers": question.answers
                    })

# @querystring_schema(ListQuestionSchema)
@response_schema(OkResponseSchema,200)
class QuestionListView(View, AuthRequiredMixin):
    async def get(self):
        await self.check_auth(self.request)
        if self.request.query.get('theme_id') is not None:
            if await self.request.app.store.quizzes.get_theme_by_id(int(self.request.query['theme_id'])) is None:
                raise HTTPNotFound
            raw_data = await self.request.app.store.quizzes.list_questions(int(self.request.query['theme_id']))
            data = []
            for question in raw_data:
                data.append({
                          "id": question.id,
                          "title": question.title,
                          "theme_id": question.theme_id,
                          "answers": question.answers
                })
            return json_response(data={"questions": data})
        else:
            data = []
            return json_response(data={"questions": data})
