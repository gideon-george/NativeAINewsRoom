import time, subprocess
from pyngrok import ngrok

# Start the Streamlit app
process = subprocess.Popen(["streamlit", "run", "app.py"])

# Wait for the app to start
time.sleep(5)

# Create ngrok tunnel
public_url = ngrok.connect(8501)
print("Streamlit app is live at:", public_url)

# Keep the script running
while True:
    time.sleep(10)
