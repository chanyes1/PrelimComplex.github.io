from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Route to calculate prelim average
@app.route('/calculate_prelim', methods=['POST'])
def calculate_prelim():
    prelim_grades = request.form.getlist('grades[]', type=float)
    prelim_avg = sum(prelim_grades) / len(prelim_grades)
    return jsonify({"prelim_avg": round(prelim_avg, 2)})

# Route to calculate the minimum midterm and final grades needed to pass and to be a Dean's Lister
@app.route('/calculate_required_grades', methods=['POST'])
def calculate_required_grades():
    prelim = float(request.form['prelim'])

    # Calculate the minimum midterm grades required to pass and be a Dean's Lister
    min_midterm_pass = (75 - (prelim * 0.2)) / 0.8
    min_midterm_dean = (90 - (prelim * 0.2)) / 0.8

    min_midterm_pass = max(0, min(min_midterm_pass, 100))
    min_midterm_dean = max(0, min(min_midterm_dean, 100))

    return jsonify({
        "min_midterm_pass": round(min_midterm_pass, 2),
        "min_midterm_dean": round(min_midterm_dean, 2)
    })

# Route to calculate the final grade needed based on midterm performance
@app.route('/calculate_final', methods=['POST'])
def calculate_final():
    prelim = float(request.form['prelim'])
    midterm = float(request.form['midterm'])
    target = float(request.form['target'])

    # Calculate the required final grade
    required_final = (target - (prelim * 0.2) - (midterm * 0.3)) / 0.5
    required_final = max(0, min(required_final, 100))

    return jsonify({
        "required_final": round(required_final, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
