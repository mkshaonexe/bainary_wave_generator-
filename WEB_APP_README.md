# 🧠 ADHD Focus Generator - Web App

A beautiful, modern web application for generating binaural beats to enhance focus and concentration. Perfect for ADHD, studying, meditation, and relaxation.

## ✨ Features

### 🎵 **Full Audio Control**
- **Independent Frequency Control**: Adjust left and right ear frequencies separately (100-1000 Hz)
- **Real-time Binaural Beat Display**: See the beat frequency as you adjust
- **Volume Control**: Smooth volume slider with percentage display
- **Instant Playback**: Play/Stop controls with visual feedback

### 🎨 **Modern UI/UX**
- **Dark Theme**: Beautiful dark mode with purple gradient accents
- **Animated Background**: Subtle wave animations for a calming effect
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Smooth Animations**: Card hover effects, button transitions, and pulsing elements
- **Glass Morphism**: Modern card-based layout with depth

### 🎯 **Quick Presets**
- **ADHD Focus** (850 Hz) - Specialized frequency for ADHD
- **Deep Focus** (6 Hz Beat) - Theta waves for deep concentration
- **Alpha Waves** (10 Hz Beat) - Relaxation and learning
- **Beta Waves** (15 Hz Beat) - Active focus and concentration

### 💾 **Export Functionality**
- **WAV Export**: High-quality uncompressed audio
- **Custom Duration**: Choose from 1-120 minutes
- **Instant Download**: One-click download with custom filename

## 🚀 How to Use

### **Option 1: Open Directly in Browser**
1. Simply open `index.html` in any modern web browser
2. No installation or server required!

### **Option 2: Run with Local Server (Recommended)**
```bash
# Using Python 3
python -m http.server 8000

# Using Node.js
npx serve

# Then open: http://localhost:8000
```

## 🎧 Using the App

### **Quick Start**
1. **Choose a Preset**: Click one of the preset buttons (ADHD Focus, Deep Focus, etc.)
2. **Click PLAY**: Start the binaural beat audio
3. **Put on Headphones**: Binaural beats only work with headphones!

### **Custom Frequencies**
1. **Adjust Left Ear**: Use the left slider to set left ear frequency
2. **Adjust Right Ear**: Use the right slider to set right ear frequency
3. **Watch the Beat**: The center circle shows the binaural beat frequency
4. **Fine-tune Volume**: Adjust volume to comfortable level (30% recommended)

### **Export Audio**
1. **Set Duration**: Enter desired length in minutes
2. **Click Export**: Choose WAV format
3. **Save File**: Audio downloads automatically

## 🧠 Understanding Binaural Beats

Binaural beats work by playing two slightly different frequencies in each ear:
- **Left Ear**: Base frequency (e.g., 200 Hz)
- **Right Ear**: Base + Beat frequency (e.g., 206 Hz)
- **Your Brain**: Perceives the difference (6 Hz) as a rhythmic beat

### **Frequency Ranges**
- **Delta (1-4 Hz)**: Deep sleep, healing
- **Theta (4-8 Hz)**: Meditation, creativity, deep relaxation
- **Alpha (8-14 Hz)**: Relaxed focus, learning, stress reduction
- **Beta (14-30 Hz)**: Active concentration, problem-solving
- **850 Hz**: ADHD-specific focus frequency

## 🎨 Features Breakdown

### **Visual Design**
- Animated gradient background with rotating waves
- Card-based layout with hover effects
- Pulsing brain icon and beat circle
- Color-coded status indicators
- Smooth transitions and animations

### **Audio Technology**
- Web Audio API for high-quality sound generation
- Stereo panning for true binaural effect
- Real-time frequency adjustment
- Smooth gain control for volume

### **User Experience**
- Intuitive controls with clear labels
- Visual feedback for all interactions
- Responsive design for all screen sizes
- Keyboard accessible
- No installation required

## ⚠️ Safety & Best Practices

1. **Always Use Headphones**: Binaural beats require stereo separation
2. **Start Low**: Begin with lower volumes (20-30%)
3. **Take Breaks**: Use for 20-30 minute sessions
4. **Not While Driving**: Never use while operating vehicles or machinery
5. **Medical Conditions**: Consult a doctor if you have epilepsy or neurological conditions

## 🛠️ Technical Details

### **Technologies Used**
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **JavaScript (ES6+)**: Web Audio API for sound generation
- **No Dependencies**: Pure vanilla JavaScript, no frameworks needed

### **Browser Compatibility**
- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 14+
- ✅ Edge 79+

### **Audio Specifications**
- **Sample Rate**: 44,100 Hz (CD quality)
- **Bit Depth**: 16-bit PCM (WAV export)
- **Channels**: Stereo (2 channels)
- **Waveform**: Pure sine waves

## 📱 Mobile Support

The web app is fully responsive and works on:
- 📱 Smartphones (iOS & Android)
- 📱 Tablets
- 💻 Laptops
- 🖥️ Desktop computers

## 🔧 Customization

### **Changing Colors**
Edit `style.css` and modify the CSS variables:
```css
:root {
    --primary: #6c5ce7;        /* Main purple color */
    --secondary: #00b894;      /* Green accent */
    --accent: #fd79a8;         /* Pink accent */
    --bg-dark: #0a0e27;        /* Background */
}
```

### **Adding Presets**
Edit `index.html` and add new preset buttons:
```html
<button class="preset-btn" data-left="200" data-right="220">
    <span class="preset-icon">🌟</span>
    <span class="preset-name">Custom Preset</span>
    <span class="preset-freq">20 Hz Beat</span>
</button>
```

## 📊 Performance

- **Lightweight**: < 50KB total (HTML + CSS + JS)
- **Fast Loading**: No external dependencies
- **Low CPU**: Efficient audio generation
- **Battery Friendly**: Optimized for mobile devices

## 🎯 Use Cases

- **ADHD Focus**: Use 850 Hz preset for enhanced concentration
- **Studying**: Alpha/Beta waves for learning and retention
- **Meditation**: Theta waves for deep relaxation
- **Sleep**: Delta waves for deep sleep
- **Creativity**: Theta waves for creative thinking
- **Stress Relief**: Alpha waves for relaxation

## 🆚 Web App vs Desktop App

### **Web App Advantages**
- ✅ No installation required
- ✅ Works on any device with a browser
- ✅ Always up-to-date
- ✅ Cross-platform (Windows, Mac, Linux, Mobile)
- ✅ Shareable via URL

### **Desktop App Advantages**
- ✅ MP3 export (requires ffmpeg)
- ✅ Offline usage
- ✅ System tray integration

## 🤝 Contributing

Feel free to customize and improve the web app!

## 📝 License

Open source - use freely for personal and commercial projects.

## 🔗 Resources

- [Web Audio API Documentation](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
- [Binaural Beats Research](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4428073/)
- [ADHD and Sound Therapy](https://www.additudemag.com/sound-therapy-adhd/)

---

**Made with ❤️ for better focus and concentration**

Enjoy your journey to enhanced focus! 🧘‍♂️✨

