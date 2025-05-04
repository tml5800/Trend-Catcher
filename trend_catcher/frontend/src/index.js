const BASE_URL = "https://verbose-waffle-v6q6wjpxg5x4fxwgw-8000.app.github.dev";

async function searchTrends() {
  const topic = document.getElementById("topicInput").value.toLowerCase().trim();
  const resultBox = document.getElementById("result");

  if (!topic) {
    resultBox.textContent = "⚠️ Please enter a topic to search.";
    return;
  }

  try {
    const res = await fetch(`${BASE_URL}/search?topic=${encodeURIComponent(topic)}`);
    if (!res.ok) throw new Error("Failed to fetch search results");

    const data = await res.json();
    const matches = data.results;

    if (matches.length === 0) {
      resultBox.textContent = `⚠️ No trends found matching "${topic}".`;
    } else {
      displayTrends(matches);
    }
  } catch (error) {
    console.error("Search error:", error);
    resultBox.textContent = "⚠️ Failed to search trends. Make sure the backend is running.";
  }
}

function displayTrends(trends) {
  const resultBox = document.getElementById("result");

  let html = `
    <table>
      <thead>
        <tr>
          <th>Rank</th>
          <th>Hashtag</th>
          <th>Views</th>
        </tr>
      </thead>
      <tbody>
  `;

  trends.forEach((trend, index) => {
    html += `
      <tr${index === 0 ? ' class="gold"' : ''}>
        <td>#${index + 1}</td>
        <td>${trend.hashtag}</td>
        <td>${trend.views.toLocaleString()}</td>
      </tr>
    `;
  });

  html += `
      </tbody>
    </table>
  `;

  resultBox.innerHTML = html;
}

// Hook up the search button if it exists
document.addEventListener("DOMContentLoaded", () => {
  const searchBtn = document.querySelector("button[onclick='searchTrends()']");
  if (searchBtn) {
    searchBtn.addEventListener("click", searchTrends);
  }
});
