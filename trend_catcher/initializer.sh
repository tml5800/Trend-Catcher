#!/bin/bash

echo "=============================="
echo "   Trend Catchers Setup"
echo "=============================="

# Create folders
mkdir -p backend frontend

# -------------------
# Backend Setup
# -------------------
cd backend
python3 -m venv venv
source venv/bin/activate

# Install backend dependencies
pip install fastapi uvicorn pandas scikit-learn

# Create files
touch main.py trend_analyzer.py trend_predictor.py database.py requirements.txt

# Save requirements
pip freeze > requirements.txt
deactivate

# -------------------
# Frontend Setup
# -------------------
cd ../
npx create-react-app frontend

# Create components folder
mkdir -p frontend/src/components

# Create sample Dashboard component
cat <<EOL > frontend/src/components/Dashboard.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Dashboard = () => {
    const [trends, setTrends] = useState([]);

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/trends")
        .then(res => setTrends(res.data.trends))
        .catch(err => console.log(err));
    }, []);

    return (
        <div>
            <h1>Trend Catchers Dashboard</h1>
            <ul>
                {trends.map((t, i) => (
                    <li key={i}>{t.hashtag} - {t.views.toLocaleString()} views</li>
                ))}
            </ul>
        </div>
    );
}

export default Dashboard;
EOL

# -------------------
# Final Message
# -------------------
echo "✅ Trend Catchers Project initialized!"
echo "Backend: ./backend"
echo "Frontend: ./frontend"
