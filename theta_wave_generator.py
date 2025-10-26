import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import sounddevice as sd
import wave
import threading
import subprocess
import os

class ModernBinauralGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Binaural Wave Generator")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Audio parameters
        self.sample_rate = 44100
        self.is_playing = False
        self.audio_position = 0
        
        # Frequency variables - Default to ADHD preset (856 Hz)
        self.left_freq_var = tk.DoubleVar(value=856)
        self.right_freq_var = tk.DoubleVar(value=856)
        self.volume_var = tk.DoubleVar(value=30)  # 0-100 scale
        self.export_duration_var = tk.IntVar(value=10)
        
        # Configure dark theme colors
        self.colors = {
            'bg_primary': '#0B1220',
            'bg_secondary': '#152238',
            'bg_tertiary': '#1C2F47',
            'accent_primary': '#00D9FF',
            'accent_secondary': '#0099CC',
            'text_primary': '#FFFFFF',
            'text_secondary': '#8B9BB3',
            'border_color': '#2A3F5F'
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Create GUI
        self.create_widgets()
        self.update_beat_display()
        
    def create_widgets(self):
        """Create the modern UI matching the web app"""
        
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Control Panel Frame (main card)
        control_panel = tk.Frame(main_frame, bg=self.colors['bg_secondary'], 
                                highlightthickness=1, highlightbackground=self.colors['border_color'])
        control_panel.pack(fill='both', pady=(0, 20))
        
        # Inner padding frame
        inner_frame = tk.Frame(control_panel, bg=self.colors['bg_secondary'])
        inner_frame.pack(fill='both', padx=60, pady=50)
        
        # Three column layout: Left Ear | Center | Right Ear
        inner_frame.columnconfigure(0, weight=1)
        inner_frame.columnconfigure(1, weight=0)
        inner_frame.columnconfigure(2, weight=1)
        
        # ========== LEFT EAR CONTROL ==========
        self.create_ear_control(inner_frame, 'LEFT EAR', self.left_freq_var, 0)
        
        # ========== CENTER BEAT CONTROL ==========
        self.create_center_control(inner_frame, 1)
        
        # ========== RIGHT EAR CONTROL ==========
        self.create_ear_control(inner_frame, 'RIGHT EAR', self.right_freq_var, 2)
        
        # ========== MORE OPTIONS (Collapsible) ==========
        self.create_more_options(main_frame)
        
        # ========== STATUS BAR ==========
        self.create_status_bar(main_frame)
        
        # ========== ABOUT BUTTON ==========
        self.create_about_section(main_frame)
        
    def create_about_section(self, parent):
        """Create About button with version info"""
        about_btn_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        about_btn_frame.pack(fill='x')
        
        about_btn = tk.Button(about_btn_frame,
                            text='ℹ️ About',
                            font=('Segoe UI', 9),
                            bg=self.colors['bg_tertiary'],
                            fg=self.colors['text_secondary'],
                            activebackground=self.colors['accent_primary'],
                            activeforeground=self.colors['bg_primary'],
                            relief='flat', bd=0,
                            padx=15, pady=8,
                            cursor='hand2',
                            command=self.show_about)
        about_btn.pack(anchor='e')
        
    def show_about(self):
        """Display about information"""
        about_text = """Binaural Wave Generator
Version 0.0.5

Last Updated: October 6, 2024 at 7:45 PM
Developer: mkshaon2024@gmail.com

Features:
• ADHD Focus Preset (856 Hz)
• Custom frequency control (0-1000 Hz)
• Real-time binaural beat generation
• WAV and MP3 export
• Modern dark UI interface

Made with ❤️ for better focus and concentration"""
        
        messagebox.showinfo("About Binaural Wave Generator", about_text)
        
    def create_ear_control(self, parent, label_text, freq_var, column):
        """Create left or right ear frequency control"""
        container = tk.Frame(parent, bg=self.colors['bg_secondary'])
        container.grid(row=0, column=column, sticky='ew', padx=30)
        
        # Ear label with icon
        header_frame = tk.Frame(container, bg=self.colors['bg_secondary'])
        header_frame.pack(anchor='w' if column == 0 else 'e')
        
        ear_label = tk.Label(header_frame, text=label_text,
                            font=('Segoe UI', 10, 'bold'),
                            bg=self.colors['bg_secondary'],
                            fg=self.colors['text_secondary'])
        ear_label.pack(side='left' if column == 0 else 'right', pady=(0, 10))
        
        # Frequency display (large number)
        freq_frame = tk.Frame(container, bg=self.colors['bg_secondary'])
        freq_frame.pack(anchor='w' if column == 0 else 'e', pady=(0, 20))
        
        freq_label = tk.Label(freq_frame, text=str(int(freq_var.get())),
                             font=('Segoe UI', 56, 'bold'),
                             bg=self.colors['bg_secondary'],
                             fg=self.colors['text_primary'])
        freq_label.pack(side='left')
        
        hz_label = tk.Label(freq_frame, text='Hz',
                           font=('Segoe UI', 18),
                           bg=self.colors['bg_secondary'],
                           fg=self.colors['text_secondary'])
        hz_label.pack(side='left', padx=(8, 0), anchor='s', pady=(0, 10))
        
        # Store label reference for updates
        if column == 0:
            self.left_freq_label = freq_label
        else:
            self.right_freq_label = freq_label
        
        # Slider
        slider_frame = tk.Frame(container, bg=self.colors['bg_secondary'])
        slider_frame.pack(fill='x', pady=(0, 10))
        
        slider = tk.Scale(slider_frame, from_=0, to=1000,
                         orient='horizontal',
                         variable=freq_var,
                         showvalue=False,
                         bg=self.colors['accent_primary'],
                         fg='white',
                         activebackground=self.colors['accent_primary'],
                         highlightthickness=0,
                         highlightbackground=self.colors['bg_secondary'],
                         troughcolor=self.colors['bg_tertiary'],
                         sliderlength=30,
                         sliderrelief='raised',
                         bd=2,
                         width=12,
                         length=300,
                         command=lambda v: self.update_freq_display())
        slider.pack(fill='x')
        slider.bind('<B1-Motion>', lambda e: self.update_freq_display())
        slider.bind('<ButtonRelease-1>', lambda e: self.update_freq_display())
        
        # Slider labels
        label_frame = tk.Frame(container, bg=self.colors['bg_secondary'])
        label_frame.pack(fill='x')
        
        min_label = tk.Label(label_frame, text='0 Hz',
                            font=('Segoe UI', 9),
                            bg=self.colors['bg_secondary'],
                            fg=self.colors['text_secondary'])
        min_label.pack(side='left')
        
        max_label = tk.Label(label_frame, text='1000 Hz',
                            font=('Segoe UI', 9),
                            bg=self.colors['bg_secondary'],
                            fg=self.colors['text_secondary'])
        max_label.pack(side='right')
        
    def create_center_control(self, parent, column):
        """Create center beat control with play button"""
        container = tk.Frame(parent, bg=self.colors['bg_secondary'])
        container.grid(row=0, column=column, padx=40)
        
        # Beat adjustment buttons
        adjust_frame = tk.Frame(container, bg=self.colors['bg_secondary'])
        adjust_frame.pack(pady=(0, 15))
        
        decrease_btn = tk.Button(adjust_frame, text='-0.1',
                                font=('Segoe UI', 12, 'bold'),
                                bg=self.colors['bg_tertiary'],
                                fg=self.colors['text_primary'],
                                activebackground=self.colors['accent_primary'],
                                activeforeground=self.colors['bg_primary'],
                                relief='flat', bd=0,
                                padx=20, pady=8,
                                cursor='hand2',
                                command=lambda: self.adjust_beat(-0.1))
        decrease_btn.pack(side='left', padx=5)
        
        # Beat display
        beat_container = tk.Frame(container, bg=self.colors['bg_secondary'])
        beat_container.pack(pady=(0, 15))
        
        self.beat_value_label = tk.Label(beat_container, text='184',
                                         font=('Segoe UI', 56, 'bold'),
                                         bg=self.colors['bg_secondary'],
                                         fg=self.colors['accent_primary'])
        self.beat_value_label.pack(side='left')
        
        beat_hz_label = tk.Label(beat_container, text='Hz',
                                font=('Segoe UI', 18),
                                bg=self.colors['bg_secondary'],
                                fg=self.colors['text_secondary'])
        beat_hz_label.pack(side='left', padx=(8, 0), anchor='s', pady=(0, 10))
        
        increase_btn = tk.Button(adjust_frame, text='+0.1',
                                font=('Segoe UI', 12, 'bold'),
                                bg=self.colors['bg_tertiary'],
                                fg=self.colors['text_primary'],
                                activebackground=self.colors['accent_primary'],
                                activeforeground=self.colors['bg_primary'],
                                relief='flat', bd=0,
                                padx=20, pady=8,
                                cursor='hand2',
                                command=lambda: self.adjust_beat(0.1))
        increase_btn.pack(side='left', padx=5)
        
        # Play button (circular)
        play_btn_frame = tk.Frame(container, bg=self.colors['bg_secondary'])
        play_btn_frame.pack(pady=(0, 15))
        
        self.play_button = tk.Button(play_btn_frame, text='▶',
                                     font=('Segoe UI', 28),
                                     bg=self.colors['bg_tertiary'],
                                     fg=self.colors['accent_primary'],
                                     activebackground=self.colors['accent_primary'],
                                     activeforeground=self.colors['bg_primary'],
                                     relief='flat', bd=0,
                                     width=3, height=1,
                                     cursor='hand2',
                                     command=self.toggle_playback)
        self.play_button.pack()
        
        # Binaural Beat label
        beat_label = tk.Label(container, text='BINAURAL BEAT',
                            font=('Segoe UI', 9, 'bold'),
                            bg=self.colors['bg_secondary'],
                            fg=self.colors['text_secondary'])
        beat_label.pack()
        
    def create_more_options(self, parent):
        """Create collapsible More Options section"""
        # More Options button
        self.more_options_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        self.more_options_frame.pack(fill='x', pady=(0, 20))
        
        self.more_options_btn = tk.Button(self.more_options_frame,
                                         text='More Options ▼',
                                         font=('Segoe UI', 11),
                                         bg=self.colors['bg_secondary'],
                                         fg=self.colors['text_primary'],
                                         activebackground=self.colors['bg_tertiary'],
                                         relief='flat', bd=0,
                                         padx=20, pady=12,
                                         cursor='hand2',
                                         command=self.toggle_more_options)
        self.more_options_btn.pack(fill='x')
        
        # Options content (initially hidden)
        self.options_content = tk.Frame(parent, bg=self.colors['bg_secondary'],
                                       highlightthickness=1,
                                       highlightbackground=self.colors['border_color'])
        
        inner_options = tk.Frame(self.options_content, bg=self.colors['bg_secondary'])
        inner_options.pack(fill='both', padx=30, pady=20)
        
        # Volume Control
        volume_label = tk.Label(inner_options, text='VOLUME',
                              font=('Segoe UI', 9, 'bold'),
                              bg=self.colors['bg_secondary'],
                              fg=self.colors['text_secondary'])
        volume_label.pack(anchor='w', pady=(0, 10))
        
        volume_frame = tk.Frame(inner_options, bg=self.colors['bg_secondary'])
        volume_frame.pack(fill='x', pady=(0, 20))
        
        self.volume_slider = tk.Scale(volume_frame, from_=0, to=100,
                                     orient='horizontal',
                                     variable=self.volume_var,
                                     showvalue=False,
                                     bg=self.colors['accent_primary'],
                                     fg='white',
                                     activebackground=self.colors['accent_primary'],
                                     highlightthickness=0,
                                     troughcolor=self.colors['bg_tertiary'],
                                     sliderlength=25,
                                     sliderrelief='raised',
                                     bd=2,
                                     width=12,
                                     command=self.update_volume_label)
        self.volume_slider.pack(side='left', fill='x', expand=True)
        
        self.volume_value_label = tk.Label(volume_frame, text='30%',
                                          font=('Segoe UI', 10, 'bold'),
                                          bg=self.colors['bg_secondary'],
                                          fg=self.colors['text_primary'],
                                          width=6)
        self.volume_value_label.pack(side='left', padx=(10, 0))
        
        # Presets
        presets_label = tk.Label(inner_options, text='PRESETS',
                               font=('Segoe UI', 9, 'bold'),
                               bg=self.colors['bg_secondary'],
                               fg=self.colors['text_secondary'])
        presets_label.pack(anchor='w', pady=(0, 10))
        
        presets_grid = tk.Frame(inner_options, bg=self.colors['bg_secondary'])
        presets_grid.pack(fill='x', pady=(0, 20))
        
        # Define presets matching web app
        presets = [
            ('Theta', '6 Hz', 200, 206),
            ('Alpha', '10 Hz', 200, 210),
            ('Beta', '15 Hz', 200, 215),
            ('Study', '14 Hz', 440, 454),
            ('Calm', '8 Hz', 400, 408),
            ('Sleep', '3 Hz', 200, 203),
            ('Wake', '25 Hz', 500, 525),
            ('ADHD', '0 Hz', 856, 856)
        ]
        
        for i, (name, beat, left, right) in enumerate(presets):
            row = i // 4
            col = i % 4
            
            btn = tk.Button(presets_grid, text=f'{name}\n{beat}',
                          font=('Segoe UI', 9),
                          bg=self.colors['bg_tertiary'],
                          fg=self.colors['text_primary'],
                          activebackground=self.colors['accent_primary'],
                          activeforeground=self.colors['bg_primary'],
                          relief='flat', bd=0,
                          padx=15, pady=10,
                          cursor='hand2',
                          command=lambda l=left, r=right: self.apply_preset(l, r))
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            presets_grid.columnconfigure(col, weight=1)
        
        # Export Audio
        export_label = tk.Label(inner_options, text='EXPORT AUDIO',
                              font=('Segoe UI', 9, 'bold'),
                              bg=self.colors['bg_secondary'],
                              fg=self.colors['text_secondary'])
        export_label.pack(anchor='w', pady=(0, 10))
        
        export_frame = tk.Frame(inner_options, bg=self.colors['bg_secondary'])
        export_frame.pack(fill='x')
        
        duration_spinbox = tk.Spinbox(export_frame, from_=1, to=120,
                                      textvariable=self.export_duration_var,
                                      font=('Segoe UI', 11),
                                      bg=self.colors['bg_tertiary'],
                                      fg=self.colors['text_primary'],
                                      buttonbackground=self.colors['bg_tertiary'],
                                      relief='flat', bd=0,
                                      width=8)
        duration_spinbox.pack(side='left', padx=(0, 5))
        
        duration_label = tk.Label(export_frame, text='minutes',
                                font=('Segoe UI', 10),
                                bg=self.colors['bg_secondary'],
                                fg=self.colors['text_secondary'])
        duration_label.pack(side='left', padx=(0, 15))
        
        export_wav_btn = tk.Button(export_frame, text='Export WAV',
                                  font=('Segoe UI', 10, 'bold'),
                                  bg=self.colors['accent_primary'],
                                  fg=self.colors['bg_primary'],
                                  activebackground=self.colors['accent_secondary'],
                                  relief='flat', bd=0,
                                  padx=20, pady=8,
                                  cursor='hand2',
                                  command=self.export_wav)
        export_wav_btn.pack(side='left', padx=5)
        
        export_mp3_btn = tk.Button(export_frame, text='Export MP3',
                                  font=('Segoe UI', 10, 'bold'),
                                  bg='#fd79a8',
                                  fg='#ffffff',
                                  activebackground='#fc5c93',
                                  relief='flat', bd=0,
                                  padx=20, pady=8,
                                  cursor='hand2',
                                  command=self.export_mp3)
        export_mp3_btn.pack(side='left', padx=5)
        
    def create_status_bar(self, parent):
        """Create status bar at bottom"""
        status_frame = tk.Frame(parent, bg=self.colors['bg_secondary'],
                               highlightthickness=1,
                               highlightbackground=self.colors['border_color'])
        status_frame.pack(fill='x')
        
        status_inner = tk.Frame(status_frame, bg=self.colors['bg_secondary'])
        status_inner.pack(pady=12)
        
        # Status indicator (dot)
        self.status_indicator = tk.Label(status_inner, text='●',
                                        font=('Segoe UI', 12),
                                        bg=self.colors['bg_secondary'],
                                        fg=self.colors['text_secondary'])
        self.status_indicator.pack(side='left', padx=(0, 8))
        
        self.status_text = tk.Label(status_inner, text='Ready',
                                   font=('Segoe UI', 10),
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['text_secondary'])
        self.status_text.pack(side='left')
        
    def update_freq_display(self):
        """Update frequency displays and beat"""
        self.left_freq_label.config(text=str(int(self.left_freq_var.get())))
        self.right_freq_label.config(text=str(int(self.right_freq_var.get())))
        self.update_beat_display()
        
        if self.is_playing:
            self.update_audio_frequencies()
        
    def update_beat_display(self):
        """Update binaural beat display"""
        beat = abs(self.left_freq_var.get() - self.right_freq_var.get())
        self.beat_value_label.config(text=str(int(beat)))
        
    def adjust_beat(self, amount):
        """Adjust the right ear frequency to change beat"""
        new_right = self.right_freq_var.get() + amount
        if 0 <= new_right <= 1000:
            self.right_freq_var.set(new_right)
            self.update_freq_display()
        
    def update_volume_label(self, value=None):
        """Update volume label"""
        vol = int(self.volume_var.get())
        self.volume_value_label.config(text=f'{vol}%')
        if self.is_playing:
            self.update_audio_volume()
        
    def toggle_more_options(self):
        """Toggle More Options section"""
        if self.options_content.winfo_ismapped():
            self.options_content.pack_forget()
            self.more_options_btn.config(text='More Options ▼')
        else:
            self.options_content.pack(fill='x', before=self.more_options_frame, pady=(0, 20))
            self.more_options_btn.config(text='More Options ▲')
        
    def apply_preset(self, left_freq, right_freq):
        """Apply frequency preset"""
        self.left_freq_var.set(left_freq)
        self.right_freq_var.set(right_freq)
        self.update_freq_display()
        
    def toggle_playback(self):
        """Toggle play/stop"""
        if self.is_playing:
            self.stop_audio()
        else:
            self.play_audio()
        
    def play_audio(self):
        """Start audio playback"""
        if self.is_playing:
            return
            
        self.is_playing = True
        self.play_button.config(text='⏸', bg=self.colors['accent_primary'],
                               fg=self.colors['bg_primary'])
        self.status_indicator.config(fg=self.colors['accent_primary'])
        self.status_text.config(text='Playing', fg=self.colors['accent_primary'])
        
        # Start audio thread
        self.audio_thread = threading.Thread(target=self._playback_loop, daemon=True)
        self.audio_thread.start()
        
    def _playback_loop(self):
        """Continuous audio playback loop"""
        try:
            def audio_callback(outdata, frames, time_info, status):
                if status:
                    print(f'Status: {status}')
                
                left_freq = self.left_freq_var.get()
                right_freq = self.right_freq_var.get()
                volume = self.volume_var.get() / 100.0
                
                t = np.arange(frames) / self.sample_rate + self.audio_position
                left_channel = volume * np.sin(2 * np.pi * left_freq * t)
                right_channel = volume * np.sin(2 * np.pi * right_freq * t)
                
                self.audio_position += frames / self.sample_rate
                
                outdata[:, 0] = left_channel
                outdata[:, 1] = right_channel
            
            self.audio_position = 0
            
            with sd.OutputStream(channels=2, 
                                callback=audio_callback,
                                samplerate=self.sample_rate,
                                blocksize=2048):
                while self.is_playing:
                    sd.sleep(100)
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Playback Error", str(e)))
            self.root.after(0, self.stop_audio)
            
    def stop_audio(self):
        """Stop audio playback"""
        self.is_playing = False
        sd.stop()
        
        self.play_button.config(text='▶', bg=self.colors['bg_tertiary'],
                               fg=self.colors['accent_primary'])
        self.status_indicator.config(fg=self.colors['text_secondary'])
        self.status_text.config(text='Ready', fg=self.colors['text_secondary'])
        
    def update_audio_frequencies(self):
        """Update frequencies during playback (audio regenerates automatically)"""
        pass  # The callback handles this automatically
        
    def update_audio_volume(self):
        """Update volume during playback (audio regenerates automatically)"""
        pass  # The callback handles this automatically
        
    def generate_binaural_beat(self, duration_seconds):
        """Generate binaural beat audio for export"""
        left_freq = self.left_freq_var.get()
        right_freq = self.right_freq_var.get()
        volume = self.volume_var.get() / 100.0
        
        t = np.linspace(0, duration_seconds, int(self.sample_rate * duration_seconds), False)
        
        left_channel = volume * np.sin(2 * np.pi * left_freq * t)
        right_channel = volume * np.sin(2 * np.pi * right_freq * t)
        
        stereo_audio = np.column_stack((left_channel, right_channel))
        
        return stereo_audio.astype(np.float32)
        
    def export_wav(self):
        """Export to WAV file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".wav",
                filetypes=[("WAV files", "*.wav"), ("All files", "*.*")],
                initialfile=f"binaural_{int(self.left_freq_var.get())}-{int(self.right_freq_var.get())}.wav"
            )
            
            if not filename:
                return
                
            self.status_text.config(text='Generating audio...', fg='#fdcb6e')
            self.root.update()
            
            duration_minutes = self.export_duration_var.get()
            duration_seconds = duration_minutes * 60
            
            audio_data = self.generate_binaural_beat(duration_seconds)
            audio_data_int = np.int16(audio_data * 32767)
            
            with wave.open(filename, 'w') as wav_file:
                wav_file.setnchannels(2)
                wav_file.setsampwidth(2)
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(audio_data_int.tobytes())
                
            self.status_text.config(text='Export successful!', fg='#00b894')
            messagebox.showinfo("Success", 
                               f"WAV file saved successfully!\n\n"
                               f"Duration: {duration_minutes} minutes\n"
                               f"Left: {int(self.left_freq_var.get())} Hz\n"
                               f"Right: {int(self.right_freq_var.get())} Hz\n"
                               f"File: {filename}")
            
            self.root.after(3000, lambda: self.status_text.config(text='Ready',
                                                                  fg=self.colors['text_secondary']))
            
        except Exception as e:
            self.status_text.config(text='Export failed', fg='#d63031')
            messagebox.showerror("Export Error", f"Failed to export WAV:\n{str(e)}")
            
    def export_mp3(self):
        """Export to MP3 file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".mp3",
                filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")],
                initialfile=f"binaural_{int(self.left_freq_var.get())}-{int(self.right_freq_var.get())}.mp3"
            )
            
            if not filename:
                return
                
            self.status_text.config(text='Generating audio...', fg='#fdcb6e')
            self.root.update()
            
            duration_minutes = self.export_duration_var.get()
            duration_seconds = duration_minutes * 60
            
            audio_data = self.generate_binaural_beat(duration_seconds)
            audio_data_int = np.int16(audio_data * 32767)
            
            temp_wav = filename.replace('.mp3', '_temp.wav')
            
            with wave.open(temp_wav, 'w') as wav_file:
                wav_file.setnchannels(2)
                wav_file.setsampwidth(2)
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(audio_data_int.tobytes())
            
            try:
                cmd = ['ffmpeg', '-i', temp_wav, '-acodec', 'mp3', 
                       '-ab', '192k', '-y', filename]
                subprocess.run(cmd, check=True, capture_output=True)
                os.remove(temp_wav)
                
                self.status_text.config(text='Export successful!', fg='#00b894')
                messagebox.showinfo("Success", 
                                   f"MP3 file saved successfully!\n\n"
                                   f"Duration: {duration_minutes} minutes\n"
                                   f"Left: {int(self.left_freq_var.get())} Hz\n"
                                   f"Right: {int(self.right_freq_var.get())} Hz\n"
                                   f"Bitrate: 192 kbps\n"
                                   f"File: {filename}")
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                os.rename(temp_wav, filename.replace('.mp3', '.wav'))
                self.status_text.config(text='Saved as WAV (ffmpeg not found)', fg='#fdcb6e')
                messagebox.showinfo("Note", 
                                   f"Audio saved as WAV format.\n\n"
                                   f"(MP3 conversion requires ffmpeg)\n\n"
                                   f"File: {filename.replace('.mp3', '.wav')}")
            
            self.root.after(3000, lambda: self.status_text.config(text='Ready',
                                                                  fg=self.colors['text_secondary']))
            
        except Exception as e:
            self.status_text.config(text='Export failed', fg='#d63031')
            messagebox.showerror("Export Error", f"Failed to export audio:\n{str(e)}")
            
    def on_closing(self):
        """Handle window closing"""
        self.stop_audio()
        self.root.destroy()

def main():
    print("Starting Binaural Wave Generator...")
    root = tk.Tk()
    app = ModernBinauralGenerator(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Ensure window is visible
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(lambda: root.attributes('-topmost', False))
    
    root.mainloop()

if __name__ == "__main__":
    main()
