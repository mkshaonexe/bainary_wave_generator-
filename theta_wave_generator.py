import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import sounddevice as sd
import wave
import threading
import time
import subprocess
import os

class ThetaWaveGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("ADHD Focus Generator - 850 Hz Binaural Beat")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        self.root.resizable(True, True)
        
        # Audio parameters
        self.sample_rate = 44100
        self.is_playing = False
        self.stream = None
        self.audio_thread = None
        self.audio_position = 0  # For phase continuity in continuous playback
        
        # Configure style
        self.setup_styles()
        
        # Create GUI
        self.create_widgets()
        
        # Load default ADHD preset
        self.apply_preset('adhd')
        
    def setup_styles(self):
        """Setup custom styles for the GUI"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Header.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Info.TLabel', font=('Arial', 10), foreground='#34495e')
        style.configure('Value.TLabel', font=('Arial', 11, 'bold'), foreground='#e74c3c')
        
    def create_widgets(self):
        """Create all GUI widgets with modern design"""
        
        # Configure root background
        self.root.configure(bg='#f5f6fa')
        
        # Header with gradient effect (simulated)
        header_frame = tk.Frame(self.root, bg='#6c5ce7', height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🧠 ADHD Focus Generator",
                               font=('Segoe UI', 24, 'bold'), bg='#6c5ce7', fg='white')
        title_label.pack(pady=(20, 5))
        
        subtitle_label = tk.Label(header_frame, text="850 Hz Binaural Beat for Enhanced Focus & Concentration",
                                 font=('Segoe UI', 11), bg='#6c5ce7', fg='#dfe6e9')
        subtitle_label.pack()
        
        # Main content frame with scrollable canvas
        main_container = tk.Frame(self.root, bg='#f5f6fa')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create canvas for scrolling
        canvas = tk.Canvas(main_container, bg='#f5f6fa', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient='vertical', command=canvas.yview)
        content_frame = tk.Frame(canvas, bg='#f5f6fa')
        
        content_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=content_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Quick Start Card
        quick_start_frame = tk.Frame(content_frame, bg='white', relief='solid', bd=1)
        quick_start_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(quick_start_frame, text="⚡ Quick Start", 
                font=('Segoe UI', 16, 'bold'), bg='white', fg='#2d3436').pack(anchor='w', padx=20, pady=(15, 5))
        
        tk.Label(quick_start_frame, 
                text="Ready to boost your focus? Click PLAY to start the 850 Hz ADHD focus frequency! 🎧",
                font=('Segoe UI', 10), bg='white', fg='#636e72', wraplength=800, justify='left').pack(anchor='w', padx=20, pady=(0, 15))
        
        # Preset button
        preset_btn_frame = tk.Frame(quick_start_frame, bg='white')
        preset_btn_frame.pack(pady=(0, 15))
        
        adhd_btn = tk.Button(preset_btn_frame, text="🧠 Load ADHD Focus Preset (850 Hz)", 
                            bg='#6c5ce7', fg='white', activebackground='#5f4dd1',
                            command=lambda: self.apply_preset('adhd'),
                            font=('Segoe UI', 12, 'bold'), padx=30, pady=12, 
                            relief='flat', cursor='hand2', bd=0)
        adhd_btn.pack()
        
        self.preset_status = tk.Label(quick_start_frame, text="✓ ADHD Focus preset loaded and ready!",
                                     font=('Segoe UI', 10, 'bold'), bg='white', fg='#00b894')
        self.preset_status.pack(pady=(0, 15))
        
        # Playback Controls Card
        playback_frame = tk.Frame(content_frame, bg='white', relief='solid', bd=1)
        playback_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(playback_frame, text="🎵 Playback Controls", 
                font=('Segoe UI', 16, 'bold'), bg='white', fg='#2d3436').pack(anchor='w', padx=20, pady=(15, 10))
        
        button_container = tk.Frame(playback_frame, bg='white')
        button_container.pack(pady=(0, 15))
        
        self.play_button = tk.Button(button_container, text="▶️  PLAY", command=self.play_audio,
                                     font=('Segoe UI', 14, 'bold'), bg='#00b894', fg='white',
                                     activebackground='#00a383', padx=60, pady=18, 
                                     relief='flat', cursor='hand2', bd=0)
        self.play_button.pack(side='left', padx=10)
        
        self.stop_button = tk.Button(button_container, text="⏹️  STOP", command=self.stop_audio,
                                     font=('Segoe UI', 14, 'bold'), bg='#d63031', fg='white',
                                     activebackground='#c0281f', padx=60, pady=18, 
                                     relief='flat', cursor='hand2', bd=0, state='disabled')
        self.stop_button.pack(side='left', padx=10)
        
        self.status_label = tk.Label(playback_frame, text="⚫ Status: Ready to Play",
                                     font=('Segoe UI', 11), bg='white', fg='#636e72')
        self.status_label.pack(pady=(10, 15))
        
        # Export Audio Card - ALWAYS VISIBLE
        export_card = tk.Frame(content_frame, bg='white', relief='solid', bd=1)
        export_card.pack(fill='x', pady=(0, 15))
        
        tk.Label(export_card, text="💾 Export Audio File", 
                font=('Segoe UI', 16, 'bold'), bg='white', fg='#2d3436').pack(anchor='w', padx=20, pady=(15, 5))
        
        tk.Label(export_card, 
                text="Save your ADHD focus frequency as an audio file. Choose duration and format below.",
                font=('Segoe UI', 10), bg='white', fg='#636e72', wraplength=800, justify='left').pack(anchor='w', padx=20, pady=(0, 15))
        
        # Duration input
        duration_frame = tk.Frame(export_card, bg='white')
        duration_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        tk.Label(duration_frame, text="Duration:", font=('Segoe UI', 11, 'bold'), 
                bg='white', fg='#2d3436').pack(side='left', padx=(0, 10))
        
        self.export_duration_var = tk.DoubleVar(value=10.0)
        duration_spinbox = tk.Spinbox(duration_frame, from_=1, to=120, increment=1,
                                     textvariable=self.export_duration_var,
                                     font=('Segoe UI', 11), width=8, 
                                     relief='solid', bd=1)
        duration_spinbox.pack(side='left', padx=(0, 5))
        
        tk.Label(duration_frame, text="minutes", font=('Segoe UI', 10), 
                bg='white', fg='#636e72').pack(side='left')
        
        # Export buttons
        export_btn_frame = tk.Frame(export_card, bg='white')
        export_btn_frame.pack(pady=(0, 20))
        
        export_wav_btn = tk.Button(export_btn_frame, text="📁 Save as WAV",
                                   command=self.export_wav,
                                   font=('Segoe UI', 12, 'bold'), bg='#0984e3', fg='white',
                                   activebackground='#0770c7', padx=40, pady=15, 
                                   relief='flat', cursor='hand2', bd=0)
        export_wav_btn.pack(side='left', padx=10)
        
        export_mp3_btn = tk.Button(export_btn_frame, text="🎵 Save as MP3",
                                   command=self.export_mp3,
                                   font=('Segoe UI', 12, 'bold'), bg='#fd79a8', fg='white',
                                   activebackground='#fc5c93', padx=40, pady=15, 
                                   relief='flat', cursor='hand2', bd=0)
        export_mp3_btn.pack(side='left', padx=10)
        
        # Collapsible Advanced Settings
        self.show_advanced = tk.BooleanVar(value=False)
        advanced_toggle_frame = tk.Frame(content_frame, bg='#f5f6fa')
        advanced_toggle_frame.pack(fill='x', pady=(0, 10))
        
        self.advanced_toggle_btn = tk.Button(advanced_toggle_frame, 
                                            text="⚙️ Show Advanced Settings",
                                            command=self.toggle_advanced,
                                            font=('Segoe UI', 10), bg='#dfe6e9', fg='#2d3436',
                                            activebackground='#b2bec3',
                                            relief='flat', bd=0, cursor='hand2', padx=15, pady=8)
        self.advanced_toggle_btn.pack()
        
        # Settings frame (Initially hidden)
        self.settings_container = tk.Frame(content_frame, bg='#f5f6fa')
        
        settings_frame = tk.Frame(self.settings_container, bg='white', relief='solid', bd=1)
        settings_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(settings_frame, text="⚙️ Advanced Audio Settings", 
                font=('Segoe UI', 16, 'bold'), bg='white', fg='#2d3436').pack(anchor='w', padx=20, pady=(15, 15))
        
        settings_grid = tk.Frame(settings_frame, bg='white')
        settings_grid.pack(fill='x', padx=20, pady=(0, 20))
        
        # Left Ear Frequency
        tk.Label(settings_grid, text="Left Ear Frequency (Hz):", font=('Segoe UI', 10), 
                bg='white', fg='#2d3436').grid(row=0, column=0, sticky='w', pady=12, padx=(0, 15))
        self.base_freq_var = tk.DoubleVar(value=850.0)
        base_freq_scale = ttk.Scale(settings_grid, from_=100, to=1000,
                                    variable=self.base_freq_var, orient='horizontal', length=300)
        base_freq_scale.grid(row=0, column=1, padx=10)
        self.base_freq_label = tk.Label(settings_grid, text="850.0 Hz",
                                        font=('Segoe UI', 10, 'bold'), bg='white', fg='#6c5ce7')
        self.base_freq_label.grid(row=0, column=2, padx=(10, 0))
        base_freq_scale.configure(command=self.update_base_freq_label)
        
        # Right Ear Frequency Difference
        tk.Label(settings_grid, text="Right Ear Frequency Difference (Hz):", font=('Segoe UI', 10), 
                bg='white', fg='#2d3436').grid(row=1, column=0, sticky='w', pady=12, padx=(0, 15))
        self.theta_freq_var = tk.DoubleVar(value=0.0)
        theta_freq_scale = ttk.Scale(settings_grid, from_=0, to=20,
                                     variable=self.theta_freq_var, orient='horizontal', length=300)
        theta_freq_scale.grid(row=1, column=1, padx=10)
        self.theta_freq_label = tk.Label(settings_grid, text="0.0 Hz",
                                         font=('Segoe UI', 10, 'bold'), bg='white', fg='#6c5ce7')
        self.theta_freq_label.grid(row=1, column=2, padx=(10, 0))
        theta_freq_scale.configure(command=self.update_theta_freq_label)
        
        # Volume
        tk.Label(settings_grid, text="Volume:", font=('Segoe UI', 10), 
                bg='white', fg='#2d3436').grid(row=2, column=0, sticky='w', pady=12, padx=(0, 15))
        self.volume_var = tk.DoubleVar(value=0.3)
        volume_scale = ttk.Scale(settings_grid, from_=0.0, to=1.0,
                                variable=self.volume_var, orient='horizontal', length=300)
        volume_scale.grid(row=2, column=1, padx=10)
        self.volume_label = tk.Label(settings_grid, text="30%",
                                     font=('Segoe UI', 10, 'bold'), bg='white', fg='#6c5ce7')
        self.volume_label.grid(row=2, column=2, padx=(10, 0))
        volume_scale.configure(command=self.update_volume_label)
        
        
    def apply_preset(self, preset_type):
        """Apply a preset configuration"""
        presets = {
            'adhd': {
                'base_freq': 850.0,
                'theta_freq': 0.0,
                'volume': 0.3,
                'duration': 30.0,
                'name': '🧠 ADHD Focus',
                'color': '#9b59b6',
                'description': '850 Hz Left Ear Frequency for ADHD Focus'
            },
            'calm_mind': {
                'base_freq': 200.0,
                'theta_freq': 852.0,
                'volume': 0.3,
                'duration': 20.0,
                'name': '🧠 Stop Overthinking / Calm Mind',
                'color': '#9b59b6',
                'description': 'Solfeggio Frequency - 852 Hz'
            },
            'focus': {
                'base_freq': 200.0,
                'theta_freq': 15.0,
                'volume': 0.3,
                'duration': 30.0,
                'name': '📚 Focus / Study / Learning',
                'color': '#3498db',
                'description': 'Beta Waves - 15 Hz (14-20 Hz range)'
            },
            'deep_sleep': {
                'base_freq': 200.0,
                'theta_freq': 2.0,
                'volume': 0.25,
                'duration': 60.0,
                'name': '😴 Deep Sleep / Healing',
                'color': '#2c3e50',
                'description': 'Delta Waves - 2 Hz (1-3 Hz range)'
            }
        }
        
        preset = presets[preset_type]
        
        # Apply settings
        self.base_freq_var.set(preset['base_freq'])
        self.theta_freq_var.set(preset['theta_freq'])
        self.volume_var.set(preset['volume'])
        # Note: duration_var is now export_duration_var
        
        # Update labels
        self.update_base_freq_label(preset['base_freq'])
        self.update_theta_freq_label(preset['theta_freq'])
        self.update_volume_label(preset['volume'])
        # Note: duration label update removed since we use export_duration_var now
        
        # Update status
        self.preset_status.config(
            text=f"✓ {preset['name']} preset loaded - Now click PLAY!",
            fg=preset['color']
        )
        
    def toggle_advanced(self):
        """Toggle advanced settings visibility"""
        if self.show_advanced.get():
            # Hide advanced settings
            self.settings_container.pack_forget()
            self.advanced_toggle_btn.config(text="⚙️ Show Advanced Settings")
            self.show_advanced.set(False)
        else:
            # Show advanced settings
            self.settings_container.pack(fill='x', pady=(0, 15))
            self.advanced_toggle_btn.config(text="⚙️ Hide Advanced Settings")
            self.show_advanced.set(True)
        
    def update_base_freq_label(self, value):
        """Update base frequency label"""
        self.base_freq_label.config(text=f"{float(value):.1f} Hz")
        
    def update_theta_freq_label(self, value):
        """Update theta frequency label"""
        self.theta_freq_label.config(text=f"{float(value):.1f} Hz")
        
    def update_volume_label(self, value):
        """Update volume label"""
        self.volume_label.config(text=f"{int(float(value) * 100)}%")
        
    def update_duration_label(self, value):
        """Update duration label"""
        self.duration_label.config(text=f"{float(value):.1f} min")
        
    def generate_binaural_beat(self, duration_seconds):
        """Generate binaural beat audio"""
        base_freq = self.base_freq_var.get()
        theta_freq = self.theta_freq_var.get()
        volume = self.volume_var.get()
        
        # Calculate left and right ear frequencies
        left_freq = base_freq
        right_freq = base_freq + theta_freq
        
        # Generate time array
        t = np.linspace(0, duration_seconds, int(self.sample_rate * duration_seconds), False)
        
        # Generate sine waves for left and right channels
        left_channel = volume * np.sin(2 * np.pi * left_freq * t)
        right_channel = volume * np.sin(2 * np.pi * right_freq * t)
        
        # Combine into stereo audio
        stereo_audio = np.column_stack((left_channel, right_channel))
        
        return stereo_audio.astype(np.float32)
        
    def play_audio(self):
        """Start real-time audio playback"""
        if self.is_playing:
            return
            
        self.is_playing = True
        self.play_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.status_label.config(text="🎵 Status: Playing - Focus Mode Active", fg='#00b894')
        
        # Start audio playback in a separate thread
        self.audio_thread = threading.Thread(target=self._playback_loop, daemon=True)
        self.audio_thread.start()
        
    def _playback_loop(self):
        """Continuous audio playback loop"""
        try:
            # Use a callback-based stream for truly continuous playback
            def audio_callback(outdata, frames, time_info, status):
                if status:
                    print(f'Status: {status}')
                
                # Generate audio on-the-fly
                base_freq = self.base_freq_var.get()
                theta_freq = self.theta_freq_var.get()
                volume = self.volume_var.get()
                
                # Calculate frequencies
                left_freq = base_freq
                right_freq = base_freq + theta_freq
                
                # Generate sine waves for this chunk
                t = np.arange(frames) / self.sample_rate + self.audio_position
                left_channel = volume * np.sin(2 * np.pi * left_freq * t)
                right_channel = volume * np.sin(2 * np.pi * right_freq * t)
                
                # Update position for next chunk (to maintain phase continuity)
                self.audio_position += frames / self.sample_rate
                
                # Fill output buffer
                outdata[:, 0] = left_channel
                outdata[:, 1] = right_channel
            
            # Reset audio position for phase continuity
            self.audio_position = 0
            
            # Create and start the stream
            with sd.OutputStream(channels=2, 
                                callback=audio_callback,
                                samplerate=self.sample_rate,
                                blocksize=2048):  # Smaller blocksize for lower latency
                # Keep stream running while playing
                while self.is_playing:
                    sd.sleep(100)  # Sleep in small intervals to check status
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Playback Error", str(e)))
            self.root.after(0, self.stop_audio)
            
    def stop_audio(self):
        """Stop audio playback"""
        self.is_playing = False
        sd.stop()
        
        self.play_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_label.config(text="⚫ Status: Stopped", fg='#636e72')
        
    def export_wav(self):
        """Export binaural beat to WAV file"""
        try:
            # Ask for save location
            filename = filedialog.asksaveasfilename(
                defaultextension=".wav",
                filetypes=[("WAV files", "*.wav"), ("All files", "*.*")],
                initialfile=f"adhd_focus_{self.base_freq_var.get():.0f}hz.wav"
            )
            
            if not filename:
                return
                
            # Show progress
            self.status_label.config(text="💾 Generating WAV file...", fg='#fdcb6e')
            self.root.update()
            
            # Generate audio for specified duration
            duration_minutes = self.export_duration_var.get()
            duration_seconds = duration_minutes * 60
            
            audio_data = self.generate_binaural_beat(duration_seconds)
            
            # Convert to 16-bit PCM
            audio_data_int = np.int16(audio_data * 32767)
            
            # Save to WAV file
            with wave.open(filename, 'w') as wav_file:
                wav_file.setnchannels(2)  # Stereo
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(audio_data_int.tobytes())
                
            self.status_label.config(text="✓ WAV export successful!", fg='#00b894')
            messagebox.showinfo("Success", 
                               f"WAV file saved successfully!\n\n"
                               f"Duration: {duration_minutes:.1f} minutes\n"
                               f"Left Ear Frequency: {self.base_freq_var.get():.1f} Hz\n"
                               f"Right Ear Frequency: {self.base_freq_var.get() + self.theta_freq_var.get():.1f} Hz\n"
                               f"File: {filename}")
            
        except Exception as e:
            self.status_label.config(text="❌ WAV export failed", fg='#d63031')
            messagebox.showerror("Export Error", f"Failed to export WAV file:\n{str(e)}")
            
    def export_mp3(self):
        """Export binaural beat to MP3 file"""
        try:
            # Ask for save location
            filename = filedialog.asksaveasfilename(
                defaultextension=".mp3",
                filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")],
                initialfile=f"adhd_focus_{self.base_freq_var.get():.0f}hz.mp3"
            )
            
            if not filename:
                return
                
            # Show progress
            self.status_label.config(text="🎵 Generating MP3 file...", fg='#fdcb6e')
            self.root.update()
            
            # Get current settings
            duration_minutes = self.export_duration_var.get()
            duration_seconds = duration_minutes * 60
            
            # Generate audio data
            audio_data = self.generate_binaural_beat(duration_seconds)
            
            # Convert to 16-bit PCM
            audio_data_int = np.int16(audio_data * 32767)
            
            # Create temporary WAV file
            temp_wav = filename.replace('.mp3', '_temp.wav')
            
            # Save to temporary WAV file
            with wave.open(temp_wav, 'w') as wav_file:
                wav_file.setnchannels(2)  # Stereo
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(audio_data_int.tobytes())
            
            # Try to convert WAV to MP3 using ffmpeg
            try:
                # Use ffmpeg to convert WAV to MP3
                cmd = [
                    'ffmpeg', '-i', temp_wav, '-acodec', 'mp3', 
                    '-ab', '192k', '-y', filename
                ]
                subprocess.run(cmd, check=True, capture_output=True)
                
                # Remove temporary WAV file
                os.remove(temp_wav)
                
                self.status_label.config(text="✓ MP3 export successful!", fg='#00b894')
                messagebox.showinfo("Success", 
                                   f"MP3 file saved successfully!\n\n"
                                   f"Duration: {duration_minutes:.1f} minutes\n"
                                   f"Left Ear Frequency: {self.base_freq_var.get():.1f} Hz\n"
                                   f"Right Ear Frequency: {self.base_freq_var.get() + self.theta_freq_var.get():.1f} Hz\n"
                                   f"Bitrate: 192 kbps\n"
                                   f"File: {filename}")
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                # If ffmpeg is not available, just rename the WAV file
                os.rename(temp_wav, filename.replace('.mp3', '.wav'))
                
                self.status_label.config(text="⚠️ Saved as WAV (ffmpeg not found)", fg='#fdcb6e')
                messagebox.showinfo("Export Complete", 
                                   f"Audio file saved as WAV format!\n\n"
                                   f"(MP3 conversion requires ffmpeg to be installed)\n\n"
                                   f"Duration: {duration_minutes:.1f} minutes\n"
                                   f"Left Ear Frequency: {self.base_freq_var.get():.1f} Hz\n"
                                   f"Right Ear Frequency: {self.base_freq_var.get() + self.theta_freq_var.get():.1f} Hz\n"
                                   f"File: {filename.replace('.mp3', '.wav')}")
            
        except Exception as e:
            self.status_label.config(text="❌ MP3 export failed", fg='#d63031')
            messagebox.showerror("Export Error", f"Failed to export audio:\n{str(e)}")
            
    def on_closing(self):
        """Handle window closing"""
        self.stop_audio()
        self.root.destroy()

def main():
    print("Starting ADHD Focus Generator...")
    root = tk.Tk()
    print("Tkinter window created")
    app = ThetaWaveGenerator(root)
    print("Application initialized")
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Ensure window is visible and on top
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(lambda: root.attributes('-topmost', False))
    
    print("Starting main loop...")
    root.mainloop()
    print("Application closed")

if __name__ == "__main__":
    main()

