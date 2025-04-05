import os
import json

apps = {
    "main-app": "Trusure Median",
    "anydesk": "Anydesk Tool",
    "plugin": "Utility Plugin"
}

base_url = "https://raw.githubusercontent.com/median0533/trusure-median-apps/main"

# Safely load existing updates.json
updates = {}
if os.path.exists("updates.json"):
    try:
        with open("updates.json", "r") as f:
            content = f.read().strip()
            if content:
                updates = json.loads(content)
    except Exception as e:
        print("⚠️ Could not parse updates.json, starting fresh.")
        updates = {}

# Loop through each app folder
for folder, display_name in apps.items():
    app_path = os.path.join(folder)
    if not os.path.isdir(app_path):
        continue

    versions = sorted(os.listdir(app_path), reverse=True)

    if not versions:
        continue

    latest_version = versions[0]

    # Check if already up-to-date
    if folder in updates and updates[folder].get("latest_version") == latest_version:
        continue

    files = os.listdir(os.path.join(folder, latest_version))
    apk_file = next((f for f in files if f.endswith(".apk")), None)

    if not apk_file:
        continue

    # Update the JSON entry
    updates[folder] = {
        "name": display_name,
        "latest_version": latest_version,
        "changelog": f"Auto-added {latest_version}",
        "apk_url": f"{base_url}/{folder}/{latest_version}/{apk_file}"
    }

# Save back
with open("updates.json", "w") as f:
    json.dump(updates, f, indent=2)

print("✅ updates.json updated.")
