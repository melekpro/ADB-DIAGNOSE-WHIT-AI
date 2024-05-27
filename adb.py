import subprocess
import time

# Install spaCy and download English language model
subprocess.run("pip install spacy", shell=True)
subprocess.run("python -m spacy download en_core_web_sm", shell=True)

# Install NLTK and download required data
subprocess.run("pip install nltk", shell=True)
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

# Load English tokenizer, tagger, parser and NER
import spacy
from nltk.tokenize import word_tokenize
from nltk import pos_tag

nlp = spacy.load("en_core_web_sm")

def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    return result.stdout.decode().strip()

def get_device_info():
    print("Fetching device information... Please wait.")
    time.sleep(1)
    
    device_model = run_command("adb shell getprop ro.product.model")
    android_version = run_command("adb shell getprop ro.build.version.release")
    serial_number = run_command("adb shell getprop ro.serialno")
    battery_info = run_command("adb shell dumpsys battery")
    memory_info = run_command("adb shell dumpsys meminfo")
    installed_apps = run_command("adb shell pm list packages")
    sensor_info = run_command("adb shell dumpsys sensorservice")
    screen_info = run_command("adb shell dumpsys display")

    return {
        "Device Model": device_model,
        "Android Version": android_version,
        "Serial Number": serial_number,
        "Battery Info": battery_info,
        "Memory Info": memory_info,
        "Installed Apps": installed_apps,
        "Sensor Info": sensor_info,
        "Screen Info": screen_info
    }

def analyze_text_with_spacy(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def analyze_text_with_nltk(text):
    tokens = word_tokenize(text)
    tagged_tokens = pos_tag(tokens)
    return tagged_tokens

def display_info(info):
    for key, value in info.items():
        print(f"{key}: {value}")

def simplify_battery_info(battery_info):
    for line in battery_info.splitlines():
        if "level" in line:
            level = line.split(": ")[1]
        if "health" in line:
            health = line.split(": ")[1]
        if "status" in line:
            status = line.split(": ")[1]
    return f"Battery Level: {level}, Health: {health}, Status: {status}"

print("Device Information:")
device_info = get_device_info()
display_info(device_info)

# Simplify and display battery information
print("\nSimplified Battery Information:")
simplified_battery_info = simplify_battery_info(device_info["Battery Info"])
print(simplified_battery_info)

# Analyze device information using spaCy
text_to_analyze = f"{device_info['Device Model']} {device_info['Android Version']} {device_info['Serial Number']}"
analyzed_info_spacy = analyze_text_with_spacy(text_to_analyze)

print("\nAnalyzed Information using spaCy:")
for entity, label in analyzed_info_spacy:
    print(f"{label}: {entity}")

# Analyze device information using NLTK
analyzed_info_nltk = analyze_text_with_nltk(text_to_analyze)

print("\nAnalyzed Information using NLTK:")
for token, pos in analyzed_info_nltk:
    print(f"{pos}: {token}")

print("\nAdditional Information:")
for key in ["Memory Info", "Installed Apps", "Sensor Info", "Screen Info"]:
    print(f"\n{key}:\n{device_info[key]}")
