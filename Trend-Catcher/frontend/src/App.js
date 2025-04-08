import React, { useEffect, useState } from "react";

function Dashboard() {
  const [trends, setTrends] = useState([]);

  useEffect(() => {
    fetch(`${process.env.REACT_APP_API_URL}/api/trends`)
      .then((res) => res.json())
      .then((data) => setTrends(data.trends))
      .catch((err) => console.error("Failed to fetch trends:", err));
  }, []);

  return (
    <div>
      <h1>Trending Hashtags</h1>
      <ul>
        {trends.map((trend, index) => (
          <li key={index}>
            {trend.hashtag} – {trend.views.toLocaleString()} views
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;
