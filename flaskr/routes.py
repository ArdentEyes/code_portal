from flask import render_template, flash, redirect, url_for, request, abort
from flaskr import app, db
from flaskr.forms import RegistrationForm, LoginForm, PostForm
from flaskr.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query\
        .order_by(Post.contest_date.desc()).paginate(page=page, per_page=2)
    return render_template('home.html', title='Home Page', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        t_user = User.query.filter_by(username=form.username.data).first()
        if t_user and (t_user.pwd == form.password.data):
            login_user(t_user, remember=form.remember.data)
            flash(f'You have been logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page\
                else redirect(url_for('home'))
        else:
            flash(f'Wrong credentials', 'danger')
    return render_template('login.html', title='Login Page', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        temp_user = User(username=form.username.data, pwd=form.password.data)
        db.session.add(temp_user)
        db.session.commit()
        flash('Account Created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register Page', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, contest_url=form.url.data,
                    content=form.content.data,
                    author=current_user, contest_date=form.date.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html',
                           title='New Post', form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.contest_url = form.url.data
        post.content = form.content.data
        post.contest_date = form.date.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.url.data = post.contest_url
        form.date.data = post.contest_date
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.contest_date.desc())\
        .paginate(page=page, per_page=2)
    return render_template('user_posts.html', posts=posts, user=user)
