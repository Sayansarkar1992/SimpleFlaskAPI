from flask import Flask, jsonify, request


def create_app():
    app = Flask(__name__)

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "service": "simple-flask-api"})

    @app.get("/api/greet")
    def greet():
        name = request.args.get("name", "World").strip() or "World"
        return jsonify({"message": f"Hello, {name}!"})

    @app.post("/api/add")
    def add_numbers():
        payload = request.get_json(silent=True) or {}
        a = payload.get("a")
        b = payload.get("b")

        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            return jsonify({"error": "Request JSON must include numeric 'a' and 'b' fields."}), 400

        return jsonify({"a": a, "b": b, "result": a + b})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
