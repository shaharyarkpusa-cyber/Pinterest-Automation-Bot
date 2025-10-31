"""Flask web application for generating random full names."""

from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from name_generator.generator import generate_names


app = Flask(__name__)


def _parse_count(raw: str, default: int = 10, limit: int = 500) -> int:
    try:
        value = int(raw)
    except (TypeError, ValueError):
        raise ValueError("Count must be an integer")
    if value <= 0:
        raise ValueError("Count must be positive")
    if value > limit:
        raise ValueError(f"Count cannot exceed {limit}")
    return value


def _parse_seed(raw: str | None) -> int | None:
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError("Seed must be an integer") from exc


@app.route("/", methods=["GET", "POST"])
def index():
    names: list[str] = []
    error: str | None = None

    count_field = request.form.get("count") if request.method == "POST" else request.args.get("count")
    gender = request.form.get("gender", request.args.get("gender", "any"))
    seed_field = request.form.get("seed", request.args.get("seed", ""))

    # Preserve user input for the template
    form_data = {
        "count": count_field or "10",
        "gender": gender or "any",
        "seed": seed_field or "",
    }

    if request.method == "POST" or any(v for v in (count_field, seed_field) if v):
        try:
            count = _parse_count(form_data["count"])
            seed = _parse_seed(seed_field)
            generated = generate_names(count, gender=gender or "any", seed=seed)
            names = [item.full_name for item in generated]
        except ValueError as exc:
            error = str(exc)

    return render_template("index.html", names=names, error=error, form_data=form_data)


@app.get("/api/names")
def api_names():
    count_raw = request.args.get("count", "10")
    gender = request.args.get("gender", "any")
    seed_raw = request.args.get("seed", "")

    try:
        count = _parse_count(count_raw, limit=1000)
        seed = _parse_seed(seed_raw)
        names = generate_names(count, gender=gender, seed=seed)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    payload = [
        {
            "first_name": name.first_name,
            "last_name": name.last_name,
            "full_name": name.full_name,
        }
        for name in names
    ]
    return jsonify(payload)


if __name__ == "__main__":
    app.run(debug=True)
