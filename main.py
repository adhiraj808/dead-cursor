import customtkinter as ctk
import time
from jiggler import jiggler_instance

class DeadCursorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dead Cursor - Mouse Jiggler")
        self.geometry("400x450")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.setup_ui()
        self.update_status_loop()

    def setup_ui(self):
        # Header
        self.header_label = ctk.CTkLabel(self, text="👻 Dead Cursor", font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.pack(pady=(20, 10))

        self.subheader_label = ctk.CTkLabel(self, text="Keep your system alive automatically", font=ctk.CTkFont(size=12))
        self.subheader_label.pack(pady=(0, 20))

        # Inactivity Timeout
        self.timeout_frame = ctk.CTkFrame(self)
        self.timeout_frame.pack(pady=10, padx=20, fill="x")

        self.timeout_label = ctk.CTkLabel(self.timeout_frame, text="Inactivity Threshold (seconds):")
        self.timeout_label.pack(pady=(5, 0))

        self.timeout_entry = ctk.CTkEntry(self.timeout_frame, placeholder_text="300")
        self.timeout_entry.insert(0, "300")
        self.timeout_entry.pack(pady=5, padx=10)

        # Jiggle Duration
        self.duration_frame = ctk.CTkFrame(self)
        self.duration_frame.pack(pady=10, padx=20, fill="x")

        self.duration_label = ctk.CTkLabel(self.duration_frame, text="Jiggle Duration (seconds):")
        self.duration_label.pack(pady=(5, 0))

        self.duration_entry = ctk.CTkEntry(self.duration_frame, placeholder_text="30")
        self.duration_entry.insert(0, "30")
        self.duration_entry.pack(pady=5, padx=10)

        # Status
        self.status_label = ctk.CTkLabel(self, text="Status: Stopped", font=ctk.CTkFont(weight="bold"))
        self.status_label.pack(pady=10)

        self.timer_label = ctk.CTkLabel(self, text="Idle for: 0s")
        self.timer_label.pack(pady=5)

        # Control Button
        self.control_button = ctk.CTkButton(self, text="Start Guard", command=self.toggle_guard, height=40)
        self.control_button.pack(pady=20)

    def toggle_guard(self):
        if not jiggler_instance.is_running:
            try:
                threshold = int(self.timeout_entry.get())
                duration = int(self.duration_entry.get())
                
                jiggler_instance.inactivity_threshold = threshold
                jiggler_instance.jiggle_duration = duration
                
                jiggler_instance.start()
                self.control_button.configure(text="Stop Guard", fg_color="red", hover_color="#8B0000")
                self.timeout_entry.configure(state="disabled")
                self.duration_entry.configure(state="disabled")
            except ValueError:
                # Handle non-integer input
                self.status_label.configure(text="Error: Enter valid numbers", text_color="red")
        else:
            jiggler_instance.stop()
            self.control_button.configure(text="Start Guard", fg_color=["#3B8ED0", "#1F6AA5"], hover_color=["#367E96", "#144870"])
            self.timeout_entry.configure(state="normal")
            self.duration_entry.configure(state="normal")
            self.status_label.configure(text="Status: Stopped", text_color=["#DCE4EE", "#DCE4EE"])

    def update_status_loop(self):
        if jiggler_instance.is_running:
            if jiggler_instance.is_jiggling:
                self.status_label.configure(text="Status: JIGGLING! 🚀", text_color="#22c55e")
            else:
                self.status_label.configure(text="Status: Monitoring... 🕵️", text_color="#38bdf8")
            
            idle_time = int(time.time() - jiggler_instance.last_activity_time)
            self.timer_label.configure(text=f"Idle for: {idle_time}s")
        else:
            self.timer_label.configure(text="Idle for: 0s")
            
        self.after(500, self.update_status_loop)

if __name__ == "__main__":
    app = DeadCursorApp()
    app.mainloop()
