import tkinter as tk
from tkinter import Text, font
import os

class StickyNote:
    def __init__(self, master):
        self.master = master
        self.note = tk.Toplevel(master)
        self.note.overrideredirect(True)
        self.note.geometry("150x150")
        self.note.configure(bg='#FFFF99')  # Light yellow background

        # Use a relative path for the icon
        icon_path = os.path.join(os.path.dirname(__file__), 'sticky-notes.ico')
        if os.path.exists(icon_path):
            self.note.iconbitmap(icon_path)

        # Create top frame (entire top area will be draggable)
        self.top_frame = tk.Frame(self.note, bg='#FFFF99', height=25)
        self.top_frame.pack(fill=tk.X)
        self.top_frame.pack_propagate(False)

        # Add button
        self.add_button = tk.Button(self.top_frame, text="+", command=self.create_new_note, 
                                    bg='#FFFF99', relief=tk.FLAT, bd=0)
        self.add_button.pack(side=tk.LEFT, padx=(5,0))

        # Close button
        self.close_button = tk.Button(self.top_frame, text="x", command=self.close_note, 
                                      bg='#FFFF99', relief=tk.FLAT, bd=0)
        self.close_button.pack(side=tk.RIGHT, padx=(0,5))

        # Make the entire top frame draggable
        self.top_frame.bind("<ButtonPress-1>", self.start_move)
        self.top_frame.bind("<ButtonRelease-1>", self.stop_move)
        self.top_frame.bind("<B1-Motion>", self.do_move)

        # Text area with Roboto Light font
        roboto_light = font.Font(family="Roboto Light", size=10)
        self.text_area = Text(self.note, wrap=tk.WORD, bd=0, bg='#FFFF99', font=roboto_light)
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=5, pady=(0, 5))

        # Bind text changes to resize function
        self.text_area.bind("<<Modified>>", self.resize_note)

        # Define colors
        self.bg_color = '#FFFF99'  # Light yellow background
        self.resize_color = '#E6E68A'  # Slightly darker yellow for resize grip

        # Add resize grip
        self.resize_grip = tk.Frame(self.note, bg=self.resize_color, cursor='sizing')
        self.resize_grip.place(relx=1.0, rely=1.0, anchor='se', width=10, height=10)
        self.resize_grip.bind("<ButtonPress-1>", self.start_resize)
        self.resize_grip.bind("<B1-Motion>", self.do_resize)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.note.winfo_x() + deltax
        y = self.note.winfo_y() + deltay
        self.note.geometry(f"+{x}+{y}")

    def create_new_note(self):
        StickyNote(self.master)

    def close_note(self):
        self.note.destroy()

    def resize_note(self, event=None):
        self.text_area.update_idletasks()
        lines = int(self.text_area.index('end-1c').split('.')[0])
        width = max(150, min(300, max(len(line) for line in self.text_area.get('1.0', 'end-1c').split('\n')) * 10))
        height = max(150, min(300, lines * 20))
        self.note.geometry(f"{width}x{height}")
        self.text_area.edit_modified(False)

    def start_resize(self, event):
        self.x = event.x
        self.y = event.y

    def do_resize(self, event):
        xwin = self.note.winfo_x()
        ywin = self.note.winfo_y()
        startx = event.x_root - xwin
        starty = event.y_root - ywin
        width = max(150, startx)
        height = max(150, starty)
        self.note.geometry(f"{width}x{height}")

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Use the same relative path for the icon
    icon_path = os.path.join(os.path.dirname(__file__), 'sticky-notes.ico')
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
    
    StickyNote(root)
    root.mainloop()

if __name__ == "__main__":
    main()
