from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import json


app = Flask(__name__)
CORS(app)

# Initialize AWS Clients
s3 = boto3.client("s3", region_name="us-east-2")  # Change this to your AWS region
lambda_client = boto3.client("lambda", region_name="us-east-2")
S3_BUCKET = "nfl-player-analysis-results"

@app.route("/search", methods=["GET"])
def search_qb():
    qb_name = request.args.get("qb_name")
    if not qb_name:
        return jsonify({"error": "Please provide a QB name"}), 400

    # Format file name for S3 lookup
    s3_file = f"{qb_name.replace(' ', '_').lower()}_prediction.json"
    print(f"Looking for file in S3: {s3_file}")

    # Check if data is already in S3
    try:
        s3_object = s3.get_object(Bucket=S3_BUCKET, Key=s3_file)
        data = json.loads(s3_object["Body"].read().decode("utf-8"))
        return jsonify(data)
    except s3.exceptions.NoSuchKey:
        # If not in S3, call Lambda to generate data
        response = lambda_client.invoke(
            FunctionName="nfl_player_scraper",
            InvocationType="RequestResponse",
            Payload=json.dumps({"player_name": qb_name})
        )
        new_data =  json.loads(response["Payload"].read())
        print("Newly generated data:", new_data)
        predicted_data = new_data.get("predicted_data",{}).get("data",{})
        return jsonify(predicted_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
