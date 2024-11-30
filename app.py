import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def fetch_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=en"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        description = data["weather"][0]["description"].lower()
        main_weather = data["weather"][0]["main"].lower()
        temperature = data["main"]["temp"]
        wind_speed_mps = data["wind"]["speed"]  # Wind speed in m/s
        wind_speed_kmh = wind_speed_mps * 3.6  # Convert m/s to km/h

        adverse_conditions = ["rain", "thunderstorm", "drizzle", "snow"]
        is_adverse = any(
            condition in description or condition in main_weather
            for condition in adverse_conditions
        )

        message = (
            f"Today's weather in {city}:\n\n"
            f"Description: {description.capitalize()}\n"
            f"Temperature: {temperature}°C\n"
            f"Wind Speed: {wind_speed_kmh:.1f} km/h\n"
        )

        if is_adverse or wind_speed_kmh > 25:
            message += "\nToday is not ideal for a bike ride."
        else:
            message += "\nIt's a good day to ride your bike!"

        return message
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"


def send_email(sender_email, password, recipient_email, message):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)

        subject = "Should bike today?"
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except smtplib.SMTPException as e:
        print(f"An error occurred while sending the email: {e}")


def main():
    api_key = os.getenv("API_KEY")
    city = os.getenv("CITY")
    sender_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    recipient_email = os.getenv("RECIPIENT_EMAIL")

    weather_message = fetch_weather(api_key, city)
    send_email(sender_email, password, recipient_email, weather_message)


if __name__ == "__main__":
    main()
