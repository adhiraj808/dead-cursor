import time
import threading
import random
import pyautogui
from pynput import mouse, keyboard

class MouseJiggler:
    def __init__(self):
        self.last_activity_time = time.time()
        self.is_running = False
        self.is_jiggling = False
        self.inactivity_threshold = 300  # 5 minutes default
        self.jiggle_duration = 30        # 30 seconds default
        
        self.mouse_listener = None
        self.key_listener = None
        self.main_thread = None
        
        # Disable pyautogui fail-safe for this specific app use case
        pyautogui.FAILSAFE = True 

    def _on_activity(self, *args, **kwargs):
        self.last_activity_time = time.time()
        # If we are currently jiggling and the user moves the mouse, stop jiggling
        if self.is_jiggling:
            self.is_jiggling = False

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.last_activity_time = time.time()
            
            # Recreate listeners each time we start
            self.mouse_listener = mouse.Listener(on_move=self._on_activity, on_click=self._on_activity, on_scroll=self._on_activity)
            self.key_listener = keyboard.Listener(on_press=self._on_activity)
            
            self.mouse_listener.start()
            self.key_listener.start()
            
            self.main_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.main_thread.start()

    def stop(self):
        self.is_running = False
        self.is_jiggling = False
        
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None
            
        if self.key_listener:
            self.key_listener.stop()
            self.key_listener = None

    def _monitor_loop(self):
        while self.is_running:
            idle_time = time.time() - self.last_activity_time
            if idle_time >= self.inactivity_threshold and not self.is_jiggling:
                self._perform_jiggle()
            time.sleep(1)

    def _perform_jiggle(self):
        self.is_jiggling = True
        start_jiggle_time = time.time()
        
        print(f"Inactivity threshold reached ({self.inactivity_threshold}s). Starting jiggle...")
        
        screen_width, screen_height = pyautogui.size()
        
        while self.is_jiggling and (time.time() - start_jiggle_time < self.jiggle_duration):
            # Check if user intervened
            current_idle = time.time() - self.last_activity_time
            if current_idle < 0.5: # More sensitive detection
                print("User intervention detected. Stopping jiggle.")
                self.is_jiggling = False
                break
                
            # Random movement
            x = random.randint(100, screen_width - 100)
            y = random.randint(100, screen_height - 100)
            
            # Move smoothly
            pyautogui.moveTo(x, y, duration=0.5)
            
            # Optional click
            if random.random() > 0.7:
                # pyautogui.click() // random click in random time between 1 and 3 seconds which is disabled for now
                # Small random sleeps between moves
                time.sleep(random.uniform(1, 3))
            
        self.is_jiggling = False
        print("Jiggle session ended.")  # Print when jiggle session ends
        self.last_activity_time = time.time()  # Update last activity time

jiggler_instance = MouseJiggler()  # Create instance for external access
