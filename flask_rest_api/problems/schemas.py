from flask_io import fields, Schema, post_dump

class ProblemSchema(Schema):
    id = fields.Integer(dump_only=True)
    question = fields.String(required=True)
    answer = fields.String(required=True)
    distraction1 = fields.String(required=False)
    distraction2 = fields.String(required=False)
    distraction3 = fields.String(required=False)
    distraction4 = fields.String(required=False)
    distraction5 = fields.String(required=False)

    @post_dump
    def make_object(self, data):
        return data

class FilterSchema(Schema):
    search = fields.String(required=False)
    sort = fields.String(required=False)
    limit = fields.Integer(required=False)
    page_start = fields.Integer(required=False)