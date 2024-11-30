# 🚴‍♂️ Should bike today? 

**Should Bike Today?** is a Python application that helps you decide whether it's a good day to go biking based on the weather conditions in your city. The app uses the [OpenWeatherMap API](https://openweathermap.org/api) to fetch real-time weather data and sends you a personalized email with the recommendation.

## 📂 Repository Structure
- `app.py`: main application code.
- `requirements.txt`: list of dependencies required to run the app.
- `.env.example`: template for the environment variables file.
- `aws_lambda/`: a version of the code tailored to run as an AWS Lambda function.

## 💡Features
- Fetches real-time weather data from OpenWeatherMap API.
- Sends a weather summary and biking recommendation via email.

## 🚀 Automation with AWS

The `aws_lambda/` folder contains code ready to deploy on AWS Lambda. By integrating it with an *EventBridge Rule*, you can schedule the function to run daily at a specific time, automating the email delivery process.