from app import app, db, mail, celery
from flask import request, render_template, url_for, redirect, flash, session
from .models import Articles, User
from .forms import ArticleForm, ContactForm
from functools import wraps
from flask_mail import Mail, Message

POSTS_PER_PAGE = 4


@app.route('/', defaults={'page': 1}, methods=['GET'])
@app.route('/page/<int:page>')
def index(page=1):
    posts = Articles.query.order_by(Articles.created_date.desc()).paginate(page, per_page=4, error_out=False)
    return render_template('index.html', posts=posts)


#Login template
@app.route('/add_user')
def add_user():
    return render_template('add_user.html')


#Login template
@app.route('/login', methods=['POST'])
def login():
    user_logging_in = User('first_name_dummy', request.form['form-username'], 'smiec1@mail.com', request.form['form-password'])
    username_lookup = user_logging_in.username
    user = User.query.filter_by(username=username_lookup).first()
    if(user_logging_in.password != user.password):
        flash("Password is incorrect")
        return render_template('add_user.html')
    else:
        session['logged_in'] = True
        session['username'] = user_logging_in.username
        flash('You are now logged in')
        return render_template('add_user.html')


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login')
            return redirect(url_for('add_user'))
    return wrap


@app.route('/logged_out')
def logged_out():
    session.clear()
    flash('You are now logged out')
    return redirect(url_for('add_user'))


#Add user to the db
@app.route('/post_user', methods=['POST'])
def add_user_db():
    user = User(request.form['first_name'], request.form['username'], request.form['email'], request.form['password'])
    db.session.add(user)
    db.session.commit()
    flash('User was Created successfully. Thank you for registration.')
    return render_template('add_user.html')


# Add Article
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def article_form():
    article_form = ArticleForm()
    return render_template('add_article.html', article_form=article_form)


#Submit Article to DB
@app.route('/post_article', methods=['POST'])
@is_logged_in
def add_article_db():
    author = session['username']
    article = Articles(request.form['title'], request.form['content'], author)
    article_form = ArticleForm()
    db.session.add(article)
    db.session.commit()
    flash('Article was Created successfully')
    return render_template('add_article.html', article_form=article_form)


#Edit Article to DB
@app.route('/edit_article/<string:id>', methods=['GET','POST'])
@is_logged_in
def edit_article(id):
    result = Articles.query.filter_by(id=id).first()

    article_form = ArticleForm()

    article_form.id.data = result.id
    article_form.title.data = result.title
    article_form.content.data = result.content

    if request.method == 'POST':
        Articles.query.filter_by(id=id).update(dict(title=request.form['title'], content=request.form['content']))
        db.session.commit()
        flash('Article Updated successfully')
        return render_template('edit_article.html', article_form=article_form)

    return render_template('edit_article.html', article_form=article_form)


@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    Articles.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Article Deleted successfully')
    return redirect(url_for('post'))



@app.route('/articles/<string:id>')
def articles(id):
    one_article = Articles.query.filter_by(id=id).first()
    return render_template('articles.html', one_article=one_article)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/post_cat')
@is_logged_in
def post():
    articles = [u.__dict__ for u in Articles.query.all()]
    if articles > 0:
        return render_template('post.html', articles=articles)
    else:
        msg = 'No articles Found'
        return render_template('post.html', msg=msg)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm()
        msg = Message("Message from your visitor", sender='test@test.gmail.com',
                      recipients=['lizinczyk.karolina@gmail.com'])
        msg.body = """
                    From: %s <%s>,
                    %s
                    """ % (form.username.data, form.email.data, form.message.data)

        send_async_email.apply_async(args=[msg], countdown=120)

        return redirect(url_for('contact'))

    return render_template('contact.html', form=form)


@celery.task(trail=True)
def send_async_email(msg):
    with app.app_context():
        mail.send(msg)
    print("Done!!!!!")

