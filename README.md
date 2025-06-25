# Dementia Detection System - Frontend

A machine learning-powered clinical tool that predicts early signs of dementia based on patient data.

## Features

- **Patient Data Input**: Comprehensive form for entering demographic, clinical, and brain measurement data
- **Real-time Prediction**: Machine learning model integration for instant dementia risk assessment
- **Professional UI**: Medical-grade interface built with Material UI and Tailwind CSS
- **Responsive Design**: Works seamlessly across desktop, tablet, and mobile devices
- **Backend Integration**: RESTful API communication with Flask backend

## Tech Stack

- **Frontend**: React 18, TypeScript, Material UI, Tailwind CSS
- **Routing**: React Router DOM
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Build Tool**: Vite

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend Flask server running on `http://localhost:5000`

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd dementia-detection-system
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Update the `.env` file with your backend URL:
```env
REACT_APP_API_BASE_URL=http://localhost:5000
```

5. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Backend Integration

### API Endpoints Expected

Your Flask backend should provide these endpoints:

#### 1. Health Check
```
GET /health
Response: { "status": "healthy" }
```

#### 2. Prediction
```
POST /predict
Content-Type: application/json

Request Body:
{
  "age": 75,
  "gender": "M",
  "education": 16,
  "ses": 2,
  "mmse": 24,
  "cdr": 0.5,
  "etiv": 1678,
  "nwbv": 0.736,
  "asf": 1.046
}

Response:
{
  "prediction": "Mild Dementia",
  "confidence": 0.85,
  "probabilities": {
    "No Dementia": 0.15,
    "Mild Dementia": 0.65,
    "Moderate Dementia": 0.15,
    "Severe Dementia": 0.05
  }
}
```

### CORS Configuration

Make sure your Flask backend has CORS enabled:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])
```

### Sample Flask Backend Structure

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

# Load your trained model
model = joblib.load('your_model.pkl')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Extract features in the correct order
        features = np.array([[
            data['age'],
            1 if data['gender'] == 'M' else 0,  # Encode gender
            data['education'],
            data['ses'],
            data['mmse'],
            data['cdr'],
            data['etiv'],
            data['nwbv'],
            data['asf']
        ]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        
        # Map prediction to class names
        class_names = ['No Dementia', 'Mild Dementia', 'Moderate Dementia', 'Severe Dementia']
        
        return jsonify({
            "prediction": class_names[prediction],
            "confidence": float(max(probabilities)),
            "probabilities": {
                class_names[i]: float(prob) 
                for i, prob in enumerate(probabilities)
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Footer.tsx
│   ├── HelpButton.tsx
│   ├── Layout.tsx
│   └── Navbar.tsx
├── pages/              # Page components
│   ├── AboutPage.tsx
│   ├── FeaturesPage.tsx
│   ├── HomePage.tsx
│   ├── NotFoundPage.tsx
│   └── PredictPage.tsx
├── routes/             # Routing configuration
│   └── AppRoutes.tsx
├── services/           # API services
│   └── api.ts
├── App.tsx
├── main.tsx
├── theme.ts
└── index.css
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Features Used in Prediction

The model uses these patient features:

### Demographic Features
- **Age**: Patient age in years
- **Gender**: Male (M) or Female (F)
- **Education**: Years of formal education
- **SES**: Socioeconomic Status (1-5 scale)

### Clinical Assessments
- **MMSE**: Mini-Mental State Examination score (0-30)
- **CDR**: Clinical Dementia Rating (0, 0.5, 1, 2, 3)

### Brain Measurements
- **eTIV**: Estimated Total Intracranial Volume (mm³)
- **nWBV**: Normalized Whole Brain Volume (ratio)
- **ASF**: Atlas Scaling Factor (ratio)

## Deployment

### Frontend Deployment

1. Build the project:
```bash
npm run build
```

2. Deploy the `dist` folder to your hosting service (Netlify, Vercel, etc.)

3. Update the environment variable for production:
```env
REACT_APP_API_BASE_URL=https://your-production-backend.com
```

### Backend Requirements

Ensure your backend:
- Accepts the exact JSON format shown above
- Returns predictions in the expected format
- Has CORS configured for your frontend domain
- Handles errors gracefully

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.