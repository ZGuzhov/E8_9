import requests
from datetime import datetime
from flask import render_template, request, redirect
from app import app, db, celery
from .models import Results, Tasks
from .forms import WebsiteForm


@celery.task
def parse_website_text(_id):
    task = Tasks.query.get(_id)
    task.task_status = 'PENDING'
    db.session.commit()
    address = task.address
    if not address.startswith('http') and not address.startswith('https'):
        address = 'http://' + address
    with app.app_context():
        try:
            # отключаем проверку SSL и ограничиваем длительность запроса 10 секундами
            # при превышении 10 секунд status_code возвращает 404
            res = requests.get(address, verify=False, timeout=10)
            words_count = 0
            if res.ok:
                words = res.text.split()
                words_count = words.count("Python")
            result = Results(address=address, words_count=words_count, http_status_code=res.status_code)
            task = Tasks.query.get(_id)
            task.task_status = 'FINISHED'
            db.session.add(result)
            db.session.commit()
        # в идеале надо ловить конкретные исключения, но на учебном проекте будем считать, что это всегда ошибка 404
        except:
            result = Results(address=address, words_count=0, http_status_code=404)
            task = Tasks.query.get(_id)
            task.task_status = 'FINISHED'
            db.session.add(result)
            db.session.commit()


@app.route('/', methods=['POST', 'GET'])
def website():
    website_form = WebsiteForm()
    if request.method == 'POST':
        if website_form.validate_on_submit():
            address = request.form.get('address')
            task = Tasks(address=address, timestamp=datetime.now(), task_status='NOT_STARTED')
            db.session.add(task)
            db.session.commit()
            parse_website_text(task._id)
            return redirect('/')
        error = "Ошибка заполнения формы"
        return render_template('error.html', form=website_form, error=error)
    return render_template('index.html', form=website_form)


@app.route('/results')
def get_results():
    results = Results.query.all()
    return render_template('results.html', results=results)