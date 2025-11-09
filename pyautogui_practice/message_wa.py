import pyautogui
import time
import webbrowser
import platform

# ========== CONFIGURATION ==========
contact_name = "SE-AI-B3-2"      # <-- Change to your WhatsApp contact name
message = "Hi Eagles, Happy Sunday! This is an automated message sent via pyautogui!"
wait_time = 15                 # seconds to wait for WhatsApp Web to load
close_tab_after = True         # set False if you don't want to close browser
# ==================================

# Step 1: Open WhatsApp Web
webbrowser.open("https://web.whatsapp.com")
print("Opening WhatsApp Web...")
time.sleep(wait_time)  # Wait for page to load completely

# Step 2: Click on search bar
# (You might need to adjust these coordinates once)
print("Locating search bar...")
pyautogui.click(x=216, y=255)  # <-- Adjust this based on your screen resolution
time.sleep(1)

# Step 3: Type contact name and select it
pyautogui.typewrite(contact_name, interval=0.1)
time.sleep(2)
pyautogui.press('enter')

# Step 4: Type your message
time.sleep(2)
pyautogui.typewrite(message, interval=0.05)
pyautogui.press('enter')

print("✅ Message sent successfully!")

# Step 5: Close WhatsApp Web tab/window
if close_tab_after:
    time.sleep(2)  # brief pause before closing
    os_name = platform.system()

    print("Closing browser window...")
    if os_name == "Windows":
        pyautogui.hotkey('ctrl', 'w')    # closes tab
        # pyautogui.hotkey('alt', 'f4')  # uncomment to close entire window
    elif os_name == "Darwin":  # macOS
        pyautogui.hotkey('command', 'w')
    else:  # Linux or others
        pyautogui.hotkey('ctrl', 'w')

    print("✅ WhatsApp Web closed.")
