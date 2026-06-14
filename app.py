from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

records = []
next_id = 1


def sort_records_by_date():
    global records
    records.sort(key=lambda x: x["date"], reverse=True)


def calculate_summary(filtered_records):
    income = 0
    expense = 0

    for record in filtered_records:
        amount = float(record["amount"]) if record["amount"] else 0
        if record["type"] == "收入":
            income += amount
        else:
            expense += amount

    balance = income - expense
    return income, expense, balance


@app.route("/", methods=["GET"])
def index():
    month = request.args.get("month", "")

    sort_records_by_date()

    all_income, all_expense, all_balance = calculate_summary(records)

    if month:
        filtered_records = [r for r in records if r["date"].startswith(month)]
        month_income, month_expense, month_balance = calculate_summary(filtered_records)
    else:
        filtered_records = records[:]
        month_income, month_expense, month_balance = 0, 0, 0

    return render_template(
        "index.html",
        records=filtered_records,
        month=month,
        all_income=all_income,
        all_expense=all_expense,
        all_balance=all_balance,
        month_income=month_income,
        month_expense=month_expense,
        month_balance=month_balance
    )


@app.route("/add", methods=["POST"])
def add():
    global next_id

    date = request.form.get("date")
    record_type = request.form.get("type")
    category = request.form.get("category")
    amount = request.form.get("amount")
    note = request.form.get("note")

    new_record = {
        "id": next_id,
        "date": date,
        "type": record_type,
        "category": category,
        "amount": amount,
        "note": note
    }

    records.append(new_record)
    next_id += 1

    return redirect(url_for("index"))


@app.route("/delete/<int:record_id>")
def delete(record_id):
    global records
    records = [r for r in records if r["id"] != record_id]
    return redirect(url_for("index"))


@app.route("/edit/<int:record_id>", methods=["GET", "POST"])
def edit(record_id):
    record = next((r for r in records if r["id"] == record_id), None)

    if record is None:
        return redirect(url_for("index"))

    if request.method == "POST":
        record["date"] = request.form.get("date")
        record["type"] = request.form.get("type")
        record["category"] = request.form.get("category")
        record["amount"] = request.form.get("amount")
        record["note"] = request.form.get("note")
        return redirect(url_for("index"))

    return render_template("edit.html", record=record)


if __name__ == "__main__":
    app.run(debug=True)

