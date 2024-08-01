import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Load the data from CSV file
data = pd.read_csv('./高邮/6-7/svr/weekend_train_data.csv')

# Parse the time column to extract the hour
data['time'] = pd.to_datetime(data['time'], format='%H:%M:%S').dt.hour

# Prepare to store the feature importances
feature_importances = []

# Prepare to store the actual and predicted values for comparison
actual_vs_predicted = []

# Loop over each hour
unique_times = data['time'].unique()
for hour in unique_times:
    # Select data for the current hour
    hourly_data = data[data['time'] == hour]
    
    # Prepare features and target
    X = hourly_data[['total_up', 'total_down']]
    y_target = hourly_data['total_toll']
    
    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train Random Forest model
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_scaled, y_target)
    
    # Get feature importances
    importances = rf.feature_importances_
    
    # Store the importances with the corresponding hour
    feature_importances.append({'hour': hour, 'importance_total_up': importances[0], 'importance_total_down': importances[1]})
    
    # Predict the target values
    y_pred = rf.predict(X_scaled)
    
    # Store actual and predicted values for plotting
    actual_vs_predicted.append({'hour': hour, 'actual': y_target.values, 'predicted': y_pred})

# Convert feature importances to DataFrame for analysis
feature_importances_df = pd.DataFrame(feature_importances)

# Plot the feature importances over time
plt.figure(figsize=(14, 7))
plt.plot(feature_importances_df['hour'], feature_importances_df['importance_total_up'], label='Importance of total_up', marker='o')
plt.plot(feature_importances_df['hour'], feature_importances_df['importance_total_down'], label='Importance of total_down', marker='o')
plt.xlabel('Hour of the Day')
plt.ylabel('Feature Importance')
plt.title('Pattern of Feature Importances over Different Times of the Day')
plt.legend()
plt.grid(True)
plt.savefig('./Random Forest/weekend results/feature_importances.png')
plt.show()
plt.close()

# Plot the actual vs. predicted values for each hour
for entry in actual_vs_predicted:
    hour = entry['hour']
    actual = entry['actual']
    predicted = entry['predicted']
    
    plt.figure(figsize=(10, 5))
    plt.plot(actual, label='Actual', marker='o')
    plt.plot(predicted, label='Predicted', marker='o')
    plt.xlabel('Sample')
    plt.ylabel('Total Toll')
    plt.title(f'Actual vs Predicted Total Toll at Hour {hour}')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'./Random Forest/weekend results/{hour}.png')
    plt.close()
    # plt.show()
