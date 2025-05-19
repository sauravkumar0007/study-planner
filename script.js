document.getElementById("studyForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const subjects = document.getElementById("subjects").value.split(",").map(s => s.trim());
  const examDates = document.getElementById("examDates").value.split(",").map(d => d.trim());
  const dailyHours = parseInt(document.getElementById("dailyHours").value);

  if (subjects.length !== examDates.length) {
    alert("Subjects and Exam Dates count must match!");
    return;
  }

  fetch("http://localhost:5000/api/generate-timetable", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ subjects, examDates, dailyHours }),
  })
    .then(res => res.json())
    .then(timetable => {
      let html = "<h2>📅 Generated Timetable</h2>";
      html += "<table><tr><th>Day</th><th>Subject</th><th>Date</th></tr>";

      timetable.forEach(entry => {
        html += `<tr><td>${entry.day}</td><td>${entry.subject}</td><td>${entry.examDate}</td></tr>`;
      });

      html += "</table>";
      document.getElementById("timetable").innerHTML = html;
    })
    .catch(err => {
      console.error(err);
      alert("Failed to generate timetable.");
    });
});