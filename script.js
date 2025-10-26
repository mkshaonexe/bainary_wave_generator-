// Modern Binaural Wave Generator - JavaScript
// Professional audio engine with Web Audio API

class BinauralGenerator {
    constructor() {
        // Audio context and nodes
        this.audioContext = null;
        this.leftOscillator = null;
        this.rightOscillator = null;
        this.leftGain = null;
        this.rightGain = null;
        this.isPlaying = false;
        
        // DOM elements
        this.elements = {
            leftFreq: document.getElementById('leftFreq'),
            rightFreq: document.getElementById('rightFreq'),
            leftFreqValue: document.getElementById('leftFreqValue'),
            rightFreqValue: document.getElementById('rightFreqValue'),
            beatValue: document.getElementById('beatValue'),
            playBtn: document.getElementById('playBtn'),
            decreaseBeat: document.getElementById('decreaseBeat'),
            increaseBeat: document.getElementById('increaseBeat'),
            volume: document.getElementById('volume'),
            volumeValue: document.getElementById('volumeValue'),
            toggleControls: document.getElementById('toggleControls'),
            controlsContent: document.getElementById('controlsContent'),
            exportBtn: document.getElementById('exportBtn'),
            duration: document.getElementById('duration'),
            statusIndicator: document.getElementById('statusIndicator'),
            statusText: document.getElementById('statusText')
        };
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.updateDisplay();
    }
    
    setupEventListeners() {
    // Frequency sliders
        this.elements.leftFreq.addEventListener('input', () => {
            this.updateDisplay();
            this.updateSliderFill(this.elements.leftFreq);
            if (this.isPlaying) {
                this.updateFrequencies();
            }
        });
        
        this.elements.rightFreq.addEventListener('input', () => {
            this.updateDisplay();
            this.updateSliderFill(this.elements.rightFreq);
            if (this.isPlaying) {
                this.updateFrequencies();
            }
        });
        
        // Initialize slider fills
        this.updateSliderFill(this.elements.leftFreq);
        this.updateSliderFill(this.elements.rightFreq);
        
        // Manual frequency input handlers
        this.elements.leftFreqValue.addEventListener('input', (e) => {
            this.handleManualInput(e.target, this.elements.leftFreq);
        });
        
        this.elements.leftFreqValue.addEventListener('blur', (e) => {
            this.validateAndUpdateEditable(e.target, this.elements.leftFreq);
        });
        
        this.elements.leftFreqValue.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === 'Escape') {
                this.validateAndUpdateEditable(e.target, this.elements.leftFreq);
                e.target.blur();
            }
        });
        
        this.elements.rightFreqValue.addEventListener('input', (e) => {
            this.handleManualInput(e.target, this.elements.rightFreq);
        });
        
        this.elements.rightFreqValue.addEventListener('blur', (e) => {
            this.validateAndUpdateEditable(e.target, this.elements.rightFreq);
        });
        
        this.elements.rightFreqValue.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === 'Escape') {
                this.validateAndUpdateEditable(e.target, this.elements.rightFreq);
                e.target.blur();
            }
        });
        
        // Beat adjustment buttons
        this.elements.decreaseBeat.addEventListener('click', () => {
            this.adjustBeat(-0.1);
        });
        
        this.elements.increaseBeat.addEventListener('click', () => {
            this.adjustBeat(0.1);
        });
        
        // Play button
        this.elements.playBtn.addEventListener('click', () => {
            this.togglePlayback();
        });
        
        // Volume control
        this.elements.volume.addEventListener('input', () => {
            this.elements.volumeValue.textContent = `${this.elements.volume.value}%`;
            if (this.isPlaying) {
                this.updateVolume();
            }
        });
        
        // Toggle additional controls
        this.elements.toggleControls.addEventListener('click', () => {
            this.toggleAdditionalControls();
        });

    // Preset buttons
        document.querySelectorAll('.preset-btn').forEach(btn => {
        btn.addEventListener('click', () => {
                const left = parseFloat(btn.dataset.left);
                const right = parseFloat(btn.dataset.right);
                this.applyPreset(left, right);
            });
        });
        
        // Export button
        this.elements.exportBtn.addEventListener('click', () => {
            this.exportAudio();
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && e.target.tagName !== 'INPUT') {
                e.preventDefault();
                this.togglePlayback();
            }
        });
        
        // About button
        const aboutBtn = document.getElementById('aboutBtn');
        const aboutModal = document.getElementById('aboutModal');
        const closeBtn = aboutModal.querySelector('.close');
        
        aboutBtn.addEventListener('click', () => {
            aboutModal.style.display = 'block';
        });
        
        closeBtn.addEventListener('click', () => {
            aboutModal.style.display = 'none';
        });
        
        window.addEventListener('click', (e) => {
            if (e.target === aboutModal) {
                aboutModal.style.display = 'none';
            }
        });
    }
    
    updateDisplay() {
        const leftFreq = parseFloat(this.elements.leftFreq.value);
        const rightFreq = parseFloat(this.elements.rightFreq.value);
        const beat = Math.abs(leftFreq - rightFreq);
        
        // Update display if not currently being edited
        if (document.activeElement !== this.elements.leftFreqValue) {
            this.elements.leftFreqValue.textContent = Math.round(leftFreq);
        }
        if (document.activeElement !== this.elements.rightFreqValue) {
            this.elements.rightFreqValue.textContent = Math.round(rightFreq);
        }
        
        // Update beat display
        this.animateValue(this.elements.beatValue, Math.round(beat));
    }
    
    handleManualInput(element, sliderElement) {
        const text = element.textContent.trim();
        const value = parseFloat(text);
        
        // Allow numeric input, empty, or valid numbers
        if (!isNaN(value) && value >= 0 && value <= 1000) {
            sliderElement.value = value;
            this.updateSliderFill(sliderElement);
            if (this.isPlaying) {
                this.updateFrequencies();
            }
            // Update beat display
            const leftFreq = parseFloat(this.elements.leftFreq.value);
            const rightFreq = parseFloat(this.elements.rightFreq.value);
            const beat = Math.abs(leftFreq - rightFreq);
            this.animateValue(this.elements.beatValue, Math.round(beat));
        }
    }
    
    validateAndUpdateEditable(element, sliderElement) {
        let value = parseFloat(element.textContent.trim());
        
        // Validate and clamp to 0-1000
        if (isNaN(value) || element.textContent.trim() === '') {
            value = parseFloat(sliderElement.value);
        } else {
            value = Math.max(0, Math.min(1000, value));
        }
        
        // Update both editable element and slider
        element.textContent = Math.round(value);
        sliderElement.value = value;
        
        // Update slider fill
        this.updateSliderFill(sliderElement);
        
        // Update beat display
        const leftFreq = parseFloat(this.elements.leftFreq.value);
        const rightFreq = parseFloat(this.elements.rightFreq.value);
        const beat = Math.abs(leftFreq - rightFreq);
        this.animateValue(this.elements.beatValue, Math.round(beat));
        
        // Update audio if playing
        if (this.isPlaying) {
            this.updateFrequencies();
        }
    }
    
    animateValue(element, newValue) {
        // Add a pulse effect when value changes
        const currentValue = parseInt(element.textContent) || 0;
        
        if (currentValue !== newValue) {
            element.style.transform = 'scale(1.1)';
            element.style.color = 'var(--accent-primary)';
            
            setTimeout(() => {
                element.style.transform = 'scale(1)';
                element.style.color = '';
            }, 150);
        }
        
        element.textContent = newValue;
    }
    
    updateSliderFill(slider) {
        const value = parseFloat(slider.value);
        const min = parseFloat(slider.min);
        const max = parseFloat(slider.max);
        const percentage = ((value - min) / (max - min)) * 100;
        
        slider.style.background = `linear-gradient(to right, 
            var(--accent-primary) 0%, 
            var(--accent-primary) ${percentage}%, 
            var(--bg-tertiary) ${percentage}%, 
            var(--bg-tertiary) 100%)`;
    }
    
    adjustBeat(amount) {
        const currentRight = parseFloat(this.elements.rightFreq.value);
        const newRight = Math.max(0, Math.min(1000, currentRight + amount));
        this.elements.rightFreq.value = newRight;
        this.updateDisplay();
        this.updateSliderFill(this.elements.rightFreq);
        
        // Visual feedback for button press
        const button = amount < 0 ? this.elements.decreaseBeat : this.elements.increaseBeat;
        button.style.transform = 'scale(0.9)';
        setTimeout(() => {
            button.style.transform = '';
        }, 100);
        
        if (this.isPlaying) {
            this.updateFrequencies();
        }
    }
    
    togglePlayback() {
        if (this.isPlaying) {
            this.stop();
        } else {
            this.play();
        }
    }
    
    play() {
        try {
            // Create audio context
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            
            // Create oscillators
            this.leftOscillator = this.audioContext.createOscillator();
            this.rightOscillator = this.audioContext.createOscillator();

    // Create gain nodes
            this.leftGain = this.audioContext.createGain();
            this.rightGain = this.audioContext.createGain();
            
            // Create stereo panner for left/right separation
            const leftPanner = this.audioContext.createStereoPanner();
            const rightPanner = this.audioContext.createStereoPanner();
    leftPanner.pan.value = -1; // Full left
    rightPanner.pan.value = 1;  // Full right

            // Set oscillator type
            this.leftOscillator.type = 'sine';
            this.rightOscillator.type = 'sine';

    // Set frequencies
            this.updateFrequencies();

    // Set volume
            this.updateVolume();
            
            // Connect the audio graph
            this.leftOscillator.connect(this.leftGain);
            this.leftGain.connect(leftPanner);
            leftPanner.connect(this.audioContext.destination);
            
            this.rightOscillator.connect(this.rightGain);
            this.rightGain.connect(rightPanner);
            rightPanner.connect(this.audioContext.destination);

    // Start oscillators
            this.leftOscillator.start();
            this.rightOscillator.start();
            
            // Update state
            this.isPlaying = true;
            this.updateUI('playing');
            
        } catch (error) {
            console.error('Error starting audio:', error);
            this.setStatus('Error: Could not start audio', false);
        }
    }
    
    stop() {
        try {
    // Stop oscillators
            if (this.leftOscillator) {
                this.leftOscillator.stop();
                this.leftOscillator.disconnect();
                this.leftOscillator = null;
            }
            
            if (this.rightOscillator) {
                this.rightOscillator.stop();
                this.rightOscillator.disconnect();
                this.rightOscillator = null;
    }

    // Close audio context
            if (this.audioContext) {
                this.audioContext.close();
                this.audioContext = null;
            }
            
            // Update state
            this.isPlaying = false;
            this.updateUI('stopped');
            
        } catch (error) {
            console.error('Error stopping audio:', error);
        }
    }
    
    updateFrequencies() {
        if (!this.leftOscillator || !this.rightOscillator || !this.audioContext) return;
        
        const leftFreq = parseFloat(this.elements.leftFreq.value);
        const rightFreq = parseFloat(this.elements.rightFreq.value);
        
        this.leftOscillator.frequency.setValueAtTime(leftFreq, this.audioContext.currentTime);
        this.rightOscillator.frequency.setValueAtTime(rightFreq, this.audioContext.currentTime);
    }
    
    updateVolume() {
        if (!this.leftGain || !this.rightGain || !this.audioContext) return;
        
        const volume = parseFloat(this.elements.volume.value) / 100;
        
        this.leftGain.gain.setValueAtTime(volume, this.audioContext.currentTime);
        this.rightGain.gain.setValueAtTime(volume, this.audioContext.currentTime);
    }
    
    updateUI(state) {
        if (state === 'playing') {
            this.elements.playBtn.classList.add('playing');
            this.elements.playBtn.innerHTML = `
                <svg class="play-icon" width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
                    <rect x="6" y="4" width="4" height="16"/>
                    <rect x="14" y="4" width="4" height="16"/>
                </svg>
            `;
            this.setStatus('Playing', true);
        } else {
            this.elements.playBtn.classList.remove('playing');
            this.elements.playBtn.innerHTML = `
                <svg class="play-icon" width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M8 5v14l11-7z"/>
                </svg>
            `;
            this.setStatus('Ready', false);
        }
    }
    
    setStatus(text, active) {
        this.elements.statusText.textContent = text;
        if (active) {
            this.elements.statusIndicator.classList.add('active');
        } else {
            this.elements.statusIndicator.classList.remove('active');
        }
    }
    
    toggleAdditionalControls() {
        const content = this.elements.controlsContent;
        const button = this.elements.toggleControls;
        
        if (content.classList.contains('open')) {
            content.classList.remove('open');
            button.classList.remove('active');
        } else {
            content.classList.add('open');
            button.classList.add('active');
        }
    }
    
    applyPreset(leftFreq, rightFreq) {
        this.elements.leftFreq.value = leftFreq;
        this.elements.rightFreq.value = rightFreq;
        this.updateDisplay();
        this.updateSliderFill(this.elements.leftFreq);
        this.updateSliderFill(this.elements.rightFreq);
        
        if (this.isPlaying) {
            this.updateFrequencies();
        }
    }
    
    // Export audio functionality
    exportAudio() {
        this.setStatus('Generating audio...', false);
        
        try {
            const duration = parseInt(this.elements.duration.value) * 60; // Convert to seconds
            const sampleRate = 44100;
            const length = sampleRate * duration;
            
            // Create offline audio context for rendering
            const offlineContext = new OfflineAudioContext(2, length, sampleRate);
            
            // Create oscillators
            const leftOsc = offlineContext.createOscillator();
            const rightOsc = offlineContext.createOscillator();
            
            // Create gain nodes
            const leftGain = offlineContext.createGain();
            const rightGain = offlineContext.createGain();
            
            // Create panners
            const leftPanner = offlineContext.createStereoPanner();
            const rightPanner = offlineContext.createStereoPanner();
            leftPanner.pan.value = -1;
            rightPanner.pan.value = 1;
            
            // Configure oscillators
            leftOsc.type = 'sine';
            rightOsc.type = 'sine';
            leftOsc.frequency.value = parseFloat(this.elements.leftFreq.value);
            rightOsc.frequency.value = parseFloat(this.elements.rightFreq.value);
            
            // Set volume
            const volume = parseFloat(this.elements.volume.value) / 100;
            leftGain.gain.value = volume;
            rightGain.gain.value = volume;
            
            // Connect nodes
            leftOsc.connect(leftGain);
            leftGain.connect(leftPanner);
            leftPanner.connect(offlineContext.destination);
            
            rightOsc.connect(rightGain);
            rightGain.connect(rightPanner);
            rightPanner.connect(offlineContext.destination);
            
            // Start oscillators
            leftOsc.start(0);
            rightOsc.start(0);
            
            // Render audio
            offlineContext.startRendering().then(buffer => {
                const wav = this.audioBufferToWav(buffer);
        const blob = new Blob([wav], { type: 'audio/wav' });
                const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
                a.download = `binaural_${Math.round(leftOsc.frequency.value)}-${Math.round(rightOsc.frequency.value)}_${this.elements.duration.value}min.wav`;
        a.click();

                URL.revokeObjectURL(url);
        
                this.setStatus('Export successful!', false);
        setTimeout(() => {
                    this.setStatus(this.isPlaying ? 'Playing' : 'Ready', this.isPlaying);
        }, 3000);
            }).catch(error => {
                console.error('Export error:', error);
                this.setStatus('Export failed', false);
            });
            
    } catch (error) {
        console.error('Export error:', error);
            this.setStatus('Export failed', false);
        }
    }
    
    // Convert AudioBuffer to WAV format
    audioBufferToWav(buffer) {
    const length = buffer.length * buffer.numberOfChannels * 2 + 44;
    const arrayBuffer = new ArrayBuffer(length);
    const view = new DataView(arrayBuffer);
    const channels = [];
    let offset = 0;
    let pos = 0;
        
        // Helper functions
        const setUint16 = (data) => {
            view.setUint16(pos, data, true);
            pos += 2;
        };
        
        const setUint32 = (data) => {
            view.setUint32(pos, data, true);
            pos += 4;
        };

    // Write WAV header
    setUint32(0x46464952); // "RIFF"
    setUint32(length - 8); // file length - 8
    setUint32(0x45564157); // "WAVE"

    setUint32(0x20746d66); // "fmt " chunk
    setUint32(16); // length = 16
    setUint16(1); // PCM (uncompressed)
    setUint16(buffer.numberOfChannels);
    setUint32(buffer.sampleRate);
    setUint32(buffer.sampleRate * 2 * buffer.numberOfChannels); // avg. bytes/sec
    setUint16(buffer.numberOfChannels * 2); // block-align
    setUint16(16); // 16-bit

        setUint32(0x61746164); // "data" chunk
    setUint32(length - pos - 4); // chunk length

    // Write interleaved data
    for (let i = 0; i < buffer.numberOfChannels; i++) {
        channels.push(buffer.getChannelData(i));
    }

    while (pos < length) {
        for (let i = 0; i < buffer.numberOfChannels; i++) {
            let sample = Math.max(-1, Math.min(1, channels[i][offset]));
            sample = sample < 0 ? sample * 0x8000 : sample * 0x7FFF;
            view.setInt16(pos, sample, true);
            pos += 2;
        }
        offset++;
    }

    return arrayBuffer;
    }
}

// Initialize the application
let generator;

document.addEventListener('DOMContentLoaded', () => {
    generator = new BinauralGenerator();
});

// Clean up on page unload
window.addEventListener('beforeunload', () => {
    if (generator && generator.isPlaying) {
        generator.stop();
    }
});
