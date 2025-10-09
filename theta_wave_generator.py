import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import sounddevice as sd
import wave
import threading
import time

class ThetaWaveGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Brainwave Binaural Beat Generator")
        self.root.geometry("750x550")
        self.root.resizable(False, False)
        
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
        
        # Load default calm mind preset
        self.apply_preset('calm_mind')
        
    def setup_styles(self):
        """Setup custom styles for the GUI"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Header.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Info.TLabel', font=('Arial', 10), foreground='#34495e')
        style.configure('Value.TLabel', font=('Arial', 11, 'bold'), foreground='#e74c3c')
        
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Header
        header_frame = tk.Frame(self.root, bg='#3498db', height=80)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🧠 Brainwave Binaural Beat Generator",
                               font=('Arial', 18, 'bold'), bg='#3498db', fg='white')
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(header_frame, text="Calm Mind • Focus & Study • Deep Sleep",
                                 font=('Arial', 10), bg='#3498db', fg='#ecf0f1')
        subtitle_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, padx=30, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Quick Start Section (NEW!)
        quick_start_frame = tk.LabelFrame(content_frame, text="⚡ Quick Start - Choose Your Goal",
                                          font=('Arial', 13, 'bold'), padx=20, pady=20,
                                          bg='#f8f9fa', relief='raised', bd=2)
        quick_start_frame.pack(fill='x', pady=(0, 20))
        
        quick_label = tk.Label(quick_start_frame, 
                              text="Click a preset and then Play - That's it! 🎧",
                              font=('Arial', 11), bg='#f8f9fa', fg='#2c3e50')
        quick_label.pack(pady=(0, 15))
        
        presets_frame = tk.Frame(quick_start_frame, bg='#f8f9fa')
        presets_frame.pack()
        
        # Preset buttons
        btn_config = {'font': ('Arial', 11, 'bold'), 'width': 18, 'height': 3, 'relief': 'raised', 'bd': 3}
        
        calm_mind_btn = tk.Button(presets_frame, text="🧠 Stop Overthinking\nCalm Mind\n(7.83 Hz)", 
                                   bg='#9b59b6', fg='white',
                                   command=lambda: self.apply_preset('calm_mind'),
                                   **btn_config)
        calm_mind_btn.grid(row=0, column=0, padx=10, pady=5)
        
        focus_btn = tk.Button(presets_frame, text="📚 Focus & Study\nLearning\n(Beta 15 Hz)",
                             bg='#3498db', fg='white',
                             command=lambda: self.apply_preset('focus'),
                             **btn_config)
        focus_btn.grid(row=0, column=1, padx=10, pady=5)
        
        deep_sleep_btn = tk.Button(presets_frame, text="😴 Deep Sleep\nHealing\n(Delta 2 Hz)",
                                  bg='#2c3e50', fg='white',
                                  command=lambda: self.apply_preset('deep_sleep'),
                                  **btn_config)
        deep_sleep_btn.grid(row=0, column=2, padx=10, pady=5)
        
        self.preset_status = tk.Label(quick_start_frame, text="👆 Select a preset above to get started",
                                     font=('Arial', 10, 'bold'), bg='#f8f9fa', fg='#7f8c8d')
        self.preset_status.pack(pady=(15, 0))
        
        # Real-time playback controls (MOVED UP FOR EASY ACCESS)
        playback_frame = tk.LabelFrame(content_frame, text="🎵 Playback Controls",
                                       font=('Arial', 12, 'bold'), padx=15, pady=15,
                                       bg='#e8f5e9', relief='raised', bd=2)
        playback_frame.pack(fill='x', pady=(0, 20))
        
        button_frame = tk.Frame(playback_frame, bg='#e8f5e9')
        button_frame.pack()
        
        self.play_button = tk.Button(button_frame, text="▶️ PLAY", command=self.play_audio,
                                     font=('Arial', 14, 'bold'), bg='#27ae60', fg='white',
                                     padx=50, pady=15, relief='raised', bd=4)
        self.play_button.pack(side='left', padx=10)
        
        self.stop_button = tk.Button(button_frame, text="⏹️ STOP", command=self.stop_audio,
                                     font=('Arial', 14, 'bold'), bg='#e74c3c', fg='white',
                                     padx=50, pady=15, relief='raised', bd=4, state='disabled')
        self.stop_button.pack(side='left', padx=10)
        
        self.status_label = tk.Label(playback_frame, text="Status: Stopped",
                                     font=('Arial', 11, 'bold'), bg='#e8f5e9', fg='#7f8c8d')
        self.status_label.pack(pady=(15, 0))
        
        # Collapsible Advanced Settings
        self.show_advanced = tk.BooleanVar(value=False)
        advanced_toggle_frame = tk.Frame(content_frame)
        advanced_toggle_frame.pack(fill='x', pady=(0, 10))
        
        self.advanced_toggle_btn = tk.Button(advanced_toggle_frame, 
                                            text="▼ Show Advanced Settings",
                                            command=self.toggle_advanced,
                                            font=('Arial', 10), bg='#ecf0f1', 
                                            relief='flat', bd=0, cursor='hand2')
        self.advanced_toggle_btn.pack()
        
        # Settings frame (Initially hidden)
        self.settings_container = tk.Frame(content_frame)
        
        settings_frame = tk.LabelFrame(self.settings_container, text="⚙️ Advanced Audio Settings",
                                       font=('Arial', 12, 'bold'), padx=15, pady=15)
        settings_frame.pack(fill='x', pady=(0, 20))
        
        # Base Frequency
        tk.Label(settings_frame, text="Base Frequency (Hz):", font=('Arial', 10)).grid(
            row=0, column=0, sticky='w', pady=8)
        self.base_freq_var = tk.DoubleVar(value=200.0)
        base_freq_scale = ttk.Scale(settings_frame, from_=100, to=500,
                                    variable=self.base_freq_var, orient='horizontal', length=250)
        base_freq_scale.grid(row=0, column=1, padx=10)
        self.base_freq_label = tk.Label(settings_frame, text="200.0 Hz",
                                        font=('Arial', 10, 'bold'), fg='#e74c3c')
        self.base_freq_label.grid(row=0, column=2)
        base_freq_scale.configure(command=self.update_base_freq_label)
        
        # Theta Beat Frequency
        tk.Label(settings_frame, text="Theta Beat Frequency (Hz):", font=('Arial', 10)).grid(
            row=1, column=0, sticky='w', pady=8)
        self.theta_freq_var = tk.DoubleVar(value=6.0)
        theta_freq_scale = ttk.Scale(settings_frame, from_=4, to=8,
                                     variable=self.theta_freq_var, orient='horizontal', length=250)
        theta_freq_scale.grid(row=1, column=1, padx=10)
        self.theta_freq_label = tk.Label(settings_frame, text="6.0 Hz",
                                         font=('Arial', 10, 'bold'), fg='#e74c3c')
        self.theta_freq_label.grid(row=1, column=2)
        theta_freq_scale.configure(command=self.update_theta_freq_label)
        
        # Volume
        tk.Label(settings_frame, text="Volume:", font=('Arial', 10)).grid(
            row=2, column=0, sticky='w', pady=8)
        self.volume_var = tk.DoubleVar(value=0.3)
        volume_scale = ttk.Scale(settings_frame, from_=0.0, to=1.0,
                                variable=self.volume_var, orient='horizontal', length=250)
        volume_scale.grid(row=2, column=1, padx=10)
        self.volume_label = tk.Label(settings_frame, text="30%",
                                     font=('Arial', 10, 'bold'), fg='#e74c3c')
        self.volume_label.grid(row=2, column=2)
        volume_scale.configure(command=self.update_volume_label)
        
        # Duration for export
        tk.Label(settings_frame, text="Duration (minutes):", font=('Arial', 10)).grid(
            row=3, column=0, sticky='w', pady=8)
        self.duration_var = tk.DoubleVar(value=5.0)
        duration_scale = ttk.Scale(settings_frame, from_=1, to=60,
                                   variable=self.duration_var, orient='horizontal', length=250)
        duration_scale.grid(row=3, column=1, padx=10)
        self.duration_label = tk.Label(settings_frame, text="5.0 min",
                                       font=('Arial', 10, 'bold'), fg='#e74c3c')
        self.duration_label.grid(row=3, column=2)
        duration_scale.configure(command=self.update_duration_label)
        
        # Export controls (in advanced settings)
        export_frame = tk.LabelFrame(self.settings_container, text="💾 Export Audio File",
                                     font=('Arial', 12, 'bold'), padx=15, pady=15)
        export_frame.pack(fill='x')
        
        export_button = tk.Button(export_frame, text="📁 Save to WAV File",
                                 command=self.export_audio,
                                 font=('Arial', 12, 'bold'), bg='#3498db', fg='white',
                                 padx=20, pady=10, relief='raised', bd=3)
        export_button.pack()
        
        export_info = tk.Label(export_frame, 
                              text="Creates a binaural beat audio file with specified duration",
                              font=('Arial', 9), fg='#7f8c8d')
        export_info.pack(pady=(10, 0))
        
    def apply_preset(self, preset_type):
        """Apply a preset configuration"""
        presets = {
            'calm_mind': {
                'base_freq': 200.0,
                'theta_freq': 7.83,
                'volume': 0.3,
                'duration': 20.0,
                'name': '🧠 Stop Overthinking / Calm Mind',
                'color': '#9b59b6',
                'description': 'Schumann Resonance - 7.83 Hz'
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
        self.duration_var.set(preset['duration'])
        
        # Update labels
        self.update_base_freq_label(preset['base_freq'])
        self.update_theta_freq_label(preset['theta_freq'])
        self.update_volume_label(preset['volume'])
        self.update_duration_label(preset['duration'])
        
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
            self.advanced_toggle_btn.config(text="▼ Show Advanced Settings")
            self.show_advanced.set(False)
        else:
            # Show advanced settings
            self.settings_container.pack(fill='x', pady=(0, 20))
            self.advanced_toggle_btn.config(text="▲ Hide Advanced Settings")
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
        self.status_label.config(text="Status: Playing ♪", fg='#27ae60')
        
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
        self.status_label.config(text="Status: Stopped", fg='#7f8c8d')
        
    def export_audio(self):
        """Export binaural beat to WAV file"""
        try:
            # Ask for save location
            filename = filedialog.asksaveasfilename(
                defaultextension=".wav",
                filetypes=[("WAV files", "*.wav"), ("All files", "*.*")],
                initialfile=f"theta_wave_{self.theta_freq_var.get():.1f}hz.wav"
            )
            
            if not filename:
                return
                
            # Show progress
            self.status_label.config(text="Generating audio file...", fg='#f39c12')
            self.root.update()
            
            # Generate audio for specified duration
            duration_minutes = self.duration_var.get()
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
                
            self.status_label.config(text="Status: Export successful! ✓", fg='#27ae60')
            messagebox.showinfo("Success", 
                               f"Audio file saved successfully!\n\n"
                               f"Duration: {duration_minutes:.1f} minutes\n"
                               f"Theta Frequency: {self.theta_freq_var.get():.1f} Hz\n"
                               f"File: {filename}")
            
        except Exception as e:
            self.status_label.config(text="Status: Export failed", fg='#e74c3c')
            messagebox.showerror("Export Error", f"Failed to export audio:\n{str(e)}")
            
    def on_closing(self):
        """Handle window closing"""
        self.stop_audio()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ThetaWaveGenerator(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()

