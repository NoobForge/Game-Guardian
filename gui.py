import customtkinter as ctk
import tkinter as tk
import time
import threading
from plyer import notification
import pygame
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

pygame.mixer.init()

def play_notification_sound():
    sound_path = os.path.join(os.path.dirname(__file__), "notification.mp3")
    if os.path.exists(sound_path):
        try:
            sound = pygame.mixer.Sound(sound_path)
            sound.play()
        except Exception as e:
            print(f"Failed to play sound: {e}")
    else:
        print("Notification sound file not found.")

class GameGuardianApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GameGuardian")
        self.geometry("700x450")
        self.resizable(False, False)
        self.configure(bg="#0e1624")

        self.font_header = ("Segoe UI Black", 28)
        self.font_subheader = ("Segoe UI", 22)
        self.font_button = ("Segoe UI", 24)
        self.font_small = ("Segoe UI", 18)
        self.font_timer = ("Segoe UI Black", 42)

        self.match_limit = 3
        self.time_limit = 120
        self.timer_seconds = 0
        self.timer_running = False

        self.frames = {}
        self.build_pages()
        self.show_frame("MainPage")

    def build_pages(self):
        self.frames["MainPage"] = self.build_main_page()
        self.frames["SettingsPage"] = self.build_settings_page()
        self.frames["TimerPage"] = self.build_timer_page()
        self.frames["LimitPage"] = self.build_limit_page()
        self.frames["QuizPage"] = self.build_quiz_page()
        self.frames["AccessPage"] = self.build_access_page()

    def show_frame(self, name):
        for frame in self.frames.values():
            frame.place_forget()
        frame = self.frames[name]
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.fade_in(frame)

    def fade_in(self, frame, alpha=0.0):
        if alpha >= 1.0:
            self.attributes("-alpha", 1.0)
            return
        self.attributes("-alpha", alpha)
        self.after(10, lambda: self.fade_in(frame, alpha + 0.1))

    def build_header(self, parent, title):
        ctk.CTkLabel(parent, text=title.upper(), text_color="white", font=self.font_header).pack(pady=(40, 10))

    def build_navigation_buttons(self, parent):
        nav_frame = ctk.CTkFrame(parent, fg_color="transparent")
        nav_frame.place(x=10, y=10)

        ctk.CTkButton(nav_frame, text="🏠", width=40, font=self.font_button, fg_color="#db4c65",
                      command=lambda: self.show_frame("MainPage")).pack(side="left", padx=2)
        ctk.CTkButton(nav_frame, text="🔙", width=40, font=self.font_button, fg_color="#db4c65",
                      command=lambda: self.show_frame("MainPage")).pack(side="left", padx=2)
        ctk.CTkButton(nav_frame, text="⚙️", width=40, font=self.font_button, fg_color="#db4c65",
                      command=lambda: self.show_frame("SettingsPage")).pack(side="left", padx=2)

    def build_main_page(self):
        frame = ctk.CTkFrame(self, fg_color="#0e1624")

        nav_frame = ctk.CTkFrame(frame, fg_color="transparent")
        nav_frame.place(x=10, y=20)
        ctk.CTkButton(nav_frame, text="⚙️", width=40, font=self.font_button, fg_color="#db4c65",
                      command=lambda: self.show_frame("SettingsPage")).pack(side="left", padx=2)

        main_box = ctk.CTkFrame(frame, corner_radius=10, fg_color="#1a2533")
        main_box.place(relx=0.5, rely=0.22, anchor="n", relwidth=0.98)

        ctk.CTkLabel(main_box, text="GameGaurdian", font=self.font_header).pack(pady=(10, 5))
        ctk.CTkLabel(main_box, text="One more match? Not today.", font=self.font_subheader).pack(pady=(0, 15))
        ctk.CTkButton(main_box, text="START", font=self.font_button, fg_color="#db4c65", height=60, width=220,
                      command=self.start_timer).pack(pady=10)

        return frame

    def build_settings_page(self):
        frame = ctk.CTkFrame(self, fg_color="#0e1624")
        self.build_navigation_buttons(frame)

        ctk.CTkLabel(frame, text="SETTINGS", font=self.font_header, text_color="white").pack(pady=(40, 10))

        match_frame = ctk.CTkFrame(frame, fg_color="#162233", corner_radius=10)
        match_frame.pack(pady=15, padx=20)

        ctk.CTkLabel(match_frame, text="Match limit (per day)", font=self.font_subheader).grid(row=0, column=0, columnspan=3, pady=(10, 5), padx=10)

        def update_match(delta):
            self.match_limit = max(0, self.match_limit + delta)
            match_label.configure(text=str(self.match_limit))

        ctk.CTkButton(match_frame, text="-", width=30, fg_color="transparent", text_color="#db4c65", border_color="#db4c65", border_width=2, command=lambda: update_match(-1)).grid(row=1, column=0, padx=10, pady=10)
        match_label = ctk.CTkLabel(match_frame, text=str(self.match_limit), font=self.font_button)
        match_label.grid(row=1, column=1, padx=10)
        ctk.CTkButton(match_frame, text="+", width=30, fg_color="transparent", text_color="#db4c65", border_color="#db4c65", border_width=2, command=lambda: update_match(1)).grid(row=1, column=2, padx=10)

        time_frame = ctk.CTkFrame(frame, fg_color="#162233", corner_radius=10)
        time_frame.pack(pady=15, padx=20)

        ctk.CTkLabel(time_frame, text="Time limit (per day)", font=self.font_subheader).pack(pady=(10, 5))

        def update_time_label(val):
            self.time_limit = int(val)
            time_label.configure(text=f"{self.time_limit} mins")

        time_slider = ctk.CTkSlider(time_frame, from_=1, to=240, number_of_steps=239, command=update_time_label)
        time_slider.set(self.time_limit)
        time_slider.pack(padx=10)
        time_label = ctk.CTkLabel(time_frame, text=f"{self.time_limit} mins", font=self.font_small)
        time_label.pack(pady=(0, 10))

        ctk.CTkButton(frame, text="DONE", font=self.font_button, fg_color="#db4c65", height=60, width=220,
                      command=lambda: self.show_frame("MainPage")).pack(pady=20)

        return frame

    def build_timer_page(self):
        frame = ctk.CTkFrame(self, fg_color="#0e1624")
        self.build_navigation_buttons(frame)

        timer_frame = ctk.CTkFrame(frame, width=220, height=220, corner_radius=110, fg_color="#111111")
        timer_frame.place(relx=0.5, rely=0.35, anchor="center")
        self.timer_label = ctk.CTkLabel(timer_frame, text="00:00", font=self.font_timer, text_color="#db4c65")
        self.timer_label.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkButton(frame, text="RESET TIMER", font=self.font_button,
                      fg_color="#db4c65", height=65, width=300, command=self.reset_timer).place(relx=0.5, rely=0.68, anchor="center")

        return frame

    def build_limit_page(self):
        frame = ctk.CTkFrame(self, fg_color="#0e1624")
        self.build_navigation_buttons(frame)

        ctk.CTkLabel(frame, text="⛔ Woah, You've reached your limit", font=self.font_header, text_color="#db4c65").pack(pady=(60, 10))
        ctk.CTkLabel(frame, text="Let's take a quick break before the next grind!",
                     font=self.font_subheader, text_color="white").pack(pady=(0, 30))
        ctk.CTkButton(frame, text="Take a quiz to override", font=self.font_button, fg_color="#db4c65", height=65, width=300,
                      command=self.take_quiz).pack(pady=(0, 10))
        return frame

    def build_quiz_page(self):
        frame = ctk.CTkFrame(self, fg_color="#0e1624")
        self.build_navigation_buttons(frame)
        self.build_header(frame, "Quiz")

        moods = ["MEH", "One more Ranked", "Proud of myself!!", "COOKED"]
        for mood in moods:
            ctk.CTkButton(frame, text=mood, width=300, height=65, font=self.font_button,
                          fg_color="#db4c65", command=lambda m=mood: self.handle_quiz_answer(m)).pack(pady=5)
        return frame

    def handle_quiz_answer(self, mood):
        self.timer_running = False
        self.show_frame("AccessPage")

    def build_access_page(self):
        frame = ctk.CTkFrame(self, fg_color="#0e1624")
        self.build_navigation_buttons(frame)

        success_icon = ctk.CTkLabel(frame, text="✅", font=self.font_header, text_color="#00ffcc")
        success_icon.pack(pady=(50, 5))
        ctk.CTkLabel(frame, text="ACCESS UNLOCKED!!!", font=self.font_subheader, text_color="#00ffcc").pack()
        ctk.CTkLabel(frame, text="You've passed the focus check. Go win that next round :)", font=self.font_small).pack(pady=(0, 30))

        ctk.CTkButton(frame, text="Continue to game", font=self.font_button, fg_color="#db4c65", height=65, width=300,
                      command=lambda: self.show_frame("MainPage")).pack()
        return frame

    def start_timer(self):
        if self.timer_running:
            self.show_frame("TimerPage")
            return
        self.timer_seconds = self.time_limit * 60
        self.timer_running = True
        self.show_frame("TimerPage")
        self.countdown()

    def reset_timer(self):
        self.timer_running = False
        self.timer_label.configure(text="00:00")
        self.show_frame("MainPage")

    def countdown(self):
        if not self.timer_running or not self.winfo_exists():
            return

        mins, secs = divmod(self.timer_seconds, 60)
        self.timer_label.configure(text=f"{mins:02}:{secs:02}")

        if self.timer_seconds <= 0:
            self.timer_running = False
            self.notify_limit_reached()
        else:
            self.timer_seconds -= 1
            self.after(1000, self.countdown)

    def notify_limit_reached(self):
        play_notification_sound()
        notification.notify(
            title="GameGuardian Timer",
            message="Your daily time limit has been reached.",
            timeout=5
        )
        self.show_frame("LimitPage")

    def take_quiz(self):
        self.timer_running = False
        self.show_frame("QuizPage")

if __name__ == "__main__":
    app = GameGuardianApp()
    app.mainloop()
