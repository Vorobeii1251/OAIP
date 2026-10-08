from flask import (
    Flask, render_template, session, redirect,
    url_for, request, flash
)

app = Flask(__name__)
app.secret_key = "change-me-in-production"


PRODUCTS = [
    {"id": 1, "name": "Ноутбук", "price": 656399, "category": "Электроника"},
    {"id": 2, "name": "Смартфон", "price": 452300, "category": "Электроника"},
    {"id": 3, "name": "Наушники", "price": 3499,  "category": "Электроника"},
    {"id": 4, "name": "Книга «Python»", "price": 11999,  "category": "Книги"},
    {"id": 5, "name": "Книга «Flask»", "price": 1599,  "category": "Книги"},
    {"id": 6, "name": "Кружка", "price": 599,   "category": "Дом"},
    {"id": 7, "name": "Рюкзак", "price": 3999,  "category": "Аксессуары"},
    {"id": 8, "name": "Клавиатура", "price": 2599,  "category": "Электроника"},
]

PRODUCTS_BY_ID = {p["id"]: p for p in PRODUCTS}


def get_cart():
    if "cart" not in session:
        session["cart"] = {}
    return session["cart"]


def cart_items():
    cart = get_cart()
    items = []
    for pid_str, qty in cart.items():
        pid = int(pid_str)
        product = PRODUCTS_BY_ID.get(pid)
        if product is None:
            continue
        items.append({
            "id": pid,
            "name": product["name"],
            "category": product["category"],
            "price": product["price"],
            "quantity": qty,
            "sum": product["price"] * qty,
        })
    return items


def cart_stats(items):
    total_items = sum(i["quantity"] for i in items)
    unique_items = len(items)
    total_sum = sum(i["sum"] for i in items)
    return {
        "total_items": total_items,
        "unique_items": unique_items,
        "total_sum": total_sum,
    }


@app.route("/")
def index():
    cart = get_cart()
    return render_template(
        "index.html",
        products=PRODUCTS,
        cart=cart,
    )


@app.route("/cart")
def cart():
    items = cart_items()
    stats = cart_stats(items)
    return render_template("cart.html", items=items, stats=stats)


@app.route("/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    if product_id not in PRODUCTS_BY_ID:
        flash("Товар не найден", "danger")
        return redirect(url_for("index"))

    cart = get_cart()
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    session.modified = True

    flash(f"«{PRODUCTS_BY_ID[product_id]['name']}» добавлен в корзину", "success")
    return redirect(request.referrer or url_for("index"))


@app.route("/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = get_cart()
    key = str(product_id)
    if key in cart:
        del cart[key]
        session.modified = True
        flash("Товар удалён из корзины", "info")
    return redirect(url_for("cart"))


@app.route("/clear", methods=["POST"])
def clear_cart():
    session["cart"] = {}
    session.modified = True
    flash("Корзина очищена", "info")
    return redirect(url_for("cart"))


if __name__ == "__main__":
    app.run(debug=True)