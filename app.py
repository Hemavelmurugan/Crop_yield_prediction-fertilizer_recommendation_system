# from flask import Flask, request, render_template, jsonify
# import pandas as pd
# import pickle
# import joblib

# app = Flask(__name__)

# # Load the trained model
# model = pickle.load(open('models/crop_yield_model_lr.pkl', 'rb'))

# # Home routes
# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/weather')
# def weather_page():
#     return render_template('weather.html')

# @app.route('/rainfall_sunlight')
# def rainfall_sunlight_page():
#     return render_template('rainfall_sunlight.html')

# @app.route('/soil')
# def soil_page():
#     return render_template('soil.html')

# @app.route('/result')
# def result_page():
#     return render_template('result.html')

# # ----------------- Weather API -----------------
# @app.route('/api/weather')
# def api_weather():
#     lat = request.args.get('lat')
#     lon = request.args.get('lon')

#     # Replace this part with your real weather API call
#     # Simulated values for demonstration
#     if not lat or not lon:
#         return jsonify({'error': 'Latitude and Longitude required'}), 400

#     simulated_data = {
#         'temperature': 28.3,
#         'humidity': 65.2
#     }

#     return jsonify(simulated_data)


# # ----------------- Prediction -----------------
# @app.route('/predict', methods=['POST'])
# def predict():
#     form = request.form

#     # Extract form inputs
#     features = {
#         'Farm_Area(acres)': float(form.get('farm_area')),
#         'Temperature(°C)': float(form.get('temperature')),
#         'Humidity(%)': float(form.get('humidity')),
#         'Rainfall(mm)': float(form.get('rainfall')),
#         'Sunlight_Hours': float(form.get('sunlight_hours')),
#         'Soil_pH': float(form.get('soil_ph')),
#         'Soil_Moisture_Level': float(form.get('soil_moisture')),
#         'Water_Usage(cubic meters)': float(form.get('water_usage', 500)),
#         'Nutrient_Content': float(form.get('nutrient_content', 50)),
#         'Crop_Type_' + form.get('crop_type'): 1,
#         'Irrigation_Type_' + form.get('irrigation_type'): 1,
#         'Soil_Type_' + form.get('soil_type'): 1,
#         'Season_' + form.get('season'): 1
#     }

#     all_columns = model.feature_names_in_
#     input_data = {col: features.get(col, 0) for col in all_columns}
#     df = pd.DataFrame([input_data])
#     predicted_yield = model.predict(df)[0]

#     suggestions = get_yield_improvement_suggestions(df, predicted_yield)

#     # return render_template('result.html', prediction=round(predicted_yield, 2), suggestions=suggestions)
#     return render_template("result.html", prediction=round(predicted_yield, 2), suggestions=[
#     {
#         'new_yield': 12.4,
#         'improvement_percent': 17.6,
#         'changed_features': ['Soil Type: Loamy', 'Irrigation: Drip', 'Water Usage: 200 m³']
#     },
#     {
#         'new_yield': 13.1,
#         'improvement_percent': 23.4,
#         'changed_features': ['Increase Nutrients', 'Rainfall: +20 mm']
#     },
#     {
#         'new_yield': 14.3,
#         'improvement_percent': 34.6,
#         'changed_features': ['Sunlight Hours: 8 → 10', 'Soil pH: 6.0']
#     }
# ])

# # ----------------- Suggestions -----------------
# def get_yield_improvement_suggestions(df, original_yield):
#     suggestions = []

#     # Try different soil types
#     for soil in ['Loamy', 'Clay', 'Sandy']:
#         soil_col = f'Soil_Type_{soil}'
#         if soil_col in df.columns and df.at[0, soil_col] == 0:
#             df_mod = df.copy()
#             for col in df.columns:
#                 if col.startswith("Soil_Type_"):
#                     df_mod.at[0, col] = 0
#             df_mod.at[0, soil_col] = 1
#             new_yield = model.predict(df_mod)[0]
#             delta = new_yield - original_yield
#             if delta > 0.3:
#                 suggestions.append({
#                     'feature': f"Soil Type → {soil}",
#                     'new_yield': round(new_yield, 2),
#                     'improvement_percent': round((delta / original_yield) * 100, 1)
#                 })

#     # Try different irrigation types
#     for method in ['Drip', 'Sprinkler', 'Flood']:
#         irrigation_col = f'Irrigation_Type_{method}'
#         if irrigation_col in df.columns and df.at[0, irrigation_col] == 0:
#             df_mod = df.copy()
#             for col in df.columns:
#                 if col.startswith("Irrigation_Type_"):
#                     df_mod.at[0, col] = 0
#             df_mod.at[0, irrigation_col] = 1
#             new_yield = model.predict(df_mod)[0]
#             delta = new_yield - original_yield
#             if delta > 0.3:
#                 suggestions.append({
#                     'feature': f"Irrigation → {method}",
#                     'new_yield': round(new_yield, 2),
#                     'improvement_percent': round((delta / original_yield) * 100, 1)
#                 })

#     # Try increasing soil moisture
#     df_mod = df.copy()
#     df_mod.at[0, 'Soil_Moisture_Level'] += 10
#     new_yield = model.predict(df_mod)[0]
#     delta = new_yield - original_yield
#     if delta > 0.3:
#         suggestions.append({
#             'feature': "Soil Moisture +10%",
#             'new_yield': round(new_yield, 2),
#             'improvement_percent': round((delta / original_yield) * 100, 1)
#         })

#     return suggestions[:3]

# 
# if __name__ == '__main__':
#     app.run(debug=True)
# from flask import Flask, render_template, request, jsonify
# import pandas as pd

# app = Flask(__name__)

# # Load the data
# def load_data():
#     try:
#         data = pd.read_csv('attached_assets/crop_datanew.csv')
#         if 'Soil_Type' in data.columns and 'Crop_Type' in data.columns and 'Irrigation_Type' in data.columns:
#             return data
#     except Exception as e:
#         print(f"Could not load enhanced dataset: {e}")
        
#     try:
#         data = pd.read_csv('attached_assets/crop_data.csv')
#         return data
#     except Exception as e:
#         print(f"Failed to load any dataset: {e}")
#         return None

# # Get unique values
# def get_unique_values(data):
#     if data is None:
#         return [], [], []
        
#     soil_types = sorted(data['Soil_Type'].unique())
#     crop_types = sorted(data['Crop_Type'].unique())
#     irrigation_types = sorted(data['Irrigation_Type'].unique())
    
#     return soil_types, crop_types, irrigation_types

# # Filter data
# def filter_data(data, soil_type, crop_type, irrigation_type):
#     filtered_data = data.copy()
#     if soil_type != "All":
#         filtered_data = filtered_data[filtered_data['Soil_Type'] == soil_type]
#     if crop_type != "All":
#         filtered_data = filtered_data[filtered_data['Crop_Type'] == crop_type]
#     if irrigation_type != "All":
#         filtered_data = filtered_data[filtered_data['Irrigation_Type'] == irrigation_type]
#     return filtered_data

# # Calculate average values
# def get_average_values(filtered_data):
#     if filtered_data.empty:
#         return None
    
#     avg_values = {
#         'yield': filtered_data['Yield(tons)'].mean(),
#         'water_usage': filtered_data['Water_Usage(cubic meters)'].mean(),
#         'temperature': filtered_data['Temperature(°C)'].mean(),
#         'humidity': filtered_data['Humidity(%)'].mean(),
#     }
#     if 'Nutrient_Content' in filtered_data.columns:
#         avg_values['nutrient_content'] = filtered_data['Nutrient_Content'].mean()
#     if 'Soil_pH' in filtered_data.columns:
#         avg_values['soil_ph'] = filtered_data['Soil_pH'].mean()
#     if 'Soil_Moisture_Level' in filtered_data.columns:
#         avg_values['soil_moisture'] = filtered_data['Soil_Moisture_Level'].mean()
#     return avg_values

# # Get fertilizer recommendations
# def get_fertilizer_recommendations(crop_type):
#     organic_options = {
#         'Barley': ['Vermicompost', 'Cow dung compost'],
#         'Corn': ['Composted poultry manure', 'Organic corn fertilizer'],
#         'Rice': ['Rice bran compost', 'Azolla organic fertilizer'],
#         'Soybean': ['Rhizobium-enriched compost', 'Organic legume fertilizer'],
#         'Wheat': ['Organic wheat formula', 'Composted farmyard manure']
#     }
#     homemade_options = {
#         'Barley': ['Kitchen waste compost', 'Compost tea'],
#         'Corn': ['Banana peel fertilizer', 'Coffee grounds mix'],
#         'Rice': ['Rice water fertilizer', 'Fermented plant juice'],
#         'Soybean': ['Compost tea with molasses', 'Wood ash solution'],
#         'Wheat': ['Compost with aged manure', 'Alfalfa tea']
#     }
    
#     ready_made = organic_options.get(crop_type, ['Vermicompost', 'Cow dung compost'])[:2]
#     homemade = homemade_options.get(crop_type, ['Kitchen waste compost', 'Compost tea'])[:2]
    
#     return {
#         'ready_made': ready_made,
#         'homemade': homemade
#     }

# # Calculate suitability score
# def calculate_suitability_score(data, selected_soil_type, selected_crop_type, selected_irrigation_type, avg_values):
#     suitability_score = 0
#     if 'yield' in avg_values:
#         crop_avg_yield = data[data['Crop_Type'] == selected_crop_type]['Yield(tons)'].mean() if selected_crop_type != "All" else data['Yield(tons)'].mean()
#         if avg_values['yield'] > crop_avg_yield:
#             suitability_score += 50
#         else:
#             suitability_score += 30
            
#     if selected_soil_type != "All" and selected_crop_type != "All":
#         best_soil = data[data['Crop_Type'] == selected_crop_type].groupby('Soil_Type')['Yield(tons)'].mean().idxmax()
#         if selected_soil_type == best_soil:
#             suitability_score += 50
#         else:
#             suitability_score += 20
            
#     if selected_irrigation_type != "All" and selected_crop_type != "All":
#         best_irrigation = data[data['Crop_Type'] == selected_crop_type].groupby('Irrigation_Type')['Yield(tons)'].mean().idxmax()
#         if selected_irrigation_type == best_irrigation:
#             suitability_score += 50
#         else:
#             suitability_score += 30
            
#     suitability_score = max(suitability_score, 50)
#     suitability_score = min(suitability_score, 100)
#     return suitability_score

# # Suggest fertilizer quantity
# def suggest_fertilizer_quantity(crop_type):
#     quantities = {
#         'Wheat': '5 tons/acre',
#         'Rice': '4 tons/acre',
#         'Corn': '5-6 tons/acre',
#         'Barley': '4 tons/acre',
#         'Soybean': '3-4 tons/acre'
#     }
#     return quantities.get(crop_type, '5 tons/acre')

# # Calculate soil health score
# def calculate_soil_health(avg_values):
#     score = 50
#     if 'soil_ph' in avg_values:
#         if 6.0 <= avg_values['soil_ph'] <= 7.5:
#             score += 25
#         else:
#             score += 10
#     if 'soil_moisture' in avg_values:
#         if 20 <= avg_values['soil_moisture'] <= 40:
#             score += 25
#         else:
#             score += 10
#     return min(score, 100)

# # Detect soil defects and suggest solutions
# def get_soil_defects_and_solutions(avg_values):
#     defects = []
#     solutions = []

#     if 'soil_ph' in avg_values:
#         if avg_values['soil_ph'] < 6.0:
#             defects.append("Soil is too acidic.")
#             solutions.append("Apply lime powder and add organic compost.")
#         elif avg_values['soil_ph'] > 7.5:
#             defects.append("Soil is too alkaline.")
#             solutions.append("Add organic matter and sulfur to lower pH.")

#     if 'soil_moisture' in avg_values:
#         if avg_values['soil_moisture'] < 20:
#             defects.append("Soil moisture is too low (dry soil).")
#             solutions.append("Improve irrigation system and apply mulch.")
#         elif avg_values['soil_moisture'] > 40:
#             defects.append("Soil moisture is too high (waterlogged soil).")
#             solutions.append("Improve drainage and reduce overwatering.")

#     return defects, solutions

# # Load data at startup
# data = load_data()
# soil_types, crop_types, irrigation_types = get_unique_values(data)

# @app.route('/')
# def index():
#     return render_template('fertilizer.html')

# @app.route('/get_options')
# def get_options():
#     return jsonify({
#         'soil_types': soil_types,
#         'crop_types': crop_types,
#         'irrigation_types': irrigation_types
#     })

# @app.route('/get_recommendations', methods=['POST'])
# def get_recommendations():
#     request_data = request.json
#     soil_type = request_data.get('soil_type')
#     crop_type = request_data.get('crop_type')
#     irrigation_type = request_data.get('irrigation_type')
    
#     filtered_data = filter_data(data, soil_type, crop_type, irrigation_type)
    
#     if filtered_data.empty:
#         return jsonify({'error': 'No data available for this combination. Please try different options.'})
    
#     avg_values = get_average_values(filtered_data)
#     recommendations = get_fertilizer_recommendations(crop_type)
#     suitability_score = calculate_suitability_score(data, soil_type, crop_type, irrigation_type, avg_values)
#     fertilizer_quantity = suggest_fertilizer_quantity(crop_type)
#     soil_health_score = calculate_soil_health(avg_values) if avg_values else None
#     soil_defects, soil_solutions = get_soil_defects_and_solutions(avg_values) if avg_values else ([], [])

#     return jsonify({
#         'crop_type': crop_type,
#         'suitability_score': suitability_score,
#         'recommendations': recommendations,
#         'fertilizer_quantity': fertilizer_quantity,
#         'soil_health_score': soil_health_score,
#         'soil_defects': soil_defects,
#         'soil_solutions': soil_solutions
#     })

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)




#################################################################################
from flask import Flask, request, render_template, jsonify
import pandas as pd
import pickle
import os

app = Flask(__name__)

# Load the trained model
model = pickle.load(open('models/crop_yield_model_lr.pkl', 'rb'))

# ----------------- Page Routes -----------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather')
def weather_page():
    return render_template('weather.html')

@app.route('/rainfall_sunlight')
def rainfall_sunlight_page():
    return render_template('rainfall_sunlight.html')

@app.route('/soil')
def soil_page():
    return render_template('soil.html')

@app.route('/result')
def result_page():
    return render_template('result.html')

# ----------------- Weather API -----------------
@app.route('/api/weather')
def api_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Latitude and Longitude required'}), 400

    # Replace this part with your real weather API call
    simulated_data = {
        'temperature': 28.3,
        'humidity': 65.2
    }
    return jsonify(simulated_data)

# ----------------- Prediction Route -----------------
@app.route('/predict', methods=['POST'])
def predict():
    form = request.form

    features = {
        'Farm_Area(acres)': float(form.get('farm_area')),
        'Temperature(°C)': float(form.get('temperature')),
        'Humidity(%)': float(form.get('humidity')),
        'Rainfall(mm)': float(form.get('rainfall')),
        'Sunlight_Hours': float(form.get('sunlight_hours')),
        'Soil_pH': float(form.get('soil_ph')),
        'Soil_Moisture_Level': float(form.get('soil_moisture')),
        'Water_Usage(cubic meters)': float(form.get('water_usage', 500)),
        'Nutrient_Content': float(form.get('nutrient_content', 50)),
        'Crop_Type_' + form.get('crop_type'): 1,
        'Irrigation_Type_' + form.get('irrigation_type'): 1,
        'Soil_Type_' + form.get('soil_type'): 1,
        'Season_' + form.get('season'): 1
    }

    all_columns = model.feature_names_in_
    input_data = {col: features.get(col, 0) for col in all_columns}
    df = pd.DataFrame([input_data])
    predicted_yield = model.predict(df)[0]

    # You chose to keep this exact yield output and suggestion format
    return render_template("result.html", prediction=round(predicted_yield, 2), suggestions=[
        {
            'new_yield': 12.4,
            'improvement_percent': 17.6,
            'changed_features': ['Soil Type: Loamy', 'Irrigation: Drip', 'Water Usage: 200 m³']
        },
        {
            'new_yield': 13.1,
            'improvement_percent': 23.4,
            'changed_features': ['Increase Nutrients', 'Rainfall: +20 mm']
        },
        {
            'new_yield': 14.3,
            'improvement_percent': 34.6,
            'changed_features': ['Sunlight Hours: 8 → 10', 'Soil pH: 6.0']
        }
    ])

# ----------------- Yield Improvement Suggestions (Optional Use) -----------------
def get_yield_improvement_suggestions(df, original_yield):
    suggestions = []

    # Soil types
    for soil in ['Loamy', 'Clay', 'Sandy']:
        soil_col = f'Soil_Type_{soil}'
        if soil_col in df.columns and df.at[0, soil_col] == 0:
            df_mod = df.copy()
            for col in df.columns:
                if col.startswith("Soil_Type_"):
                    df_mod.at[0, col] = 0
            df_mod.at[0, soil_col] = 1
            new_yield = model.predict(df_mod)[0]
            delta = new_yield - original_yield
            if delta > 0.3:
                suggestions.append({
                    'feature': f"Soil Type → {soil}",
                    'new_yield': round(new_yield, 2),
                    'improvement_percent': round((delta / original_yield) * 100, 1)
                })

    # Irrigation types
    for method in ['Drip', 'Sprinkler', 'Flood']:
        irrigation_col = f'Irrigation_Type_{method}'
        if irrigation_col in df.columns and df.at[0, irrigation_col] == 0:
            df_mod = df.copy()
            for col in df.columns:
                if col.startswith("Irrigation_Type_"):
                    df_mod.at[0, col] = 0
            df_mod.at[0, irrigation_col] = 1
            new_yield = model.predict(df_mod)[0]
            delta = new_yield - original_yield
            if delta > 0.3:
                suggestions.append({
                    'feature': f"Irrigation → {method}",
                    'new_yield': round(new_yield, 2),
                    'improvement_percent': round((delta / original_yield) * 100, 1)
                })

    # Soil moisture +10%
    df_mod = df.copy()
    df_mod.at[0, 'Soil_Moisture_Level'] += 10
    new_yield = model.predict(df_mod)[0]
    delta = new_yield - original_yield
    if delta > 0.3:
        suggestions.append({
            'feature': "Soil Moisture +10%",
            'new_yield': round(new_yield, 2),
            'improvement_percent': round((delta / original_yield) * 100, 1)
        })

    # Nutrient Content +20
    df_mod = df.copy()
    df_mod.at[0, 'Nutrient_Content'] += 20
    new_yield = model.predict(df_mod)[0]
    delta = new_yield - original_yield
    if delta > 0.3:
        suggestions.append({
            'feature': "Nutrient Content +20",
            'new_yield': round(new_yield, 2),
            'improvement_percent': round((delta / original_yield) * 100, 1)
        })

    # Rainfall +20 mm
    df_mod = df.copy()
    df_mod.at[0, 'Rainfall(mm)'] += 20
    new_yield = model.predict(df_mod)[0]
    delta = new_yield - original_yield
    if delta > 0.3:
        suggestions.append({
            'feature': "Rainfall +20mm",
            'new_yield': round(new_yield, 2),
            'improvement_percent': round((delta / original_yield) * 100, 1)
        })

    # Sunlight +2 hours
    df_mod = df.copy()
    df_mod.at[0, 'Sunlight_Hours'] += 2
    new_yield = model.predict(df_mod)[0]
    delta = new_yield - original_yield
    if delta > 0.3:
        suggestions.append({
            'feature': "Sunlight Hours +2",
            'new_yield': round(new_yield, 2),
            'improvement_percent': round((delta / original_yield) * 100, 1)
        })

    # Soil pH adjustment to 6.0
    df_mod = df.copy()
    df_mod.at[0, 'Soil_pH'] = 6.0
    new_yield = model.predict(df_mod)[0]
    delta = new_yield - original_yield
    if delta > 0.3:
        suggestions.append({
            'feature': "Soil pH → 6.0",
            'new_yield': round(new_yield, 2),
            'improvement_percent': round((delta / original_yield) * 100, 1)
        })

    return suggestions


# Load the data
def load_data():
    try:
        data = pd.read_csv('attached_assets/crop_datanew.csv')
        if 'Soil_Type' in data.columns and 'Crop_Type' in data.columns and 'Irrigation_Type' in data.columns:
            return data
    except Exception as e:
        print(f"Could not load enhanced dataset: {e}")
        
    try:
        data = pd.read_csv('attached_assets/crop_data.csv')
        return data
    except Exception as e:
        print(f"Failed to load any dataset: {e}")
        return None

# Get unique values
def get_unique_values(data):
    if data is None:
        return [], [], []
        
    soil_types = sorted(data['Soil_Type'].unique())
    crop_types = sorted(data['Crop_Type'].unique())
    irrigation_types = sorted(data['Irrigation_Type'].unique())
    
    return soil_types, crop_types, irrigation_types

# Filter data
def filter_data(data, soil_type, crop_type, irrigation_type):
    filtered_data = data.copy()
    if soil_type != "All":
        filtered_data = filtered_data[filtered_data['Soil_Type'] == soil_type]
    if crop_type != "All":
        filtered_data = filtered_data[filtered_data['Crop_Type'] == crop_type]
    if irrigation_type != "All":
        filtered_data = filtered_data[filtered_data['Irrigation_Type'] == irrigation_type]
    return filtered_data

# Calculate average values
def get_average_values(filtered_data):
    if filtered_data.empty:
        return None
    
    avg_values = {
        'yield': filtered_data['Yield(tons)'].mean(),
        'water_usage': filtered_data['Water_Usage(cubic meters)'].mean(),
        'temperature': filtered_data['Temperature(°C)'].mean(),
        'humidity': filtered_data['Humidity(%)'].mean(),
    }
    if 'Nutrient_Content' in filtered_data.columns:
        avg_values['nutrient_content'] = filtered_data['Nutrient_Content'].mean()
    if 'Soil_pH' in filtered_data.columns:
        avg_values['soil_ph'] = filtered_data['Soil_pH'].mean()
    if 'Soil_Moisture_Level' in filtered_data.columns:
        avg_values['soil_moisture'] = filtered_data['Soil_Moisture_Level'].mean()
    return avg_values

# Get fertilizer recommendations
def get_fertilizer_recommendations(crop_type):
    organic_options = {
        'Barley': ['Vermicompost', 'Cow dung compost'],
        'Corn': ['Composted poultry manure', 'Organic corn fertilizer'],
        'Rice': ['Rice bran compost', 'Azolla organic fertilizer'],
        'Soybean': ['Rhizobium-enriched compost', 'Organic legume fertilizer'],
        'Wheat': ['Organic wheat formula', 'Composted farmyard manure']
    }
    homemade_options = {
        'Barley': ['Kitchen waste compost', 'Compost tea'],
        'Corn': ['Banana peel fertilizer', 'Coffee grounds mix'],
        'Rice': ['Rice water fertilizer', 'Fermented plant juice'],
        'Soybean': ['Compost tea with molasses', 'Wood ash solution'],
        'Wheat': ['Compost with aged manure', 'Alfalfa tea']
    }
    
    ready_made = organic_options.get(crop_type, ['Vermicompost', 'Cow dung compost'])[:2]
    homemade = homemade_options.get(crop_type, ['Kitchen waste compost', 'Compost tea'])[:2]
    
    return {
        'ready_made': ready_made,
        'homemade': homemade
    }

# Calculate suitability score
def calculate_suitability_score(data, selected_soil_type, selected_crop_type, selected_irrigation_type, avg_values):
    suitability_score = 0
    if 'yield' in avg_values:
        crop_avg_yield = data[data['Crop_Type'] == selected_crop_type]['Yield(tons)'].mean() if selected_crop_type != "All" else data['Yield(tons)'].mean()
        if avg_values['yield'] > crop_avg_yield:
            suitability_score += 50
        else:
            suitability_score += 30
            
    if selected_soil_type != "All" and selected_crop_type != "All":
        best_soil = data[data['Crop_Type'] == selected_crop_type].groupby('Soil_Type')['Yield(tons)'].mean().idxmax()
        if selected_soil_type == best_soil:
            suitability_score += 50
        else:
            suitability_score += 20
            
    if selected_irrigation_type != "All" and selected_crop_type != "All":
        best_irrigation = data[data['Crop_Type'] == selected_crop_type].groupby('Irrigation_Type')['Yield(tons)'].mean().idxmax()
        if selected_irrigation_type == best_irrigation:
            suitability_score += 50
        else:
            suitability_score += 30
            
    suitability_score = max(suitability_score, 50)
    suitability_score = min(suitability_score, 100)
    return suitability_score

# Suggest fertilizer quantity
def suggest_fertilizer_quantity(crop_type):
    quantities = {
        'Wheat': '5 tons/acre',
        'Rice': '4 tons/acre',
        'Corn': '5-6 tons/acre',
        'Barley': '4 tons/acre',
        'Soybean': '3-4 tons/acre'
    }
    return quantities.get(crop_type, '5 tons/acre')

# Calculate soil health score
def calculate_soil_health(avg_values):
    score = 50
    if 'soil_ph' in avg_values:
        if 6.0 <= avg_values['soil_ph'] <= 7.5:
            score += 25
        else:
            score += 10
    if 'soil_moisture' in avg_values:
        if 20 <= avg_values['soil_moisture'] <= 40:
            score += 25
        else:
            score += 10
    return min(score, 100)

# Detect soil defects and suggest solutions
def get_soil_defects_and_solutions(avg_values):
    defects = []
    solutions = []

    if 'soil_ph' in avg_values:
        if avg_values['soil_ph'] < 6.0:
            defects.append("Soil is too acidic.")
            solutions.append("Apply lime powder and add organic compost.")
        elif avg_values['soil_ph'] > 7.5:
            defects.append("Soil is too alkaline.")
            solutions.append("Add organic matter and sulfur to lower pH.")

    if 'soil_moisture' in avg_values:
        if avg_values['soil_moisture'] < 20:
            defects.append("Soil moisture is too low (dry soil).")
            solutions.append("Improve irrigation system and apply mulch.")
        elif avg_values['soil_moisture'] > 40:
            defects.append("Soil moisture is too high (waterlogged soil).")
            solutions.append("Improve drainage and reduce overwatering.")

    return defects, solutions

# Load data at startup
data = load_data()
soil_types, crop_types, irrigation_types = get_unique_values(data)

@app.route('/')
def index():
    return render_template('fertilizer.html')

@app.route('/get_options')
def get_options():
    return jsonify({
        'soil_types': soil_types,
        'crop_types': crop_types,
        'irrigation_types': irrigation_types
    })

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    request_data = request.json
    soil_type = request_data.get('soil_type')
    crop_type = request_data.get('crop_type')
    irrigation_type = request_data.get('irrigation_type')
    
    filtered_data = filter_data(data, soil_type, crop_type, irrigation_type)
    
    if filtered_data.empty:
        return jsonify({'error': 'No data available for this combination. Please try different options.'})
    
    avg_values = get_average_values(filtered_data)
    recommendations = get_fertilizer_recommendations(crop_type)
    suitability_score = calculate_suitability_score(data, soil_type, crop_type, irrigation_type, avg_values)
    fertilizer_quantity = suggest_fertilizer_quantity(crop_type)
    soil_health_score = calculate_soil_health(avg_values) if avg_values else None
    soil_defects, soil_solutions = get_soil_defects_and_solutions(avg_values) if avg_values else ([], [])

    return jsonify({
        'crop_type': crop_type,
        'suitability_score': suitability_score,
        'recommendations': recommendations,
        'fertilizer_quantity': fertilizer_quantity,
        'soil_health_score': soil_health_score,
        'soil_defects': soil_defects,
        'soil_solutions': soil_solutions
    })
@app.route('/fertilizer')
def fertilizer():
    return render_template('fertilizer.html')


# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)



app = Flask(__name__)

