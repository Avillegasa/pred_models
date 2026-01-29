# Cybersecurity Incident Prediction Dashboard

**Frontend web dashboard for real-time cybersecurity threat detection**

![Dashboard Status](https://img.shields.io/badge/status-ready-success)
![React](https://img.shields.io/badge/react-18.2.0-blue)
![Vite](https://img.shields.io/badge/vite-7.3.1-purple)
![Bootstrap](https://img.shields.io/badge/bootstrap-5.3.2-blueviolet)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Available Models](#available-models)
- [Usage Guide](#usage-guide)
- [API Integration](#api-integration)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

Professional dark-themed web dashboard for predicting cybersecurity incidents using machine learning models. The dashboard provides real-time threat detection for:

1. **Phishing Email Detection** (Real API - 99.09% F1-Score)
2. **Suspicious Network Attacks** (Mock - Ready for model integration)
3. **Brute Force Attacks** (Mock - Ready for model integration)

### Key Features

✅ **Real-time Predictions** - Instant threat analysis via REST API
✅ **Interactive UI** - Dynamic forms with validation
✅ **Professional Theme** - Cybersecurity-inspired dark design
✅ **Responsive Design** - Works on desktop, tablet, and mobile
✅ **Mock Services** - Test UI before models are trained
✅ **Extensible Architecture** - Easy to add new models

---

## 🚀 Features

### Prediction Models
- **Phishing Detection**: Analyzes emails using Gradient Boosting (99.09% F1-Score)
- **Network Intrusion**: Detects suspicious network traffic patterns
- **Brute Force Detection**: Identifies credential stuffing attacks

### User Interface
- Model selection with 3 interactive buttons
- Dynamic forms with field validation
- Real-time error handling
- Confidence metrics visualization
- Processing time and metadata display

### Technical Features
- Context API for global state management
- Custom hooks for predictions and validation
- Axios interceptors for API error handling
- Bootstrap 5 responsive grid system
- React Icons for visual elements

---

## 🛠️ Tech Stack

### Core
- **React 18.2.0** - UI library
- **Vite 7.3.1** - Build tool & dev server
- **JavaScript (ES6+)** - Programming language

### UI Framework
- **Bootstrap 5.3.2** - CSS framework
- **React-Bootstrap 2.10.0** - React components
- **Sass 1.70.0** - CSS preprocessor
- **React Icons 5.0.1** - Icon library

### HTTP & State
- **Axios 1.6.5** - HTTP client
- **React Context API** - Global state management

---

## 🏁 Getting Started

### Prerequisites

- **Node.js** >= 18.x (current: v18.19.1)
- **npm** >= 9.x
- **Phishing API** running on `http://localhost:8000` (optional for testing mocks)

### Installation

```bash
# Navigate to frontend directory
cd /home/megalodon/dev/cbproy/pred_model/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The dashboard will be available at **http://localhost:5173**

---

## 📦 Project Structure

```
frontend/
├── public/                       # Static assets
├── src/
│   ├── components/
│   │   ├── common/               # Shared components
│   │   ├── dashboard/            # Dashboard layout
│   │   ├── forms/                # Form components
│   │   └── results/              # Result display
│   ├── context/
│   │   └── DashboardContext.jsx  # Global state
│   ├── hooks/
│   │   ├── usePrediction.js
│   │   └── useFormValidation.js
│   ├── services/
│   │   ├── api.js                # Axios config
│   │   ├── phishingService.js    # Real API
│   │   ├── ataquesSospechososService.js  # Mock
│   │   ├── fuerzaBrutaService.js # Mock
│   │   └── modelService.js       # Factory
│   ├── styles/
│   │   ├── custom-bootstrap.scss
│   │   ├── theme.js
│   │   ├── dashboard.css
│   │   └── components.css
│   ├── utils/
│   │   ├── validators.js
│   │   ├── formatters.js
│   │   └── testData.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── .env.example
├── .env.development
├── package.json
└── README.md
```

---

## 🤖 Available Models

### 1. Phishing Detection (Real API)

**Status**: ✅ Active
**Endpoint**: `http://localhost:8000/predict`
**Model**: Gradient Boosting (99.09% F1-Score)

**Input Fields**:
- Sender Email (required)
- Receiver Email (optional)
- Subject (required)
- Body (required)
- Contains URLs (0 or 1)

---

### 2. Suspicious Network Attacks (Mock)

**Status**: 🟡 Mock (Ready for real API)
**Simulates**: Network intrusion detection

**Input Fields**:
- Source IP (required)
- Target Port (1-65535, required)
- Protocol (TCP/UDP/ICMP/HTTP/HTTPS, required)
- Packet Count (required)
- Timestamp (required)
- Payload (optional)

---

### 3. Brute Force Detection (Mock)

**Status**: 🟡 Mock (Ready for real API)
**Simulates**: Login attack detection

**Input Fields**:
- Username (required)
- Source IP (required)
- Failed Attempts (1-1000, required)
- Time Window in minutes (required)
- Login Method (SSH/FTP/HTTP/RDP/SMTP, required)
- Last Successful Login (optional)

---

## 📖 Usage Guide

### Starting the Application

1. **Start the Phishing API** (for real predictions):
   ```bash
   cd ../Phishing/modeling/api
   uvicorn app:app --reload
   ```

2. **Start the Frontend**:
   ```bash
   npm run dev
   ```

3. **Open in Browser**: http://localhost:5173

### Using the Dashboard

1. **Select a Model**: Click one of the 3 model buttons at the top
2. **Fill the Form**: Enter data in the form fields (required fields marked with *)
3. **Predict**: Click the "Predict" button
4. **View Results**: Results appear in the right panel

---

## 🔗 API Integration

### Phishing API (Real)

**Base URL**: `http://localhost:8000`

**Configuration** (`.env.development`):
```env
VITE_PHISHING_API_URL=http://localhost:8000
VITE_API_TIMEOUT=10000
VITE_DEBUG_MODE=true
```

### Adding Real APIs for Mock Models

When models are trained, replace mock services:

**Before** (`ataquesSospechososService.js`):
```javascript
export const ataquesSospechososService = {
  async predict(data) {
    await delay(800);
    return mockResponse;
  }
};
```

**After**:
```javascript
import { networkApi } from './api';

export const ataquesSospechososService = {
  async predict(data) {
    return await networkApi.post('/predict', data);
  }
};
```

**Zero changes needed** in UI components!

---

## 💻 Development

### Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Environment Variables

Create `.env.development`:
```env
VITE_PHISHING_API_URL=http://localhost:8000
VITE_API_TIMEOUT=10000
VITE_DEBUG_MODE=true
```

---

## 🧪 Testing

### Manual Testing

1. **Phishing Model**:
   - Test with obvious phishing email
   - Test with legitimate email
   - Test API offline scenario

2. **Mock Models**:
   - Verify delay (600-900ms)
   - Test high-risk inputs (should predict attack)
   - Test low-risk inputs (should predict normal)

3. **UI/UX**:
   - Test form validation
   - Test loading states
   - Test error handling
   - Test responsive design

---

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

Output: `dist/` folder

### Deploy Options

1. **Vercel** (Recommended):
   ```bash
   npm install -g vercel
   vercel
   ```

2. **Netlify**:
   - Drag `dist/` folder to Netlify Drop

3. **Static Hosting**:
   - Serve `dist/` folder with any web server

---

## 🐛 Troubleshooting

### API Connection Errors

**Problem**: "Cannot connect to API"

**Solution**:
1. Verify API is running: `curl http://localhost:8000`
2. Check `.env.development` has correct URL
3. Check CORS settings in API

### Build Errors

**Problem**: Vite build fails

**Solution**:
```bash
rm -rf node_modules dist
npm install
npm run build
```

---

## 📚 Additional Resources

- **API Documentation**: `../Phishing/modeling/api/README.md`
- **Progress Tracking**: `PROGRESS.md`
- **Project Documentation**: `../CLAUDE.md`

---

## 👥 Authors

- **Machine Learning Model**: Gradient Boosting (99.09% F1-Score)
- **API Backend**: FastAPI + Uvicorn
- **Frontend Dashboard**: React + Vite + Bootstrap

---

**Last Updated**: 2026-01-12
**Version**: 1.0.0
**Status**: ✅ Ready for Production
