from flask_app import app, render_template, redirect, request, session, flash, bcrypt
from flask_app.models.recipe import Recipe



#GET ALL
@app.route('/mycookbook')
def get_all_recipes():
    if 'user_id' not in session:
        return redirect('/logout')
    recipes = Recipe.get_all_recipes(session['user_id'])
    return render_template('dashboard.html', recipes = recipes)

#SEARCH PAGE
@app.route('/search')
def load_search():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('search.html')

#NEW - render form
@app.route('/mycookbook/new-recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/mycookbook')
    return render_template('new.html')

#NEW - process the form and redirect
@app.route('/create', methods=['POST'])
def create_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/mycookbook/new-recipe')
    Recipe.save(request.form)
    return redirect('/recipes') #redirect to show page for this recipe

@app.route('/recipe/<int:id>')
def show_recipe(id):
    return render_template("show.html",recipe=Recipe.get_recipe(id))

#UPDATE - This route renders the form
@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/mycookbook')
    recipe = Recipe.get_recipe(id)
    if session['user_id'] != recipe.user_id:
        return redirect('/mycookbook')
    return render_template('edit.html', recipe=recipe)

#UPDATE - Processing
@app.route('/recipes/update/<int:id>',methods=['POST'])
def update(id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/recipes/edit/{request.form['id']}")
    Recipe.update(request.form)
    return redirect("/recipes")

#DELETE
@app.route('/delete-recipe/<int:id>')
def delete(id):
    recipe = Recipe.get_recipe(id)
    if session['user_id'] != recipe.user_id:
        return redirect('/recipes')
    if 'user_id' not in session:
        return redirect('/logout')
    Recipe.delete(id)
    return redirect('/recipes')


# #A redirect with reference to an id gotten from the page
# @app.route("/recipes/<int:id>", methods=['POST'])
# def show_recipe(id):
#     Recipe.get_recipe(id)
#     return redirect(f"/somewhere/{'id'}")