from flask import Flask, request, jsonify, render_template
from rag_graph import app_graph  # your RAG compiled graph

app = Flask(__name__, template_folder="templates", static_folder="static")

# Route for home page
@app.route("/")
def home():
    return render_template("index.html")

# Route to handle analyze requests
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json

    # Prepare input state for RAG graph
    state_input = {
        "age": int(data.get("age", 0)),
        "state": data.get("state", "").strip(),
        "scenario": data.get("scenario", "").strip(),
        "helplines": [],
        "advice": ""
    }

    try:
        # Invoke RAG graph
        result = app_graph.invoke(state_input)

        # Select only desired helpline fields
        filtered_helplines = [
            {
                "helpline_name": h.get("helpline_name"),
                "phone_number": h.get("phone_number"),
                "description": h.get("description"),
                "source_type": h.get("source_type"),
                "state": h.get("state"),
            }
            for h in result.get("helplines", [])
        ]

        response = {
            "helplines": filtered_helplines,
            "advice": result.get("advice", "Call the helpline above. Stay safe!")
        }

    except Exception as e:
        print("Error in /analyze:", e)
        response = {"helplines": [], "advice": "Something went wrong. Check input."}

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
