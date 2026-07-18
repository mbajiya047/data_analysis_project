document.addEventListener('DOMContentLoaded', async () => {
    const loader = document.querySelector('.loader-container');
    const dashboardContent = document.getElementById('dashboard-content');
    const avgMathsEl = document.getElementById('avg-maths');
    const avgScienceEl = document.getElementById('avg-science');
    const avgEnglishEl = document.getElementById('avg-english');
    const plotImgEl = document.getElementById('analysis-plot');
    const tbody = document.querySelector('#student-table tbody');

    try {
        // Fetch data from Flask API
        const response = await fetch('/api/data');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();

        // Populate Metrics
        avgMathsEl.textContent = data.metrics.avg_maths.toFixed(1);
        avgScienceEl.textContent = data.metrics.avg_science.toFixed(1);
        avgEnglishEl.textContent = data.metrics.avg_english.toFixed(1);
        
        // Render Image
        plotImgEl.src = data.plot;

        // Populate Table
        tbody.innerHTML = '';
        if (data.raw_data && data.raw_data.length > 0) {
            data.raw_data.forEach(student => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${student.Student_ID}</td>
                    <td>${student.Name}</td>
                    <td>${student.Age}</td>
                    <td>${student.Gender}</td>
                    <td>${student.Maths}</td>
                    <td>${student.Science}</td>
                    <td>${student.English}</td>
                    <td>${student.Attendance_Percent}%</td>
                    <td>${student.Study_Hours_Per_Week}</td>
                    <td><span class="grade-badge">${student.Final_Grade}</span></td>
                `;
                tbody.appendChild(tr);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="10" style="text-align: center;">No student data available.</td></tr>';
        }

        // Hide loader and show dashboard with smooth transition
        loader.style.display = 'none';
        dashboardContent.classList.remove('hidden');

    } catch (error) {
        console.error("Failed to load dashboard data:", error);
        loader.innerHTML = `<p style="color: #ef4444;">Failed to load data. Ensure the backend server is running.</p>`;
    }
});
