from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/generate-timetable', methods=['POST'])
def generate_timetable():
    data = request.json
    subjects = data.get('subjects', [])
    exam_dates = data.get('examDates', [])
    daily_hours = data.get('dailyHours', 0)

    try:
        parsed_dates = [datetime.strptime(date_str, '%Y-%m-%d') for date_str in exam_dates]
    except Exception as e:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    sorted_pairs = sorted(zip(subjects, parsed_dates), key=lambda x: x[1])
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_index = 0

    timetable = []
    for subject, exam_date in sorted_pairs:
        for _ in range(int(daily_hours)):
            timetable.append({
                "day": days_of_week[day_index % len(days_of_week)],
                "subject": subject,
                "examDate": exam_date.strftime("%Y-%m-%d")
            })
            day_index += 1

    return jsonify(timetable)

if __name__ == '__main__':
    app.run(debug=True)