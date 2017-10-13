from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_io import fields
from sqlalchemy import func
from sqlalchemy_utils.functions import sort_query
from .models import Problem
from .schemas import ProblemSchema, FilterSchema
from .. import db, io
from flask_cors import cross_origin

app = Blueprint('problems', __name__, url_prefix='/v1/problems')


@app.route('/', methods=['POST'])
@io.from_body('problem', ProblemSchema)
def add_problem(problem):
    p = Problem(**problem)
    db.session.add(p)
    db.session.commit()

    problem['id'] = p.id

    return jsonify(problem)


@app.route('/<int:id>', methods=['GET'])
@io.marshal_with(ProblemSchema)
def get_problem(id):
    problem = Problem.query.filter_by(id=id).first()

    if not problem:
        return io.not_found('Problem not found: ' + str(id))

    return problem


@app.route('/filter', methods=['POST'])
@io.from_body('filter', FilterSchema)
@io.marshal_with(ProblemSchema)
def list_companies(filter):
    query = Problem.query

    if 'search' in filter and filter['search'] != '':
        query = query.filter(Problem.question.contains(filter['search']))

    if 'sort' in filter:
        if filter['sort'].lower() == 'asc':
            query = query.order_by(Problem.question.asc())
        elif filter['sort'].lower() == 'desc':
            query = query.order_by(Problem.question.desc())

    if 'page_start' in filter:
        query = query.offset(filter['page_start'])

    limit = 10
    if 'limit' in filter:
        limit = filter['limit']
    query = query.limit(limit)

    # for i in query.all():
    #     print (i.question)

    return query.all()


@app.route('/<int:id>', methods=['DELETE'])
def delete_problem(id):
    problem = Problem.query.filter_by(id=id).first()

    if not problem:
        return io.not_found('Problem not found: ' + str(id))

    db.session.delete(problem)
    db.session.commit()

    return io.no_content()  # this is optional


@app.route('/<int:id>', methods=['PUT'])
@io.from_body('problem', ProblemSchema)
def put_problem(id, problem):
    problem_old = Problem.query.filter_by(id=id).first()

    if not problem_old:
        return io.not_found('Problem not found: ' + str(id))

    db.session.delete(problem_old)

    problem['id'] = id
    p = Problem(**problem)
    db.session.add(p)
    db.session.commit()

    return problem


@app.route('/<int:id>/solve/<string:answer>', methods=['GET'])
def solve(id, answer):
    problem = Problem.query.filter_by(id=id).first()

    if not problem:
        return io.not_found('Problem not found: ' + str(id))

    resp = {'result': 'wrong'}
    if problem.answer == answer:
        resp = {'result': 'correct'}

    return resp
