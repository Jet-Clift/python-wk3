from flask import Flask, render_template, redirect, flash, request, session, url_for
import jinja2
from melons import melons
from forms import LoginForm
import customers
app = Flask(__name__)
app.jinja_env.undefined = jinja2.StrictUndefined
app.secret_key = "super secret"


@app.route("/")
def homepage():
    return render_template("base.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = customers.get_by_username(username)

        if not user or user["password"] !=password:
            flash("Invalid username or password")
            return redirect(url_for("login"))
    
        session["username"] = user["username"]
        flash("Logged in!")
        return redirect(url_for("all_melons"))
    return render_template("login.html", form=form)

app.route("/logout")
def logout():
    del session["username"]

    flash("Logged out!")
    return redirect(url_for("login"))

@app.route("/melons")
def all_melons():
    melon_list = melons.get_all()
    return render_template("all_melons.html", melon_list=melon_list)

@app.route("/melon/<melon_id>")
def melon_details(melon_id):
    melon = melons.get_by_id(melon_id)
    return render_template("melon_details.html", melon=melon)

@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    if "cart" not in session:
        session["cart"] = {}

    cart = session["cart"]
    cart[melon_id] = cart.get(melon_id, 0) + 1
    session.modified = True
    flash(f"Melon {melon_id} has been added to the cart.")
    print(cart)
    return redirect(url_for("show_shopping_cart"))

@app.route("/cart")
def show_shopping_cart():

    if "username" not in session:
        flash("Please log in first.")
        return redirect(url_for("login"))

    flash("Welcome to the shopping cart")

    order_total = 0
    cart_melons = []

    cart = session.get("cart", {})

    for melon_id, quantity in cart.items():
        melon = melons.get_by_id(melon_id)

        total_cost = melon.price * quantity

        order_total += total_cost

        melon.quantity = quantity
        melon.total_cost = total_cost

        cart_melons.append(melon)

        

    return render_template("cart.html")

@app.route("/empty-cart")
def empty_cart():
    session["cart"] = {}

    return redirect(url_for("show_shopping_cart"))

@app.errorhandler(404)
def error_404(e):
    return render_template("404.html")

if __name__ == "__main__":
    app.env = "development"
    app.run(debug = True, port = 8000, host = "localhost")