from flask import Flask, request, render_template, jsonify
from src.pipelines.prediction_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application

@app.route("/", methods=["GET", "POST"])
def predict_datapoint():
    if request.method == "GET":
        return render_template("index.html")
    else:
        data = request.get_json()  # Get JSON data from the request
        custom_data = CustomData(
            carat=float(data["carat"]),
            depth=float(data["depth"]),
            table=float(data["table"]),
            x=float(data["x"]),
            y=float(data["y"]),
            z=float(data["z"]),
            cut=data["cut"],
            color=data["color"],
            clarity=data["clarity"],
        )
        final_new_data = custom_data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(final_new_data)

        result = round(pred[0], 2)
        return jsonify({"price": result})  # Return JSON response

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
