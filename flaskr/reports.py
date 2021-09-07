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

    return render_template('tracking/view_project.html', cases=cases, id=project_id)


@bp.route('/<int:project_id>/gen_tree')
def gen_tree(project_id):
    db = get_db()
    cases = db.execute('SELECT * FROM _case WHERE _project_id = ?', (project_id,)).fetchall()
    out = open('out.txt', 'w')
    out.write('digraph\n{\n')
    for case in cases:
        out.write('{}\n'.format(case['id']))
        if(case['child_id'] is not ""):
            print(case['child_id'])
            out.write('{0} -> {1} \n'.format(case['id'], case['child_id']))
        if(case['parent_id'] is not ""):
            out.write('{0} -> {1} \n'.format(case['parent_id'], case['id']))
    out.write('}')
    return redirect(url_for('index'))

@bp.route('/<int:project_id>/add_case', methods=('GET', 'POST'))
def add_case(project_id):
    if request.method == 'POST':
        Desc = request.form['Description']
        error = None
        if not Desc:
            error = 'Title needed'
        parent_case = request.form['parent_case']
        child_case = request.form['child_case']
        data = [Desc, project_id]
        if parent_case is not None:
            data.append(parent_case)
        if child_case is not None:
            data.append(child_case)
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO _case (_description, _project_id, parent_id, child_id) VALUES (?, ?, ?, ?)',
                (Desc, project_id, parent_case, child_case,)
            )
            db.commit()
        
    return render_template('tracking/add_case.html')