// Audio Context and Oscillators
let audioContext = null;
let leftOscillator = null;
let rightOscillator = null;
let leftGain = null;
let rightGain = null;
let isPlaying = false;

// Get DOM elements
const leftFreqSlider = document.getElementById('leftFreq');
const rightFreqSlider = document.getElementById('rightFreq');
const leftFreqValue = document.getElementById('leftFreqValue');
const rightFreqValue = document.getElementById('rightFreqValue');
const beatValue = document.getElementById('beatValue');
const volumeSlider = document.getElementById('volume');
const volumeValue = document.getElementById('volumeValue');
const playBtn = document.getElementById('playBtn');
const stopBtn = document.getElementById('stopBtn');
const statusIcon = document.getElementById('statusIcon');
const statusText = document.getElementById('statusText');
const presetButtons = document.querySelectorAll('.preset-btn');
const exportWavBtn = document.getElementById('exportWavBtn');
const exportMp3Btn = document.getElementById('exportMp3Btn');
const durationInput = document.getElementById('duration');

// Initialize
function init() {
    updateFrequencyDisplay();
    updateBeatDisplay();
    setupEventListeners();
}

// Setup Event Listeners
function setupEventListeners() {
    // Frequency sliders
    leftFreqSlider.addEventListener('input', () => {
        updateFrequencyDisplay();
        updateBeatDisplay();
        if (isPlaying) {
            updateOscillatorFrequencies();
        }
    });

    rightFreqSlider.addEventListener('input', () => {
        updateFrequencyDisplay();
        updateBeatDisplay();
        if (isPlaying) {
            updateOscillatorFrequencies();
        }
    });

    // Volume slider
    volumeSlider.addEventListener('input', () => {
        const volume = volumeSlider.value;
        volumeValue.textContent = `${volume}%`;
        if (isPlaying) {
            updateVolume();
        }
    });

    // Playback buttons
    playBtn.addEventListener('click', startAudio);
    stopBtn.addEventListener('click', stopAudio);

    // Preset buttons
    presetButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const leftFreq = btn.dataset.left;
            const rightFreq = btn.dataset.right;
            applyPreset(leftFreq, rightFreq);
            
            // Update active state
            presetButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });

    // Export buttons
    exportWavBtn.addEventListener('click', exportWAV);
    exportMp3Btn.addEventListener('click', exportMP3);
}

// Update Frequency Display
function updateFrequencyDisplay() {
    const leftFreq = leftFreqSlider.value;
    const rightFreq = rightFreqSlider.value;
    leftFreqValue.textContent = `${leftFreq} Hz`;
    rightFreqValue.textContent = `${rightFreq} Hz`;
}

// Update Beat Display
function updateBeatDisplay() {
    const leftFreq = parseInt(leftFreqSlider.value);
    const rightFreq = parseInt(rightFreqSlider.value);
    const beat = Math.abs(rightFreq - leftFreq);
    beatValue.textContent = `${beat} Hz`;
}

// Apply Preset
function applyPreset(leftFreq, rightFreq) {
    leftFreqSlider.value = leftFreq;
    rightFreqSlider.value = rightFreq;
    updateFrequencyDisplay();
    updateBeatDisplay();
    
    if (isPlaying) {
        updateOscillatorFrequencies();
    }
}

// Start Audio
function startAudio() {
    if (isPlaying) return;

    // Create Audio Context
    audioContext = new (window.AudioContext || window.webkitAudioContext)();

    // Create oscillators for left and right channels
    leftOscillator = audioContext.createOscillator();
    rightOscillator = audioContext.createOscillator();

    // Create gain nodes
    leftGain = audioContext.createGain();
    rightGain = audioContext.createGain();

    // Create stereo panner for left and right separation
    const leftPanner = audioContext.createStereoPanner();
    const rightPanner = audioContext.createStereoPanner();
    leftPanner.pan.value = -1; // Full left
    rightPanner.pan.value = 1;  // Full right

    // Set oscillator types
    leftOscillator.type = 'sine';
    rightOscillator.type = 'sine';

    // Set frequencies
    updateOscillatorFrequencies();

    // Set volume
    updateVolume();

    // Connect nodes
    leftOscillator.connect(leftGain);
    leftGain.connect(leftPanner);
    leftPanner.connect(audioContext.destination);

    rightOscillator.connect(rightGain);
    rightGain.connect(rightPanner);
    rightPanner.connect(audioContext.destination);

    // Start oscillators
    leftOscillator.start();
    rightOscillator.start();

    // Update UI
    isPlaying = true;
    playBtn.disabled = true;
    stopBtn.disabled = false;
    updateStatus('playing', '🎵 Playing - Focus Mode Active');
}

// Stop Audio
function stopAudio() {
    if (!isPlaying) return;

    // Stop oscillators
    if (leftOscillator) {
        leftOscillator.stop();
        leftOscillator.disconnect();
        leftOscillator = null;
    }

    if (rightOscillator) {
        rightOscillator.stop();
        rightOscillator.disconnect();
        rightOscillator = null;
    }

    // Close audio context
    if (audioContext) {
        audioContext.close();
        audioContext = null;
    }

    // Update UI
    isPlaying = false;
    playBtn.disabled = false;
    stopBtn.disabled = true;
    updateStatus('stopped', '⚫ Stopped');
}

// Update Oscillator Frequencies
function updateOscillatorFrequencies() {
    if (!leftOscillator || !rightOscillator) return;

    const leftFreq = parseFloat(leftFreqSlider.value);
    const rightFreq = parseFloat(rightFreqSlider.value);

    leftOscillator.frequency.setValueAtTime(leftFreq, audioContext.currentTime);
    rightOscillator.frequency.setValueAtTime(rightFreq, audioContext.currentTime);
}

// Update Volume
function updateVolume() {
    if (!leftGain || !rightGain) return;

    const volume = volumeSlider.value / 100;
    leftGain.gain.setValueAtTime(volume, audioContext.currentTime);
    rightGain.gain.setValueAtTime(volume, audioContext.currentTime);
}

// Update Status
function updateStatus(type, text) {
    statusText.textContent = text;
    
    if (type === 'playing') {
        statusIcon.textContent = '🎵';
        statusText.style.color = '#00b894';
    } else if (type === 'stopped') {
        statusIcon.textContent = '⚫';
        statusText.style.color = '#a0aec0';
    } else if (type === 'exporting') {
        statusIcon.textContent = '💾';
        statusText.style.color = '#fdcb6e';
    } else if (type === 'success') {
        statusIcon.textContent = '✓';
        statusText.style.color = '#00b894';
    } else if (type === 'error') {
        statusIcon.textContent = '❌';
        statusText.style.color = '#d63031';
    }
}

// Generate Audio Buffer
function generateAudioBuffer(duration) {
    const sampleRate = 44100;
    const length = sampleRate * duration;
    const buffer = new AudioBuffer({
        length: length,
        numberOfChannels: 2,
        sampleRate: sampleRate
    });

    const leftChannel = buffer.getChannelData(0);
    const rightChannel = buffer.getChannelData(1);

    const leftFreq = parseFloat(leftFreqSlider.value);
    const rightFreq = parseFloat(rightFreqSlider.value);
    const volume = volumeSlider.value / 100;

    // Generate sine waves
    for (let i = 0; i < length; i++) {
        const t = i / sampleRate;
        leftChannel[i] = Math.sin(2 * Math.PI * leftFreq * t) * volume;
        rightChannel[i] = Math.sin(2 * Math.PI * rightFreq * t) * volume;
    }

    return buffer;
}

// Export WAV
function exportWAV() {
    updateStatus('exporting', '💾 Generating WAV file...');

    try {
        const duration = parseInt(durationInput.value) * 60; // Convert to seconds
        const buffer = generateAudioBuffer(duration);

        // Convert AudioBuffer to WAV
        const wav = audioBufferToWav(buffer);
        const blob = new Blob([wav], { type: 'audio/wav' });

        // Download
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `adhd_focus_${leftFreqSlider.value}hz.wav`;
        a.click();

        updateStatus('success', '✓ WAV export successful!');
        setTimeout(() => {
            updateStatus(isPlaying ? 'playing' : 'stopped', 
                        isPlaying ? '🎵 Playing - Focus Mode Active' : '⚫ Stopped');
        }, 3000);
    } catch (error) {
        console.error('Export error:', error);
        updateStatus('error', '❌ WAV export failed');
        setTimeout(() => {
            updateStatus(isPlaying ? 'playing' : 'stopped', 
                        isPlaying ? '🎵 Playing - Focus Mode Active' : '⚫ Stopped');
        }, 3000);
    }
}

// Export MP3 (Note: Browser-based MP3 encoding is complex, so we'll export as WAV with MP3 filename)
function exportMP3() {
    updateStatus('exporting', '🎵 Generating audio file...');

    try {
        const duration = parseInt(durationInput.value) * 60;
        const buffer = generateAudioBuffer(duration);

        // Convert to WAV (MP3 encoding requires external library)
        const wav = audioBufferToWav(buffer);
        const blob = new Blob([wav], { type: 'audio/wav' });

        // Download
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `adhd_focus_${leftFreqSlider.value}hz.wav`;
        a.click();

        updateStatus('success', '✓ Audio export successful!');
        alert('Note: Browser exports as WAV format. For MP3 conversion, use an online converter or the desktop app.');
        
        setTimeout(() => {
            updateStatus(isPlaying ? 'playing' : 'stopped', 
                        isPlaying ? '🎵 Playing - Focus Mode Active' : '⚫ Stopped');
        }, 3000);
    } catch (error) {
        console.error('Export error:', error);
        updateStatus('error', '❌ Export failed');
        setTimeout(() => {
            updateStatus(isPlaying ? 'playing' : 'stopped', 
                        isPlaying ? '🎵 Playing - Focus Mode Active' : '⚫ Stopped');
        }, 3000);
    }
}

// Convert AudioBuffer to WAV
function audioBufferToWav(buffer) {
    const length = buffer.length * buffer.numberOfChannels * 2 + 44;
    const arrayBuffer = new ArrayBuffer(length);
    const view = new DataView(arrayBuffer);
    const channels = [];
    let offset = 0;
    let pos = 0;

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

    setUint32(0x61746164); // "data" - chunk
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

    function setUint16(data) {
        view.setUint16(pos, data, true);
        pos += 2;
    }

    function setUint32(data) {
        view.setUint32(pos, data, true);
        pos += 4;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', init);

// Clean up on page unload
window.addEventListener('beforeunload', () => {
    if (isPlaying) {
        stopAudio();
    }
});

