import joblib
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load the model and scaler
loaded_model = joblib.load('models/insurance_model1.pkl')
scaler = joblib.load('models/scaler.pkl')

def calculate_bmi(weight, height):
    height_m = height / 100
    return weight / (height_m ** 2)

def interpret_result(age, bmi, children, smoker, price):
    interpretation = f"Based on the provided information (Age: {age}, BMI: {bmi:.1f}, Children: {children}, Smoker: {'Yes' if smoker else 'No'}), your predicted insurance price is ${price:.2f}. "
    interpretation += "Here's why:\n\n"

    if bmi < 18.5:
        interpretation += "- Your BMI is considered underweight, which might slightly increase health risks.\n"
    elif 18.5 <= bmi < 25:
        interpretation += "- Your BMI is in the normal range, which is favorable for health insurance rates.\n"
    elif 25 <= bmi < 30:
        interpretation += "- Your BMI is in the overweight range, which may increase health risks and insurance costs.\n"
    else:
        interpretation += "- Your BMI is in the obese range, which significantly increases health risks and insurance costs.\n"

    if smoker:
        interpretation += "- Being a smoker substantially increases your insurance premium, as it's associated with higher health risks.\n"
    else:
        interpretation += "- Being a non-smoker is favorable for your insurance premium.\n"

    if age < 30:
        interpretation += "- Your young age is generally associated with lower insurance costs.\n"
    elif 30 <= age < 50:
        interpretation += "- Your age puts you in a moderate risk category for insurance pricing.\n"
    else:
        interpretation += "- Your age may lead to higher insurance costs due to increased health risks.\n"

    if children > 0:
        interpretation += f"- Having {children} child(ren) may affect your insurance costs, often increasing them slightly.\n"

    interpretation += "\nRemember, insurance pricing is complex and considers many factors. This interpretation is based on general trends observed in the data."

    return interpretation

@app.route('/', methods=['GET', 'POST'])
def predict_insurance():
    if request.method == 'POST':
        age = float(request.form['age'])
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        children = int(request.form['children'])
        smoker = int(request.form['smoker'])

        # Calculate BMI
        bmi = calculate_bmi(weight, height)

        # Create a DataFrame for new input
        new_data = pd.DataFrame([[age, bmi, children, smoker]], 
                                columns=['age', 'bmi', 'children', 'smoker'])

        # Scale the new data
        new_data_scaled = scaler.transform(new_data)

        # Predict using the scaled data
        result = loaded_model.predict(new_data_scaled)[0]

        # Generate interpretation
        interpretation = interpret_result(age, bmi, children, smoker, result)

        return jsonify({
            'price': f"{result:.2f}",
            'interpretation': interpretation
        })

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
