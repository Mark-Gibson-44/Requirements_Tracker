from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('reports', __name__)

@bp.route('/')
def index():
    db = get_db()
    projects = db.execute(
                    'SELECT * FROM _project'
                ).fetchall()
    return render_template('index.html', projects = projects)

@bp.route('/browse_projects')
def browse_projects():
    db = get_db()
    projects = db.execute(
        'SELECT * FROM _project'
    ).fetchall()

    return render_template('tracking/projects.html', projects=projects)


@bp.route('/tracking/create_project', methods=('GET', 'POST'))
def create_project():
    if request.method == 'POST':
        project_title = request.form['title']
        error = None
        if not project_title:
            error = 'Title needed'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO _project (title) VALUES (?)',
                (project_title,)
            )
            db.commit()

    return render_template('tracking/create_project.html')


'''
Responsible for showing information of a given project

p_id -> integer: Used To Identify project 
'''
@bp.route('/<int:project_id>/browse_project')
def view_project(project_id):
    db = get_db()
    cases = db.execute('SELECT * FROM _case WHERE _project_id = ?', (project_id,)).fetchall()

    return render_template('tracking/view_project.html', cases=cases)


@bp.route('/<int:project_id>/gen_tree')
def gen_tree(project_id):
    db = get_db()
    cases = db.execute('SELECT * FROM _case WHERE _project_id = ?', (project_id,)).fetchall()
    out = open('out.txt')
    out.write('digraph\n{\n')
    for case in cases:
        out.write('{0} -> {1}, \n'.format(case['id'], case['child_id']))
    out.write('}')
    return redirect(url_for('index'))