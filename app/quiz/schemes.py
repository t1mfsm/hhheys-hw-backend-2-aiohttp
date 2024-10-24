from dataclasses import field

from marshmallow import Schema, fields


class ThemeSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)


class AnswerSchema(Schema):
    pass


class QuestionSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.List(required=True, cls_or_instance=fields.Dict)


class ThemeListSchema(Schema):
    pass


class ThemeIdSchema(Schema):
    pass


class ListQuestionSchema(Schema):
    pass
