import React, { useEffect, useState } from "react";

function Dashboard() {
  const [trends, setTrends] = useState([]);
  const [comparison, setComparison] = useState("");

  useEffect(() => {
    // Fetch trending hashtags
    fetch(`${process.env.REACT_APP_API_URL}/api/trends`)
      .then((res) => res.json())
      .then((data) => setTrends(data.trends))
      .catch((err) => console.error("Error fetching trends:", err));

    // Fetch trend comparison
    fetch(`${process.env.REACT_APP_API_URL}/api/compare`)
      .then((res) => res.json())
      .then((data) => setComparison(data.comparison))
      .catch((err) => console.error("Error fetching comparison:", err));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Trending Hashtags</h1>
      <ul>
        {trends.map((trend, index) => (
          <li key={index}>
            {trend.hashtag} – {trend.views.toLocaleString()} views
          </li>
        ))}
      </ul>

      <h2 style={{ marginTop: "40px" }}>Trend Comparison</h2>
      <p>{comparison}</p>
    </div>
  );
}

export default Dashboard;
