import customtkinter as ctk
import tkinter as tk
import time
import threading


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class GameGuardianApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GameGuardian")
        self.geometry("700x450")
        self.resizable(False, False)
        self.font_header = ("Segoe UI Black", 28)
        self.font_subheader = ("Segoe UI", 16)
        self.font_button = ("Segoe UI", 16)
        self.font_small = ("Segoe UI", 12)

        self.match_limit = 3
        self.time_limit = 120
        self.timer_seconds = 5 * 60

        self.frames = {}
        self.build_pages()
        self.show_frame("MainPage")

    def build_pages(self):
        self.frames["MainPage"] = self.build_main_page()
        self.frames["SettingsPage"] = self.build_settings_page()
        self.frames["LimitPage"] = self.build_limit_page()
        self.frames["QuizPage"] = self.build_quiz_page()
        self.frames["AccessPage"] = self.build_access_page()

    def show_frame(self, name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(expand=True, fill="both")

    def build_main_page(self):
        frame = ctk.CTkFrame(self)
        label = ctk.CTkLabel(frame, text="GameGuardian", font=self.font_header)
        label.pack(pady=(30, 10))

        sublabel = ctk.CTkLabel(frame, text="One more match? Not today.", font=self.font_subheader)
        sublabel.pack(pady=(0, 30))

        start_btn = ctk.CTkButton(
            frame, text="START", font=self.font_button,
            fg_color="#db4c65", hover_color="#c13c53",
            command=lambda: self.show_frame("SettingsPage")
        )
        start_btn.pack()

        return frame

    def build_settings_page(self):
        frame = ctk.CTkFrame(self)

        title = ctk.CTkLabel(frame, text="settings", font=self.font_header)
        title.pack(pady=(30, 20))

        # Match limit
        match_frame = ctk.CTkFrame(frame, fg_color="transparent")
        match_frame.pack(pady=10)
        ctk.CTkLabel(match_frame, text="Match limit (per day)", font=self.font_subheader).grid(row=0, column=0, columnspan=3)

        def update_match(delta):
            self.match_limit = max(0, self.match_limit + delta)
            match_label.configure(text=str(self.match_limit))

        ctk.CTkButton(match_frame, text="-", width=30, command=lambda: update_match(-1)).grid(row=1, column=0, padx=10)
        match_label = ctk.CTkLabel(match_frame, text=str(self.match_limit), font=self.font_button)
        match_label.grid(row=1, column=1, padx=10)
        ctk.CTkButton(match_frame, text="+", width=30, command=lambda: update_match(1)).grid(row=1, column=2, padx=10)

        # Time limit
        time_frame = ctk.CTkFrame(frame, fg_color="transparent")
        time_frame.pack(pady=20)
        ctk.CTkLabel(time_frame, text="Time limit (per day)", font=self.font_subheader).pack()

        time_slider = ctk.CTkSlider(
            time_frame, from_=30, to=240, number_of_steps=7,
            command=lambda val: time_label.configure(text=f"{int(val)} mins")
        )
        time_slider.set(self.time_limit)
        time_slider.pack()
        time_label = ctk.CTkLabel(time_frame, text=f"{self.time_limit} mins", font=self.font_small)
        time_label.pack()

        done_btn = ctk.CTkButton(
            frame, text="DONE", font=self.font_button,
            fg_color="#db4c65", command=lambda: self.show_frame("LimitPage")
        )
        done_btn.pack(pady=20)

        return frame

    def build_limit_page(self):
        frame = ctk.CTkFrame(self)

        warning = ctk.CTkLabel(frame, text="whoa. You've hit your limit.", font=self.font_header, text_color="red")
        warning.pack(pady=(30, 5))

        info = ctk.CTkLabel(frame, text="Let's take a quick break before the next grind.", font=self.font_subheader)
        info.pack(pady=(0, 20))

        timer_label = ctk.CTkLabel(frame, text="05:00", font=("Segoe UI", 30), text_color="white")
        timer_label.pack(pady=10)

        def countdown():
            while self.timer_seconds > 0:
                mins, secs = divmod(self.timer_seconds, 60)
                timer_label.configure(text=f"{mins:02}:{secs:02}")
                time.sleep(1)
                self.timer_seconds -= 1

        threading.Thread(target=countdown, daemon=True).start()

        override_btn = ctk.CTkButton(
            frame, text="Take a quiz to override", font=self.font_button,
            fg_color="#db4c65", command=lambda: self.show_frame("QuizPage")
        )
        override_btn.pack(pady=20)

        return frame

    def build_quiz_page(self):
        frame = ctk.CTkFrame(self)

        question = ctk.CTkLabel(frame, text="Which vibe matches your current mood?", font=self.font_subheader)
        question.pack(pady=(30, 20))

        moods = ["MEH", "One more Ranked", "Proud of myself!!", "COOKED"]
        for mood in moods:
            btn = ctk.CTkButton(
                frame, text=mood, width=200, font=self.font_button,
                fg_color="#332222", hover_color="#db4c65",
                command=lambda m=mood: self.handle_quiz_answer(m)
            )
            btn.pack(pady=5)

        return frame

    def handle_quiz_answer(self, mood):
        self.show_frame("AccessPage")

    def build_access_page(self):
        frame = ctk.CTkFrame(self)

        check = ctk.CTkLabel(frame, text="✅ ACCESS UNLOCKED!!!", font=self.font_header, text_color="springgreen")
        check.pack(pady=(30, 10))

        message = ctk.CTkLabel(
            frame, text="You've passed the focus check. Go win that next round :)",
            font=self.font_subheader
        )
        message.pack(pady=(0, 20))

        cont_btn = ctk.CTkButton(
            frame, text="Continue to game", font=self.font_button,
            fg_color="#db4c65", command=lambda: self.show_frame("MainPage")
        )
        cont_btn.pack()

        return frame
    


if __name__ == "__main__":
    app = GameGuardianApp()
    app.mainloop()

