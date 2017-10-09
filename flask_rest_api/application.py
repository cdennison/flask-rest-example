import logging
import os

from flask import Flask
from werkzeug.utils import import_string
from . import config, db, io
from flasgger import Swagger
from flask_cors import CORS, cross_origin
import csv
import traceback
from flask_rest_api.problems.models import Problem

logger = logging.getLogger(__name__)

def load_data(csv_filepath):
    rows_for_insert = []

    DELIM1='|'
    DELIM2=','

    dir = os.path.dirname(__file__)
    csv_filepath = os.path.join(dir, '../'+csv_filepath)

    with open(csv_filepath) as csvDataFile:
        csvReader = csv.reader(csvDataFile)

        for index,row in enumerate(csvReader):
            row_to_insert = {
                'question':'',
                'answer':'',
                'distraction1':'',
                'distraction2':'',
                'distraction3':'',
                'distraction4':'',
                'distraction5':''
            }

            # if index==11:
            #     break

            #Skip header
            if index==0:
                continue
            try:
                row_to_insert['question']=row[0].split(DELIM1)[0]
                row_to_insert['answer']=row[0].split(DELIM1)[1]
                row_to_insert['distraction1']=row[0].split(DELIM1)[2]
                for i,d in enumerate(row[1:]):
                    row_to_insert['distraction%s'%(i+2)]=d
            except:
                print ('Failed to parse row: '+str(row))
                print (traceback.format_exc())

            # print(row_to_insert)
            rows_for_insert.append(Problem(**row_to_insert))

    return rows_for_insert
    # i = problems.insert()
    # for row in rows_for_insert:
    #     i.execute(**row)

def create_app(environment):
    """Creates a new Flask application and initialize application."""

    config_map = {
        'development': config.Development(),
        'testing': config.Testing(),
        'production': config.Production(),
    }

    config_obj = config_map[environment.lower()]

    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config_obj)

    app.url_map.strict_slashes = False
    app.add_url_rule('/', '/static/index.html', home)

    register_blueprints(app)

    db.init_app(app)
    io.init_app(app)
    CORS(app)

    with app.app_context():
        db.create_all()

        rows_for_insert=load_data(config_obj.CSV_REL_FILE_PATH)

        for row in rows_for_insert:
            db.session.add(row)
        db.session.commit()

    return app

# def create_app(environment):
#     config_map = {
#         'development': config.Development(),
#         'testing': config.Testing(),
#         'production': config.Production(),
#     }
#
#     config_obj = config_map[environment.lower()]
#
#     app = Flask(__name__)
#     app.config.from_object(config_obj)
#
#     app.config['SWAGGER'] = {
#         'title': '2 Colors API',
#         'uiversion': 2
#     }
#
#     db.init_app(app)
#
#     Swagger(app)
#
#     return app


    @app.route('/colors/<palette>/')
    def colors(palette):
        """Example endpoint return a list of colors by palette
        This is using docstring for specifications
        ---
        tags:
          - colors
        parameters:
          - name: palette
            in: path
            type: string
            enum: ['all', 'rgb', 'cmyk']
            required: true
            default: all
            description: Which palette to filter?
        operationId: get_colors
        consumes:
          - application/json
        produces:
          - application/json
        security:
          colors_auth:
            - 'write:colors'
            - 'read:colors'
        schemes: ['http', 'https']
        deprecated: false
        externalDocs:
          description: Project repository
          url: http://github.com/rochacbruno/flasgger
        definitions:
          Palette:
            type: object
            properties:
              palette_name:
                type: array
                items:
                  $ref: '#/definitions/Color'
          Color:
            type: string
        responses:
          200:
            description: A list of colors (may be filtered by palette)
            schema:
              $ref: '#/definitions/Palette'
            examples:
              rgb: ['red', 'green', 'blue']
        """
        all_colors = {
            'cmyk': ['cian', 'magenta', 'yellow', 'black'],
            'rgb': ['red', 'green', 'blue']
        }
        if palette == 'all':
            result = all_colors
        else:
            result = {palette: all_colors.get(palette)}

        return result


def home():
    return dict(name='Flask REST API')


def register_blueprints(app):
    root_folder = '/Users/dennch3/temp/flask-rest-example/flask_rest_api'

    for dir_name in os.listdir(root_folder):
        module_name = 'flask_rest_api' + '.' + dir_name + '.views'
        module_path = os.path.join(root_folder, dir_name, 'views.py')

        if os.path.exists(module_path):
            module = import_string(module_name)
            obj = getattr(module, 'app', None)
            if obj:
                app.register_blueprint(obj)
