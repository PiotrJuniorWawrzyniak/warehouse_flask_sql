from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from warehouse_flask_sql import Warehouse, Action, Product, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///warehouse.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "supersecretkey"

db.init_app(app)
migrate = Migrate(app, db)


def initialize_warehouse():
    warehouse = Warehouse.read_from_db()
    if not warehouse:
        warehouse = Warehouse(account=0)
        warehouse.save_to_db()
    return warehouse


@app.route("/", methods=["GET", "POST"])
def index():
    error_message = None
    warehouse = initialize_warehouse()

    if request.method == "POST":
        action = request.form["action"]
        try:
            if action == "zakup":
                product_name = request.form["product_name"]
                product_price = float(request.form["product_price"])
                pieces_number = int(request.form["pieces_number"])
                if product_price <= 0 or pieces_number <= 0:
                    raise ValueError("Podaj poprawne dane.")
                if product_price * pieces_number > warehouse.account:
                    raise ValueError("Brak wystarczających środków na koncie.")
                product = Product.query.filter_by(
                    name=product_name, warehouse_id=warehouse.id
                ).first()
                if not product:
                    product = Product(
                        name=product_name,
                        quantity=pieces_number,
                        price=product_price,
                        warehouse_id=warehouse.id,
                    )
                else:
                    product.quantity += pieces_number
                product.save_to_db()
                warehouse.account -= product_price * pieces_number
                warehouse.save_to_db()
                action_desc = (
                    f"Kupiono {pieces_number} szt. {product_name} za {product_price} zł"
                )
                action = Action(description=action_desc, warehouse_id=warehouse.id)
                action.save_to_db()

            elif action == "sprzedaz":
                product_name = request.form["product_name"]
                pieces_number = int(request.form["pieces_number"])
                product = Product.query.filter_by(
                    name=product_name, warehouse_id=warehouse.id
                ).first()
                if not product or product.quantity < pieces_number:
                    raise ValueError("Brak wystarczającej ilości produktu w magazynie.")
                product.quantity -= pieces_number
                if product.quantity == 0:
                    db.session.delete(product)
                else:
                    product.save_to_db()
                warehouse.save_to_db()
                action_desc = f"Sprzedano {pieces_number} szt. {product_name}"
                action = Action(description=action_desc, warehouse_id=warehouse.id)
                action.save_to_db()

            elif action == "saldo":
                amount = float(request.form["amount"])
                warehouse.account += amount
                warehouse.save_to_db()
                action_desc = f"Zaktualizowano saldo: {amount} zł"
                action = Action(description=action_desc, warehouse_id=warehouse.id)
                action.save_to_db()

        except ValueError as e:
            error_message = str(e)

        return redirect(url_for("index"))

    products = Product.query.filter_by(warehouse_id=warehouse.id).all()
    actions = Action.query.filter_by(warehouse_id=warehouse.id).all()

    products = [product for product in products if product.quantity > 0]

    return render_template(
        "index.html",
        magazyn=products,
        saldo=warehouse.account,
        error_message=error_message,
    )


@app.route("/historia/", defaults={"line_from": None, "line_to": None}, methods=["GET"])
@app.route("/historia/<int:line_from>/<int:line_to>", methods=["GET"])
def historia(line_from, line_to):
    warehouse = initialize_warehouse()
    actions = Action.query.filter_by(warehouse_id=warehouse.id).all()

    if line_from is not None and line_to is not None:
        if line_from < 1 or line_to > len(actions) or line_from > line_to:
            flash(f"Nieprawidłowy zakres, zakres wynosi od 1 do {len(actions)}.")
            return redirect(url_for("historia"))
        actions = actions[line_from - 1 : line_to]
    elif request.args.get("line_from") and request.args.get("line_to"):
        line_from = int(request.args.get("line_from"))
        line_to = int(request.args.get("line_to"))
        if line_from < 1 or line_to > len(actions) or line_from > line_to:
            flash(f"Nieprawidłowy zakres, zakres wynosi od 1 do {len(actions)}.")
            return redirect(url_for("historia"))
        actions = actions[line_from - 1 : line_to]

    return render_template("historia.html", historia=actions)


if __name__ == "__main__":
    app.run(debug=True)
