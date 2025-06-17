import os
import shutil
import sys

env_example = ".env.example"
env_file = ".env"

if not os.path.exists(env_file):
    if os.path.exists(env_example):
        shutil.copy(env_example, env_file)
        print(f"Copied {env_example} to {env_file}")
    else:
        print(f"{env_example} does not exist.")
else:
    print(f"{env_file} already exists.")

    plist_template = "com.user.macbattery.plist.temlpate"
    plist_file = "com.user.macbattery.plist"

    if os.path.exists(plist_template):
        with open(plist_template, "r") as f:
            plist_content = f.read()

        venv_python = os.path.join("venv", "bin", "python3")
        if os.path.exists(venv_python):
            python_path = os.path.abspath(venv_python)
        else:
            python_path = sys.executable

        mac_battery_path = os.path.abspath("mac-battery.py")

        plist_content = plist_content.replace("{python}", python_path)
        plist_content = plist_content.replace("{mac-battery}", mac_battery_path)

        with open(plist_file, "w") as f:
            f.write(plist_content)
        print(f"Created {plist_file} from {plist_template}")
        
        launch_agents_dir = os.path.expanduser("~/Library/LaunchAgents")
        if not os.path.exists(launch_agents_dir):
            os.makedirs(launch_agents_dir)
        dest_path = os.path.join(launch_agents_dir, plist_file)
        shutil.move(plist_file, dest_path)
        print(f"Moved {plist_file} to {dest_path}")
    else:
        print(f"{plist_template} does not exist.")