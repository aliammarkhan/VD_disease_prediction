# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 23:52:29 2020

@author: Biohazard
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 15:59:31 2020

@author: Biohazard
"""

from flask import Flask,request,jsonify
import pandas as pd
import urllib.request
import json

app = Flask(__name__)


Symptoms=['back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine',
'yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach',
'swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation',
'redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs',
'fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool',
'irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs',
'swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails',
'swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips',
'slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints',
'movement_stiffness','spinning_movements','loss_of_balance','unsteadiness',
'weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine',
'continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)',
'depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain',
'abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum',
'rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion',
'receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen',
'history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf',
'palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling',
'silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose',
'yellow_crust_ooze']



#loading the models

df = pd.read_csv('Disease_Training.csv')[1:2][Symptoms]
url = 'https://ussouthcentral.services.azureml.net/workspaces/6ccc7723df19492fbb130b5f25e9bd86/services/5ca5a7196f974399b35e2c62eb14e581/execute?api-version=2.0&format=swagger'
api_key = 'wA7LwXKW1mDX1gWwJ+yxW7j77NE0yxiUtNHld0To5lv0PREfxcKCPE949TYf8LSVEeqOTTlk0yAW8JJ3Kbp/HQ==' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
@app.route('/',methods=['POST'])
def predict2():
    try:
        data = request.get_json(force=True)['symptoms']
        if len(data) ==0:
            return jsonify({'error':'Please Select a symptom before submitting !!'})

        df.iloc[:,0:] = 0
        df['fluid_overload'] = 0
        df.drop(['fluid_overload'],axis = 1,inplace = True)


        for j in data:
            df[j] = 1
        d = {}
        for col in df.columns:
            d[col] = str(df.iloc[0][col])
        d['prognosis'] = ""
        d['fluid_overload'] = "0"
        d['fluid_overload (2)'] = "0"


        data ={"Inputs" : {"input1": [d]},"GlobalParameters":{}}
        #print(data)
        body = str.encode(json.dumps(data))
        req = urllib.request.Request(url, body, headers)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read())
        prediction = result["Results"]["output1"][0]["Scored Labels"]
        return jsonify({"prediction":prediction})
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))
        return jsonify ({'error':"There is something wrong..Try Again !!"})
    except:
         return jsonify ({'error':"There is something wrong..Try Again !!"})
    

if __name__ == "__main__":
    app.run()# -*- coding: utf-8 -*-

