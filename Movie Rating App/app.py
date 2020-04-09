from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import force_instant_defaults

app=Flask("__name__")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db=SQLAlchemy(app)

class MovieRating(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(50), nullable=False)
    review=db.Column(db.Text, nullable=False)
    director=db.Column(db.String(50), default='No Director')
    rating=db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return "Movie Post "+str(self.id)

@app.route('/movies', methods=['GET','POST'])
def display_reviews():
    all_movies=MovieRating.query.all()
    return render_template('movies.html',movies=all_movies)

@app.route('/movies/delete/<int:id>',methods=['GET','POST'])
def del_rating(id):
    movie=MovieRating.query.get(id)
    db.session.delete(movie)
    db.session.commit()
    return redirect('/movies')

@app.route('/movies/edit/<int:id>',methods=['GET','POST'])
def edit_rating(id):
    movie=MovieRating.query.get(id)
    if request.method == 'POST':
        movie.title=request.form['title']
        movie.review=request.form['review']
        movie.director=request.form['director']
        movie.rating=request.form['rating']
        db.session.commit()
        return redirect('/movies')
    else:
        return render_template('edit.html',movies=movie)
@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/about')
def about_page():
    return render_template('websitevicky.html')


@app.route('/movies/new',methods=['GET','POST'])
def new_rating():
    if request.method == 'POST':
        movie_title=request.form['title']
        movie_review=request.form['review']
        movie_director=request.form['director']
        movie_rating=request.form['rating']
        new_movie=MovieRating(title=movie_title,review=movie_review,director=movie_director,rating=movie_rating)
        db.session.add(new_movie)
        db.session.commit()
        return redirect('/movies')

    else:
        return render_template('new_movie.html')


if __name__ == "__main__":
    app.run(debug=True)