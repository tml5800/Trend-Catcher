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
