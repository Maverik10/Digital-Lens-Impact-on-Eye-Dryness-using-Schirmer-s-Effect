from flask import Flask, render_template, request
import pickle
import numpy as np
import os

# Correcting the file path (Assuming the actual pickle file is "model.pkl")
filename = r'C:\Users\cialg\Downloads\Capstone 1 (2)\Capstone 1\Eyemodel.pkl'

# Load the trained classifiers (Ensure 'model.pkl' exists and is a valid pickle file)
with open(filename, 'rb') as f:
    loaded_classifiers = pickle.load(f)

app = Flask(__name__)

def make_predictions(data):
    predictions = {}
    for key, clf in loaded_classifiers.items():
        prediction = clf.predict(data)
        predictions[key] = prediction[0]
    return predictions

@app.route('/')
def home():
    return render_template('frontpage.html')

@app.route('/Test', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Retrieving input values safely
            Age = int(request.form.get('age', 0))
            Sex = int(request.form.get('sex', 0))
            wearables = int(request.form.get('eyewear', 0))
            Duration = int(request.form.get('usageDuration', 0))
            onlineplatforms = int(request.form.get('onlinePlatforms', 0))
            Nature = int(request.form.get('computerUsage', 0))
            screenillumination = int(request.form.get('screenIllumination', 0))
            workingyears = int(request.form.get('yearsWorking', 0))
            hoursspentdailycurricular = int(request.form.get('hoursOnlineClasses', 0))
            hoursspentdailynoncurricular = int(request.form.get('screenTimeNonCurricular', 0))
            Gadgetsused = int(request.form.get('mostUsedGadget', 0))
            levelofgadjetwithrespecttoeyes = int(request.form.get('gadgetLevel', 0))
            Distancekeptbetweeneyesandgadjet = int(request.form.get('distanceEyesGadget', 0))
            Avgnighttimeusageperday = int(request.form.get('nightTimeUsage', 0))
            Blinkingduringscreenusage = int(request.form.get('remindToBlink', 0))
            Difficultyinfocusingafterusingscreens = int(request.form.get('difficultyFocusing', 0))
            freqquencyofcomplaints = int(request.form.get('complaintsFrequency', 0))
            Severityofcomplaints = int(request.form.get('ocularSeverity', 0))
            
            # Handling list inputs safely
            Ocularsymptomsobservedlately = request.form.getlist('ocularSymptoms')
            Symptomsobservingatleasthalfofthetimes = request.form.getlist('symptomsObservation')
            
            if Ocularsymptomsobservedlately:
                total_symptoms = sum(map(int, Ocularsymptomsobservedlately)) / len(Ocularsymptomsobservedlately)
            else:
                total_symptoms = 0
            Ocularsymptomsobservedlately = int(total_symptoms)

            if Symptomsobservingatleasthalfofthetimes:
                total = sum(map(int, Symptomsobservingatleasthalfofthetimes)) / len(Symptomsobservingatleasthalfofthetimes)
            else:
                total = 0
            Symptomsobservingatleasthalfofthetimes = int(total)

            Complaintsfrequency = int(request.form.get('complaintFrequency', 0))
            frequencyofdryeyes = int(request.form.get('dryFrequency', 0))

            # Creating the feature array
            data = np.array([[Age, wearables, workingyears, Nature,
                              hoursspentdailycurricular, hoursspentdailynoncurricular,
                              Gadgetsused, Avgnighttimeusageperday, Blinkingduringscreenusage,
                              freqquencyofcomplaints, Severityofcomplaints,
                              Ocularsymptomsobservedlately, Symptomsobservingatleasthalfofthetimes,
                              Complaintsfrequency]])

            # Make predictions
            predictions = make_predictions(data)
            return render_template('result.html', predictions=predictions)

        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
