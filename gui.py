import tkinter as tk
from tkinter import scrolledtext
import threading
import main  # Make sure main.py is in the same folder

class VirtualAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("JoJo - Virtual Assistant")
        self.root.geometry("700x500")  # Larger window
        # Allow resizing (includes maximize button)
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="JOJO - Virtual Assistant", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=10)

        self.log_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Consolas", 11), state="disabled")
        self.log_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Custom style for SPEAKING lines
        self.log_area.tag_config("speak_style", font=("Consolas", 13, "bold"), foreground="blue")

        self.start_button = tk.Button(self.root, text="Start Assistant", font=("Helvetica", 12), command=self.run_assistant)
        self.start_button.pack(pady=10)

    def log_message(self, message):
        self.log_area.configure(state="normal")
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.configure(state="disabled")
        self.log_area.yview(tk.END)

    def log_message_with_style(self, message):
        self.log_area.configure(state="normal")
        if message.startswith("SPEAKING:"):
            self.log_area.insert(tk.END, message + "\n", "speak_style")
        else:
            self.log_area.insert(tk.END, message + "\n")
        self.log_area.configure(state="disabled")
        self.log_area.yview(tk.END)

    def run_assistant(self):
        self.start_button.config(state="disabled")
        threading.Thread(target=self.assistant_thread, daemon=True).start()

    def assistant_thread(self):
        try:
            original_print = print
            original_speak = main.speak

            def redirect_print(*args, **kwargs):
                message = " ".join(str(arg) for arg in args)
                self.root.after(0, self.log_message_with_style, message)
                original_print(*args, **kwargs)

            def redirected_speak(text):
                message = f"SPEAKING: {text}"
                self.root.after(0, self.log_message_with_style, message)
                original_speak(text)

            # Apply redirection
            main.print = redirect_print
            main.speak = redirected_speak

            # Start the assistant
            main.main()

        except Exception as e:
            self.root.after(0, self.log_message, f"ERROR: {e}")
        finally:
            self.root.after(0, lambda: self.start_button.config(state="normal"))

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualAssistantGUI(root)
    root.mainloop()
