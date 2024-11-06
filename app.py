import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteEntry
from PIL import Image, ImageTk
from weather_api import get_current_weather

# Color scheme
DARK_GREY = '#2e2e2e'
BABY_BLUE = '#89CFF0'
SUNSET_ORANGE = '#FD5E53'
WHITE = '#FFFFFF'

# Application Window
root = tk.Tk()
root.title("Weather App")
root.geometry("600x700")
root.configure(bg=DARK_GREY)
root.resizable(False, False)

# Icon
icon_image = Image.open("assets/weather_icon.png")
icon_photo = ImageTk.PhotoImage(icon_image)
root.iconphoto(False, icon_photo)

# City autocomplete suggestions
with open("assets/us_cities.txt", "r") as file:
    city_suggestions = [line.strip() for line in file]

# ttk style
style = ttk.Style()
style.theme_use('clam')

# Configure styles
style.configure("TFrame", background=DARK_GREY)
style.configure("TLabel", background=DARK_GREY, foreground=WHITE, font=("Helvetica", 16))
style.configure("Title.TLabel", background=DARK_GREY, foreground=BABY_BLUE, font=("Helvetica", 20, "bold"))
style.configure("TEntry", font=("Helvetica", 14))
style.configure("TRadiobutton", background=DARK_GREY, foreground=WHITE, font=("Helvetica", 14))
style.configure("TButton", font=("Helvetica", 14, "bold"), padding=10, foreground=WHITE, background=BABY_BLUE)
style.map("TButton",
          background=[('active', SUNSET_ORANGE)],
          foreground=[('active', WHITE)])


unit_var = tk.StringVar(value="imperial")

# Function to get weather data and update UI
def fetch_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name")
        return

    unit = unit_var.get()
    loading_label.place(relx=0.5, rely=0.5, anchor='center')
    animate_loading()
    root.update()

    weather_data = get_current_weather(city, unit)

    loading_label.place_forget()

    if "error" in weather_data:
        messagebox.showerror("Error", weather_data["error"])
    else:
        unit_symbol = "°F" if unit == "imperial" else "°C"
        city_label.config(text=f"{weather_data['city']}")
        temp_label.config(text=f"{weather_data['temperature']}{unit_symbol} (Feels like {weather_data['feels_like']}{unit_symbol})")
        desc_label.config(text=f"{weather_data['description'].capitalize()}")
        humidity_label.config(text=f"Humidity: {weather_data['humidity']}%")
        time_label.config(text=f"Time: {weather_data['timestamp']}")

# Widget frame
container = ttk.Frame(root, padding=20, style="TFrame")
container.place(relx=0.5, rely=0.5, anchor='center')

# City entry
city_entry_label = ttk.Label(container, text="Enter City Name:", style="TLabel")
city_entry_label.pack(pady=(10, 5))

city_entry = AutocompleteEntry(container, completevalues=city_suggestions, width=30, font=("Helvetica", 14))
city_entry.pack(pady=5)

# Unit buttons
unit_label = ttk.Label(container, text="Select Temperature Unit:", style="TLabel")
unit_label.pack(pady=(20, 5))

unit_frame = ttk.Frame(container, style="TFrame")
unit_frame.pack()

imperial_button = ttk.Radiobutton(unit_frame, text="Imperial (°F)", variable=unit_var, value="imperial", style="TRadiobutton")
imperial_button.pack(side='left', padx=10)

metric_button = ttk.Radiobutton(unit_frame, text="Metric (°C)", variable=unit_var, value="metric", style="TRadiobutton")
metric_button.pack(side='left', padx=10)

# Create a button to fetch weather data
fetch_button = ttk.Button(container, text="Get Weather", command=fetch_weather)
fetch_button.pack(pady=20)

# Create a loading indicator
loading_label = ttk.Label(container, text="Loading...", font=("Helvetica", 14, "italic"), foreground=BABY_BLUE, background=DARK_GREY)

# Create labels for displaying the weather data
result_frame = ttk.Frame(container, style="TFrame")
result_frame.pack(pady=20)

city_label = ttk.Label(result_frame, text="", style="Title.TLabel")
city_label.pack(pady=5)

temp_label = ttk.Label(result_frame, text="", style="TLabel")
temp_label.pack(pady=5)

desc_label = ttk.Label(result_frame, text="", style="TLabel")
desc_label.pack(pady=5)

humidity_label = ttk.Label(result_frame, text="", style="TLabel")
humidity_label.pack(pady=5)

time_label = ttk.Label(result_frame, text="", font=("Helvetica", 14, "italic"), background=DARK_GREY, foreground=WHITE)
time_label.pack(pady=5)

# Loading spinner animation
def animate_loading():
    loading_label.config(text="Loading" + "." * (animate_loading.counter % 4))
    animate_loading.counter += 1
    if loading_label.winfo_ismapped():
        root.after(500, animate_loading)
animate_loading.counter = 0

# Add hover effects to the Get Weather button
def on_enter(e):
    fetch_button.config(style="Hover.TButton")
def on_leave(e):
    fetch_button.config(style="TButton")

style.configure("Hover.TButton", font=("Helvetica", 14, "bold"), padding=10, foreground=WHITE, background=SUNSET_ORANGE)

fetch_button.bind("<Enter>", on_enter)
fetch_button.bind("<Leave>", on_leave)

# Run the main loop
root.mainloop()
