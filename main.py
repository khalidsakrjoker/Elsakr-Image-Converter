"""
Elsakr Image Converter - Premium Edition
Batch convert images between different formats with quality control.
Modern Dark Theme with Premium UI
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import threading
from pathlib import Path


class Colors:
    """Premium dark theme colors."""
    BG_DARK = "#0a0a0f"
    BG_CARD = "#12121a"
    BG_CARD_HOVER = "#1a1a25"
    BG_INPUT = "#1e1e2e"
    
    PRIMARY = "#10b981"  # Emerald
    PRIMARY_HOVER = "#34d399"
    PRIMARY_DARK = "#059669"
    
    SECONDARY = "#22d3ee"  # Cyan accent
    SUCCESS = "#10b981"
    WARNING = "#f59e0b"
    ERROR = "#ef4444"
    
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#a1a1aa"
    TEXT_MUTED = "#71717a"
    
    BORDER = "#27272a"
    BORDER_FOCUS = "#10b981"


class PremiumButton(tk.Canvas):
    """Custom premium button with hover effects."""
    
    def __init__(self, parent, text, command=None, width=200, height=45, 
                 primary=True, **kwargs):
        super().__init__(parent, width=width, height=height, 
                        bg=Colors.BG_CARD, highlightthickness=0, **kwargs)
        
        self.command = command
        self.text = text
        self.width = width
        self.height = height
        self.primary = primary
        self.hovered = False
        self.enabled = True
        
        self.draw_button()
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        
    def draw_button(self):
        """Draw the button."""
        self.delete("all")
        
        if not self.enabled:
            bg_color = Colors.BG_INPUT
            text_color = Colors.TEXT_MUTED
        elif self.primary:
            bg_color = Colors.PRIMARY_HOVER if self.hovered else Colors.PRIMARY
            text_color = Colors.TEXT_PRIMARY
        else:
            bg_color = Colors.BG_CARD_HOVER if self.hovered else Colors.BG_INPUT
            text_color = Colors.TEXT_SECONDARY
        
        # Draw rounded rectangle
        radius = 10
        self.create_rounded_rect(2, 2, self.width-2, self.height-2, 
                                  radius, fill=bg_color, outline="")
        
        # Draw text
        self.create_text(self.width//2, self.height//2, 
                        text=self.text, fill=text_color,
                        font=("Segoe UI Semibold", 11))
        
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Create a rounded rectangle."""
        points = [
            x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius,
            x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2,
            x1, y2, x1, y2-radius, x1, y1+radius, x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
        
    def on_enter(self, event):
        if self.enabled:
            self.hovered = True
            self.draw_button()
            self.config(cursor="hand2")
        
    def on_leave(self, event):
        self.hovered = False
        self.draw_button()
        
    def on_click(self, event):
        if self.command and self.enabled:
            self.command()
            
    def set_enabled(self, enabled):
        self.enabled = enabled
        self.draw_button()


class PremiumCard(tk.Frame):
    """Premium card container."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=Colors.BG_CARD, **kwargs)
        self.config(highlightbackground=Colors.BORDER, highlightthickness=1)


class FileListItem(tk.Frame):
    """Single file item in the list."""
    
    def __init__(self, parent, filepath, on_remove=None, **kwargs):
        super().__init__(parent, bg=Colors.BG_INPUT, **kwargs)
        
        self.filepath = filepath
        self.on_remove = on_remove
        
        self.config(highlightbackground=Colors.BORDER, highlightthickness=1)
        
        # File icon and name
        filename = os.path.basename(filepath)
        ext = os.path.splitext(filename)[1].upper()
        
        info_frame = tk.Frame(self, bg=Colors.BG_INPUT)
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=8)
        
        # Extension badge
        ext_label = tk.Label(info_frame, text=ext, font=("Segoe UI", 8, "bold"),
                            fg=Colors.PRIMARY, bg=Colors.BG_DARK, padx=5, pady=2)
        ext_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Filename
        name_label = tk.Label(info_frame, text=filename[:40] + "..." if len(filename) > 40 else filename,
                             font=("Segoe UI", 10), fg=Colors.TEXT_PRIMARY, bg=Colors.BG_INPUT)
        name_label.pack(side=tk.LEFT)
        
        # File size
        try:
            size = os.path.getsize(filepath)
            size_str = self.format_size(size)
            size_label = tk.Label(info_frame, text=size_str, font=("Segoe UI", 9),
                                 fg=Colors.TEXT_MUTED, bg=Colors.BG_INPUT)
            size_label.pack(side=tk.RIGHT, padx=(10, 0))
        except:
            pass
        
        # Remove button
        remove_btn = tk.Label(self, text="✕", font=("Segoe UI", 12),
                             fg=Colors.TEXT_MUTED, bg=Colors.BG_INPUT, cursor="hand2")
        remove_btn.pack(side=tk.RIGHT, padx=10)
        remove_btn.bind("<Button-1>", lambda e: self.remove())
        remove_btn.bind("<Enter>", lambda e: remove_btn.config(fg=Colors.ERROR))
        remove_btn.bind("<Leave>", lambda e: remove_btn.config(fg=Colors.TEXT_MUTED))
        
    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
        
    def remove(self):
        if self.on_remove:
            self.on_remove(self.filepath)
        self.destroy()


class ImageConverter:
    """Main application class."""
    
    SUPPORTED_FORMATS = {
        'PNG': '.png',
        'JPEG': '.jpg',
        'WebP': '.webp',
        'BMP': '.bmp',
        'TIFF': '.tiff',
        'GIF': '.gif',
        'ICO': '.ico'
    }
    
    INPUT_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff', '.tif', '.gif', '.ico')
    
    def __init__(self, root):
        self.root = root
        self.root.title("Elsakr Image Converter")
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)
        self.root.configure(bg=Colors.BG_DARK)
        
        # Set window icon
        self.set_window_icon()
        
        # Variables
        self.files = []
        self.output_format = tk.StringVar(value="PNG")
        self.quality = tk.IntVar(value=85)
        self.output_folder = None
        self.preserve_metadata = tk.BooleanVar(value=False)
        
        # Load logo
        self.load_logo()
        
        # Build UI
        self.create_ui()
        
    def resource_path(self, relative_path):
        """Get absolute path to resource."""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
        
    def set_window_icon(self):
        """Set the window icon."""
        try:
            icon_path = self.resource_path(os.path.join("assets", "fav.ico"))
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
            
    def load_logo(self):
        """Load the Elsakr logo."""
        self.logo_photo = None
        try:
            logo_path = self.resource_path(os.path.join("assets", "Sakr-logo.png"))
            if os.path.exists(logo_path):
                logo = Image.open(logo_path)
                logo.thumbnail((45, 45), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo)
        except:
            pass
        
    def create_ui(self):
        """Create the premium UI."""
        main = tk.Frame(self.root, bg=Colors.BG_DARK)
        main.pack(fill=tk.BOTH, expand=True, padx=30, pady=25)
        
        # Header
        self.create_header(main)
        
        # Content
        content = tk.Frame(main, bg=Colors.BG_DARK)
        content.pack(fill=tk.BOTH, expand=True, pady=(25, 0))
        
        # Left panel - File list
        self.create_left_panel(content)
        
        # Right panel - Settings
        self.create_right_panel(content)
        
    def create_header(self, parent):
        """Create the header section."""
        header = tk.Frame(parent, bg=Colors.BG_DARK)
        header.pack(fill=tk.X)
        
        title_frame = tk.Frame(header, bg=Colors.BG_DARK)
        title_frame.pack(side=tk.LEFT)
        
        if self.logo_photo:
            logo_label = tk.Label(title_frame, image=self.logo_photo, bg=Colors.BG_DARK)
            logo_label.pack(side=tk.LEFT, padx=(0, 15))
        
        title_text = tk.Frame(title_frame, bg=Colors.BG_DARK)
        title_text.pack(side=tk.LEFT)
        
        tk.Label(title_text, text="Image Converter", 
                font=("Segoe UI Bold", 24), fg=Colors.TEXT_PRIMARY,
                bg=Colors.BG_DARK).pack(anchor=tk.W)
        
        tk.Label(title_text, text="Batch convert images between formats",
                font=("Segoe UI", 11), fg=Colors.TEXT_MUTED,
                bg=Colors.BG_DARK).pack(anchor=tk.W)
        
        # Version badge
        badge = tk.Label(header, text=" v1.0 ", font=("Segoe UI", 9),
                        fg=Colors.PRIMARY, bg=Colors.BG_INPUT)
        badge.pack(side=tk.RIGHT)
        
    def create_left_panel(self, parent):
        """Create the left panel with file list."""
        left = tk.Frame(parent, bg=Colors.BG_DARK)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Files Card
        files_card = PremiumCard(left, padx=20, pady=20)
        files_card.pack(fill=tk.BOTH, expand=True)
        
        # Header row
        header_row = tk.Frame(files_card, bg=Colors.BG_CARD)
        header_row.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(header_row, text="📁 Files to Convert",
                font=("Segoe UI Semibold", 13), fg=Colors.TEXT_PRIMARY,
                bg=Colors.BG_CARD).pack(side=tk.LEFT)
        
        self.file_count_label = tk.Label(header_row, text="0 files",
                                         font=("Segoe UI", 10), fg=Colors.TEXT_MUTED,
                                         bg=Colors.BG_CARD)
        self.file_count_label.pack(side=tk.RIGHT)
        
        # File list container with scrollbar
        list_container = tk.Frame(files_card, bg=Colors.BG_CARD)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas for scrolling
        self.canvas = tk.Canvas(list_container, bg=Colors.BG_CARD, 
                                highlightthickness=0, height=300)
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", 
                                  command=self.canvas.yview)
        
        self.files_frame = tk.Frame(self.canvas, bg=Colors.BG_CARD)
        
        self.canvas.create_window((0, 0), window=self.files_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.files_frame.bind("<Configure>", 
                             lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Empty state
        self.empty_label = tk.Label(self.files_frame, 
                                    text="No files added\n\nClick 'Add Files' or 'Add Folder' to start",
                                    font=("Segoe UI", 11), fg=Colors.TEXT_MUTED,
                                    bg=Colors.BG_CARD, justify="center")
        self.empty_label.pack(pady=50)
        
        # Buttons row
        btn_row = tk.Frame(files_card, bg=Colors.BG_CARD)
        btn_row.pack(fill=tk.X, pady=(15, 0))
        
        add_files_btn = PremiumButton(btn_row, text="📄 Add Files",
                                      command=self.add_files, width=150, height=40,
                                      primary=False)
        add_files_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        add_folder_btn = PremiumButton(btn_row, text="📂 Add Folder",
                                       command=self.add_folder, width=150, height=40,
                                       primary=False)
        add_folder_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = PremiumButton(btn_row, text="🗑️ Clear All",
                                  command=self.clear_files, width=120, height=40,
                                  primary=False)
        clear_btn.pack(side=tk.RIGHT)
        
    def create_right_panel(self, parent):
        """Create the right panel with settings."""
        right = tk.Frame(parent, bg=Colors.BG_DARK, width=320)
        right.pack(side=tk.RIGHT, fill=tk.Y)
        right.pack_propagate(False)
        
        # Settings Card
        settings_card = PremiumCard(right, padx=20, pady=20)
        settings_card.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(settings_card, text="⚙️ Conversion Settings",
                font=("Segoe UI Semibold", 13), fg=Colors.TEXT_PRIMARY,
                bg=Colors.BG_CARD).pack(anchor=tk.W, pady=(0, 20))
        
        # Output format
        tk.Label(settings_card, text="Output Format",
                font=("Segoe UI", 10), fg=Colors.TEXT_SECONDARY,
                bg=Colors.BG_CARD).pack(anchor=tk.W)
        
        format_frame = tk.Frame(settings_card, bg=Colors.BG_CARD)
        format_frame.pack(fill=tk.X, pady=(8, 15))
        
        for i, fmt in enumerate(self.SUPPORTED_FORMATS.keys()):
            rb = tk.Radiobutton(format_frame, text=fmt, variable=self.output_format,
                               value=fmt, font=("Segoe UI", 10),
                               fg=Colors.TEXT_PRIMARY, bg=Colors.BG_CARD,
                               selectcolor=Colors.BG_INPUT,
                               activebackground=Colors.BG_CARD,
                               activeforeground=Colors.TEXT_PRIMARY)
            rb.grid(row=i//4, column=i%4, sticky="w", padx=5, pady=2)
        
        # Quality slider (for lossy formats)
        tk.Label(settings_card, text="Quality (JPEG/WebP)",
                font=("Segoe UI", 10), fg=Colors.TEXT_SECONDARY,
                bg=Colors.BG_CARD).pack(anchor=tk.W, pady=(10, 0))
        
        quality_frame = tk.Frame(settings_card, bg=Colors.BG_CARD)
        quality_frame.pack(fill=tk.X, pady=(8, 15))
        
        self.quality_slider = ttk.Scale(quality_frame, from_=1, to=100,
                                        variable=self.quality, orient="horizontal")
        self.quality_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.quality_label = tk.Label(quality_frame, text="85%",
                                     font=("Segoe UI", 10), fg=Colors.TEXT_PRIMARY,
                                     bg=Colors.BG_CARD, width=5)
        self.quality_label.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.quality.trace_add("write", self.update_quality_label)
        
        # Output folder
        tk.Label(settings_card, text="Output Folder",
                font=("Segoe UI", 10), fg=Colors.TEXT_SECONDARY,
                bg=Colors.BG_CARD).pack(anchor=tk.W, pady=(10, 0))
        
        folder_frame = tk.Frame(settings_card, bg=Colors.BG_CARD)
        folder_frame.pack(fill=tk.X, pady=(8, 0))
        
        self.folder_entry = tk.Entry(folder_frame, font=("Segoe UI", 10),
                                     bg=Colors.BG_INPUT, fg=Colors.TEXT_PRIMARY,
                                     insertbackground=Colors.TEXT_PRIMARY,
                                     relief='flat', highlightthickness=1,
                                     highlightbackground=Colors.BORDER)
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        self.folder_entry.insert(0, "Same as source")
        
        browse_btn = tk.Label(folder_frame, text="📂", cursor="hand2",
                             font=("Segoe UI", 16), fg=Colors.TEXT_SECONDARY,
                             bg=Colors.BG_CARD)
        browse_btn.pack(side=tk.RIGHT)
        browse_btn.bind("<Button-1>", lambda e: self.select_output_folder())
        
        # Convert button
        self.convert_btn = PremiumButton(right, text="🚀 Convert All",
                                         command=self.convert_all,
                                         width=280, height=50)
        self.convert_btn.pack(pady=(15, 0))
        
        # Progress section
        progress_frame = tk.Frame(right, bg=Colors.BG_DARK)
        progress_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.progress_canvas = tk.Canvas(progress_frame, height=6,
                                         bg=Colors.BG_INPUT, highlightthickness=0)
        self.progress_canvas.pack(fill=tk.X)
        
        self.status_label = tk.Label(progress_frame, text="Ready",
                                     font=("Segoe UI", 10), fg=Colors.TEXT_MUTED,
                                     bg=Colors.BG_DARK)
        self.status_label.pack(pady=(8, 0))
        
        # Stats Card
        stats_card = PremiumCard(right, padx=20, pady=15)
        stats_card.pack(fill=tk.X, pady=(15, 0))
        
        tk.Label(stats_card, text="📊 Statistics",
                font=("Segoe UI Semibold", 11), fg=Colors.TEXT_PRIMARY,
                bg=Colors.BG_CARD).pack(anchor=tk.W, pady=(0, 10))
        
        self.stats_label = tk.Label(stats_card, 
                                    text="Converted: 0\nFailed: 0\nSaved: 0 MB",
                                    font=("Segoe UI", 10), fg=Colors.TEXT_SECONDARY,
                                    bg=Colors.BG_CARD, justify="left")
        self.stats_label.pack(anchor=tk.W)
        
    def update_quality_label(self, *args):
        self.quality_label.config(text=f"{self.quality.get()}%")
        
    def add_files(self):
        """Add files to the list."""
        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.webp *.bmp *.tiff *.tif *.gif *.ico"),
            ("All files", "*.*")
        ]
        
        paths = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=filetypes
        )
        
        for path in paths:
            if path not in self.files:
                self.files.append(path)
                self.add_file_item(path)
                
        self.update_file_count()
        
    def add_folder(self):
        """Add all images from a folder."""
        folder = filedialog.askdirectory(title="Select Folder")
        
        if folder:
            for file in os.listdir(folder):
                if file.lower().endswith(self.INPUT_EXTENSIONS):
                    path = os.path.join(folder, file)
                    if path not in self.files:
                        self.files.append(path)
                        self.add_file_item(path)
                        
        self.update_file_count()
        
    def add_file_item(self, filepath):
        """Add a file item to the list."""
        if self.empty_label.winfo_exists():
            self.empty_label.destroy()
            
        item = FileListItem(self.files_frame, filepath, 
                           on_remove=self.remove_file)
        item.pack(fill=tk.X, pady=2)
        
    def remove_file(self, filepath):
        """Remove a file from the list."""
        if filepath in self.files:
            self.files.remove(filepath)
        self.update_file_count()
        
        if not self.files:
            self.empty_label = tk.Label(self.files_frame,
                                        text="No files added\n\nClick 'Add Files' or 'Add Folder' to start",
                                        font=("Segoe UI", 11), fg=Colors.TEXT_MUTED,
                                        bg=Colors.BG_CARD, justify="center")
            self.empty_label.pack(pady=50)
        
    def clear_files(self):
        """Clear all files."""
        self.files = []
        for widget in self.files_frame.winfo_children():
            widget.destroy()
            
        self.empty_label = tk.Label(self.files_frame,
                                    text="No files added\n\nClick 'Add Files' or 'Add Folder' to start",
                                    font=("Segoe UI", 11), fg=Colors.TEXT_MUTED,
                                    bg=Colors.BG_CARD, justify="center")
        self.empty_label.pack(pady=50)
        self.update_file_count()
        
    def update_file_count(self):
        """Update the file count label."""
        count = len(self.files)
        self.file_count_label.config(text=f"{count} file{'s' if count != 1 else ''}")
        
    def select_output_folder(self):
        """Select output folder."""
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder = folder
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)
            
    def update_progress(self, value):
        """Update progress bar."""
        self.progress_canvas.delete("progress")
        width = self.progress_canvas.winfo_width()
        fill_width = width * (value / 100)
        
        if fill_width > 0:
            self.progress_canvas.create_rectangle(
                0, 0, fill_width, 6,
                fill=Colors.PRIMARY, outline="", tags="progress"
            )
            
    def convert_all(self):
        """Convert all files."""
        if not self.files:
            messagebox.showwarning("No Files", "Please add some images first.")
            return
            
        thread = threading.Thread(target=self._convert_thread)
        thread.start()
        
    def _convert_thread(self):
        """Thread for converting files."""
        total = len(self.files)
        converted = 0
        failed = 0
        saved_bytes = 0
        
        output_format = self.output_format.get()
        ext = self.SUPPORTED_FORMATS[output_format]
        quality = self.quality.get()
        
        # Get output folder
        output_folder = self.output_folder
        
        for i, filepath in enumerate(self.files):
            try:
                self.root.after(0, lambda s=f"Converting {i+1}/{total}...": 
                               self.status_label.config(text=s))
                self.root.after(0, lambda p=((i+1)/total)*100: self.update_progress(p))
                
                # Open image
                img = Image.open(filepath)
                
                # Determine output path
                if output_folder:
                    out_dir = output_folder
                else:
                    out_dir = os.path.dirname(filepath)
                    
                filename = os.path.splitext(os.path.basename(filepath))[0]
                output_path = os.path.join(out_dir, f"{filename}{ext}")
                
                # Handle format-specific conversions
                if output_format in ('JPEG', 'BMP'):
                    # These formats don't support transparency
                    if img.mode in ('RGBA', 'LA', 'P'):
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                
                # Save with appropriate settings
                save_kwargs = {}
                
                if output_format == 'JPEG':
                    save_kwargs['quality'] = quality
                    save_kwargs['optimize'] = True
                elif output_format == 'WebP':
                    save_kwargs['quality'] = quality
                elif output_format == 'PNG':
                    save_kwargs['optimize'] = True
                    
                original_size = os.path.getsize(filepath)
                img.save(output_path, **save_kwargs)
                new_size = os.path.getsize(output_path)
                
                saved_bytes += original_size - new_size
                converted += 1
                
            except Exception as e:
                print(f"Error converting {filepath}: {e}")
                failed += 1
                
        # Update stats
        saved_mb = saved_bytes / (1024 * 1024)
        self.root.after(0, lambda: self.stats_label.config(
            text=f"Converted: {converted}\nFailed: {failed}\nSaved: {saved_mb:.2f} MB"
        ))
        
        self.root.after(0, lambda: self.update_progress(100))
        self.root.after(0, lambda: self.status_label.config(text="✓ Done!"))
        
        if failed == 0:
            self.root.after(0, lambda: messagebox.showinfo(
                "Success", f"All {converted} images converted successfully!"
            ))
        else:
            self.root.after(0, lambda: messagebox.showwarning(
                "Completed", f"Converted: {converted}\nFailed: {failed}"
            ))


def main():
    root = tk.Tk()
    app = ImageConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
