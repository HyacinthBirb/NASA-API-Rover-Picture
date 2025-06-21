import requests
import os
import datetime
import shutil
import sys

print("\033[96m" + """
BBBBB   III  RRRRR   BBBBB
B   B    I   R   R   B   B
B   B    I   R   R   B   B
BBBBB    I   RRRRR   BBBBB
B   B    I   R R     B   B
B   B    I   R  RR   B   B
BBBBB   III  R   R   BBBBB
""" + "\033[0m")

print ("--------------------------------------------------------")

print("\033[91m" + """
MM   MM   AA   RRRR   SSS    RRRR   OOO   V   V  EEEE  RRRR       AAA   PPPP   III
M M M M  A  A  R   R S       R   R O   O  V   V  E     R   R     A   A  P   P   I 
M  M  M AAAAA  RRRR   SSS    RRRR  O   O  V   V  EEEE  RRRR     AAAAAAA PPPP    I 
M     M A   A  R  R      S   R  R  O   O   V V   E     R  R    A     A  P       I 
M     M A   A  R   R SSSS    R   R  OOO     V    EEEE  R   R  A       A P      III
""" + "\033[0m")

print ("--------------------------------------------------------")
print ("Mars Rover API Example")
print ("This example uses the NASA Mars Rover Photos API to fetch photos from a specific rover and camera.")
print ("Personal Experiment, BIRB")
print ("Version 1.0")
print ("--------------------------------------------------------")
print ("Commands:")
print ("SOL Photos: Bring up all photos if you choose option 3")
print ("Menu: Return to the main menu at any time")
print ("Exit Prog: Exit the program at any time")
print ("Download: Download all photos or a specific photo")
print ("--------------------------------------------------------")

print ("\033[94mIn case you want to exit to the option menu, type menu at any time.\033[0m")

API_KEY = "RBu1qfRVoUn44hScU2CgS7AtWDwtKF38ka1c8EG0"  # Private NASA API key
ROVER_NAME = "curiosity"
PAGE = 1

CAMERA_INFO = {
    "FHAZ": "Front Hazard Avoidance Camera",
    "RHAZ": "Rear Hazard Avoidance Camera",
    "MAST": "Mast Camera",
    "CHEMCAM": "Chemistry and Camera Complex",
    "MAHLI": "Mars Hand Lens Imager",
    "MARDI": "Mars Descent Imager",
    "NAVCAM": "Navigation Camera",
    "PANCAM": "Panoramic Camera",
    "MINITES": "Miniature Thermal Emission Spectrometer (Mini-TES)"
}

def print_camera_options():
    print("\nAvailable cameras:")
    for cam, desc in CAMERA_INFO.items():
        print(f"  {cam}: {desc}")
    print('  ALL: All cameras\n')

is_private_api = API_KEY == "RBu1qfRVoUn44hScU2CgS7AtWDwtKF38ka1c8EG0"
print(f"\033[91mDEBUG: Private API {is_private_api}\033[0m")

manifest_url = f"https://api.nasa.gov/mars-photos/api/v1/manifests/{ROVER_NAME}"
manifest_params = {"api_key": API_KEY}
manifest_response = requests.get(manifest_url, params=manifest_params)
try:
    manifest_data = manifest_response.json()
except Exception as e:
    print("\033[91mFailed to get manifest data from NASA API. Check your API key, internet connection, or if the API is down.\033[0m")
    print(f"Status code: {manifest_response.status_code}")
    print(f"Response text: {manifest_response.text}")
    exit(1)
latest_sol = manifest_data["photo_manifest"]["max_sol"]

def fetch_photos(sol, camera=None):
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{ROVER_NAME}/photos"
    params = {
        "sol": sol,
        "api_key": API_KEY,
        "page": PAGE
    }
    if camera and camera.lower() != "all":
        params["camera"] = camera
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("photos", [])

def get_total_photos(sol):
    manifest_url = f"https://api.nasa.gov/mars-photos/api/v1/manifests/{ROVER_NAME}"
    manifest_params = {"api_key": API_KEY}
    manifest_response = requests.get(manifest_url, params=manifest_params)
    manifest_data = manifest_response.json()
    photos_list = manifest_data["photo_manifest"]["photos"]
    for entry in photos_list:
        if entry["sol"] == sol:
            return entry["total_photos"]
    return 0

def download_photos(photos, download_dir):
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    for idx, photo in enumerate(photos, 1):
        img_url = photo["img_src"]
        img_name = f"sol_{photo['sol']}_photo_{idx}.jpg"
        img_path = os.path.join(download_dir, img_name)
        try:
            img_data = requests.get(img_url).content
            with open(img_path, "wb") as handler:
                handler.write(img_data)
            print(f"Downloaded: {img_name}")
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")
    print("------- Download Finished------------")

# Update your menu_input function to handle the "archive" command:
def menu_input(prompt):
    """Input that returns None if user types 'menu', 'exit prog', or 'archive' (case-insensitive)."""
    value = input(prompt)
    if value.strip().lower() == "menu":
        print("\033[93m" + "-" * 60 + "\033[0m")
        raise KeyboardInterrupt
    if value.strip().lower() == "exit prog":
        print("\033[91mExiting program.\033[0m")
        sys.exit()
    if value.strip().lower() == "archive":
        archive_photos()
        raise KeyboardInterrupt  # Return to menu after archiving
    return value

def archive_photos():
    """Move all files from Pics to pic arc directory."""
    src_dir = "/Users/edvards/Desktop/python stuff/Nasa API stuff/Mars Rover/Mars Rover Pics"
    dst_dir = "/Users/edvards/Desktop/python stuff/Nasa API stuff/Mars Rover/pic arc"
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    files = os.listdir(src_dir)
    if not files:
        print("\033[93mNo files to archive.\033[0m")
        return
    for file in files:
        src_file = os.path.join(src_dir, file)
        dst_file = os.path.join(dst_dir, file)
        try:
            shutil.move(src_file, dst_file)
            print(f"\033[92mArchived: {file}\033[0m")
        except Exception as e:
            print(f"\033[91mFailed to archive {file}: {e}\033[0m")
    print("\033[93mAll files archived.\033[0m")

while True:
    try:
        print("Choose an option:")
        print("1. Test Specific sol day")
        print("2. Latest picture from rover")
        print("3. Show total photos taken on a sol")
        print("4. Find sol and photos by Earth date (day/month/year)")
        choice = input("Enter 1, 2, 3 or 4: ").strip()

        if choice == "1":
            while True:
                try:
                    sol = menu_input("Enter the sol (Rover Martian Day mission count) you want to view: ").strip()
                    sol = int(sol)
                    if sol < 0:
                        print("Sol must be a non-negative integer.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid integer for sol.")
                except KeyboardInterrupt:
                    break  # Return to main menu
            else:
                continue
            try:
                print_camera_options()
                camera = menu_input('Enter camera name (or type "all" for all cameras): ').strip().upper()
            except KeyboardInterrupt:
                continue
            attempts = 10
            photos = fetch_photos(sol, camera if camera else None)
            for i in range(attempts):
                if sol < 0:
                    print("ERROR 2, Number entered into negative, script ends")
                    exit()
                if photos:
                    print(f"Photos found on attempt {i+1}:")
                    print(f"Found {len(photos)} photos on sol {sol} from {ROVER_NAME.capitalize()} rover using {camera if camera else 'ALL'} camera(s).")
                    for idx, photo in enumerate(photos[:5], 1):
                        print(f"{idx}: \033[94m{photo['img_src']}\033[0m (Camera: {photo['camera']['name']})")
                    try:
                        download_cmd = menu_input('Type "DOWNLOAD" to download all, or enter the number of a specific photo to download just that one: ').strip()
                    except KeyboardInterrupt:
                        break
                    download_dir = "/Users/edvards/Desktop/python stuff/Nasa API stuff/Mars Rover/Mars Rover Pics"
                    if download_cmd.lower() == "download":
                        download_photos(photos, download_dir)
                    elif download_cmd.isdigit():
                        pic_idx = int(download_cmd)
                        if 1 <= pic_idx <= len(photos):
                            selected_photo = [photos[pic_idx - 1]]
                            download_photos(selected_photo, download_dir)
                        else:
                            print("Invalid photo number.")
                    else:
                        print("No download command recognized.")
                    break
                else:
                    print(f"(attempt {i+1}). No photos found on sol {sol}, trying {sol - 30}...")
                    sol -= 30
                    photos = fetch_photos(sol, camera if camera else None)
            else:
                print(f"ERROR 1, No photos after {attempts} attempts")

        elif choice == "2":
            try:
                sol = latest_sol
                print_camera_options()
                camera = menu_input('Enter camera name (or type "all" for all cameras): ').strip().upper()
            except KeyboardInterrupt:
                continue
            attempts = 10
            photos = fetch_photos(sol, camera if camera else None)
            for i in range(attempts):
                if photos:
                    print(f"Photos found on attempt {i+1}:")
                    print(f"Found {len(photos)} photos on sol {sol} from {ROVER_NAME.capitalize()} rover using {camera if camera else 'ALL'} camera(s).")
                    for idx, photo in enumerate(photos[:5], 1):
                        print(f"{idx}: \033[94m{photo['img_src']}\033[0m (Camera: {photo['camera']['name']})")
                    try:
                        download_cmd = menu_input('Type "DOWNLOAD" to download all, or enter the number of a specific photo to download just that one: ').strip()
                    except KeyboardInterrupt:
                        break
                    download_dir = "/Users/edvards/Desktop/python stuff/Nasa API stuff/Mars Rover/Mars Rover Pics"
                    if download_cmd.lower() == "download":
                        download_photos(photos, download_dir)
                    elif download_cmd.isdigit():
                        pic_idx = int(download_cmd)
                        if 1 <= pic_idx <= len(photos):
                            selected_photo = [photos[pic_idx - 1]]
                            download_photos(selected_photo, download_dir)
                        else:
                            print("Invalid photo number.")
                    else:
                        print("No download command recognized.")
                    break
                else:
                    print(f"(attempt {i+1}). No photos found on sol {sol}, trying {sol - 30}...")
                    sol -= 30
                    photos = fetch_photos(sol, camera if camera else None)
            else:
                print(f"ERROR 1, No photos after {attempts} attempts")
                continue  # Return to main menu if no photos found after all attempts

        elif choice == "3":
            print(f"Latest available sol for {ROVER_NAME.capitalize()} rover: {latest_sol}")
            while True:
                try:
                    sol = menu_input("Enter the sol (Martian Day) you want to check total photos for: ").strip()
                    sol = int(sol)
                    if sol < 0:
                        print("Sol must be a non-negative integer.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid integer for sol.")
                except KeyboardInterrupt:
                    break
            else:
                continue
            while True:
                total = get_total_photos(sol)
                print(f"Total photos taken by {ROVER_NAME.capitalize()} rover on sol {sol}: {total}")
                try:
                    cmd = menu_input('Type "SOL Photos" to list all photo links for this sol: ').strip()
                except KeyboardInterrupt:
                    break
                if cmd.lower() == "sol photos":
                    photos = fetch_photos(sol)  # Fetch all cameras
                    if photos:
                        print(f"Listing up to {len(photos)} photo links for sol {sol}:")
                        camera_counts = {}
                        for photo in photos:
                            cam = photo['camera']['name']
                            camera_counts[cam] = camera_counts.get(cam, 0) + 1
                        print("Photos per camera for this sol:")
                        for cam, count in camera_counts.items():
                            print(f"  {cam}: {count} photo(s)")
                        cameras = sorted(camera_counts.keys())
                        print(f"Cameras used by {ROVER_NAME.capitalize()} rover on sol {sol}: {', '.join(cameras)}")
                        for idx, photo in enumerate(photos, 1):
                            print(f"{idx}: \033[94m{photo['img_src']}\033[0m (Camera: {photo['camera']['name']})")
                        print(f"\nAvailable cameras for sol {sol}: {', '.join(cameras)}")
                        try:
                            download_cmd = menu_input('Type "DOWNLOAD" to download all, or enter the number of a specific photo to download just that one: ').strip()
                        except KeyboardInterrupt:
                            break
                        download_dir = "/Users/edvards/Desktop/python stuff/Nasa API stuff/Mars Rover/Mars Rover Pics"
                        if download_cmd.lower() == "download":
                            download_photos(photos, download_dir)
                        elif download_cmd.isdigit():
                            pic_idx = int(download_cmd)
                            if 1 <= pic_idx <= len(photos):
                                selected_photo = [photos[pic_idx - 1]]
                                download_photos(selected_photo, download_dir)
                            else:
                                print("Invalid photo number.")
                        else:
                            print("No download command recognized.")
                        break  # Exit after successful listing
                    else:
                        print(f"No photos found for sol {sol}.")
                        try:
                            retry = menu_input('Type "retry" to enter a new sol, or anything else to exit: ').strip()
                        except KeyboardInterrupt:
                            break
                        if retry.lower() == "retry":
                            while True:
                                try:
                                    sol = menu_input("Enter the sol (Martian Day) you want to check total photos for: ").strip()
                                    sol = int(sol)
                                    if sol < 0:
                                        print("Sol must be a non-negative integer.")
                                        continue
                                    break
                                except ValueError:
                                    print("Please enter a valid integer for sol.")
                                except KeyboardInterrupt:
                                    break
                            continue  # Repeat the search with new sol
                        else:
                            break  # Exit option 3
                else:
                    break  # Exit option 3 if "SOL Photos" not typed
        elif choice == "4":
            while True:
                try:
                    date_str = menu_input("Enter Earth date (day/month/year): ").strip()
                    try:
                        day, month, year = map(int, date_str.split("/"))
                        earth_date = datetime.date(year, month, day)
                    except Exception:
                        print("\033[91mNot a valid date. Please try again.\033[0m")
                        continue  # Let the user retry entering the date

                    # Get manifest data for rover operation dates
                    landing_date = manifest_data["photo_manifest"]["landing_date"]
                    max_date = manifest_data["photo_manifest"]["max_date"]
                    landing_date_dt = datetime.datetime.strptime(landing_date, "%Y-%m-%d").date()
                    max_date_dt = datetime.datetime.strptime(max_date, "%Y-%m-%d").date()

                    if not (landing_date_dt <= earth_date <= max_date_dt):
                        print(f"{ROVER_NAME.capitalize()} was not operational on {earth_date}.")
                        break

                    # Find sol for this earth date
                    sol = None
                    for entry in manifest_data["photo_manifest"]["photos"]:
                        if entry["earth_date"] == earth_date.strftime("%Y-%m-%d"):
                            sol = entry["sol"]
                            break

                    if sol is None:
                        print("\033[91mERROR 3, Not possible, please type menu:\033[0m")
                        break

                    print(f"Sol {sol} corresponds to Earth date {earth_date.strftime('%Y-%m-%d')}.")
                    total = get_total_photos(sol)
                    print(f"Total photos taken by {ROVER_NAME.capitalize()} rover on sol {sol}: {total}")
                    photos = fetch_photos(sol)
                    if photos:
                        print(f"Listing up to {len(photos)} photo links for sol {sol}:")
                        camera_counts = {}
                        for photo in photos:
                            cam = photo['camera']['name']
                            camera_counts[cam] = camera_counts.get(cam, 0) + 1
                        print("Photos per camera for this sol:")
                        for cam, count in camera_counts.items():
                            print(f"  {cam}: {count} photo(s)")
                        cameras = sorted(camera_counts.keys())
                        print(f"Cameras used by {ROVER_NAME.capitalize()} rover on sol {sol}: {', '.join(cameras)}")
                        for idx, photo in enumerate(photos, 1):
                            print(f"{idx}: \033[94m{photo['img_src']}\033[0m (Camera: {photo['camera']['name']})")
                        print(f"\nAvailable cameras for sol {sol}: {', '.join(cameras)}")
                        try:
                            download_cmd = menu_input('Type "DOWNLOAD" to download all, or enter the number of a specific photo to download just that one: ').strip()
                        except KeyboardInterrupt:
                            break
                        download_dir = "/Users/edvards/Desktop/python stuff/Nasa API stuff/Mars Rover/Mars Rover Pics"
                        if download_cmd.lower() == "download":
                            download_photos(photos, download_dir)
                        elif download_cmd.isdigit():
                            pic_idx = int(download_cmd)
                            if 1 <= pic_idx <= len(photos):
                                selected_photo = [photos[pic_idx - 1]]
                                download_photos(selected_photo, download_dir)
                            else:
                                print("Invalid photo number.")
                        else:
                            print("No download command recognized.")
                    else:
                        print(f"No photos found for sol {sol}.")
                    break  # Exit after successful listing or error
                except KeyboardInterrupt:
                    break

        else:
            print("Invalid option.")
    except KeyboardInterrupt:
        # This catches 'menu' from anywhere and restarts the main menu
        continue