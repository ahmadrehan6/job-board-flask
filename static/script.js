const API_URL = "http://localhost:5000/jobs";
const jobForm = document.getElementById("job-form");
const jobsContainer = document.getElementById("jobs");
const toggleLayoutBtn = document.getElementById("toggle-layout");
const themeToggle = document.getElementById("theme-toggle");

let editingJobId = null;

// Filters
const filterJobType = document.getElementById("filter_job_type");
const filterLocation = document.getElementById("filter_location");
const filterTag = document.getElementById("filter_tag");
const sortSelect = document.getElementById("sort_select");
const applyBtn = document.getElementById("apply-filters");
const clearBtn = document.getElementById("clear-filters");

function buildQueryParams() {
  const params = new URLSearchParams();
  if (filterJobType.value.trim()) params.append("job_type", filterJobType.value.trim());
  if (filterLocation.value.trim()) params.append("location", filterLocation.value.trim());
  if (filterTag.value.trim()) params.append("tag", filterTag.value.trim());
  if (sortSelect.value) params.append("sort", sortSelect.value);
  return params.toString();
}

async function fetchJobs() {
  try {
    const query = buildQueryParams();
    const response = await fetch(`${API_URL}?${query}`);
    const jobs = await response.json();
    jobsContainer.innerHTML = "";

    jobs.forEach(job => {
      let formattedDate = "N/A";
      if (job.posted_date) {
        const postedDate = new Date(job.posted_date);
        if (!isNaN(postedDate)) {
          formattedDate = postedDate.toLocaleDateString();
        }
      }

      const tagHTML = job.tags
        ? job.tags.split(",").map(tag => `<span class="tag-pill" onclick="filterByTag('${tag.trim()}')">${tag.trim()}</span>`).join("")
        : `<span style="color: gray">N/A</span>`;

      const div = document.createElement("div");
      div.className = "job-card";
      div.innerHTML = `
        <h3>${job.title} <br><small>@ ${job.company}</small></h3>
        <p><strong>📍 Location:</strong> ${job.location}</p>
        <p><strong>📅 Posted:</strong> ${formattedDate}</p>
        <p><span class="badge">${job.job_type}</span></p>
        <div><strong>🏷 Tags:</strong><br>${tagHTML}</div>
        <div class="btn-row" style="margin-top: 10px;">
          <button class="edit-btn" onclick="editJob(${job.id})">Edit</button>
          <button class="delete-btn" onclick="deleteJob(${job.id})">Delete</button>
        </div>
      `;
      jobsContainer.appendChild(div);
    });
  } catch (err) {
    console.error("Error loading jobs:", err);
  }
}

function filterByTag(tag) {
  filterTag.value = tag;
  fetchJobs();
}

async function deleteJob(id) {
  const confirmed = confirm("Are you sure you want to delete this job?");
  if (!confirmed) return;

  try {
    await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    fetchJobs();
  } catch (error) {
    console.error("Error deleting job:", error);
  }
}

async function editJob(id) {
  const response = await fetch(`${API_URL}/${id}`);
  const job = await response.json();
  document.getElementById("title").value = job.title;
  document.getElementById("company").value = job.company;
  document.getElementById("location").value = job.location;
  document.getElementById("job_type").value = job.job_type;
  document.getElementById("tags").value = job.tags;
  editingJobId = id;
  jobForm.querySelector("button[type='submit']").textContent = "Update Job";
}

jobForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const jobData = {
    title: document.getElementById("title").value,
    company: document.getElementById("company").value,
    location: document.getElementById("location").value,
    job_type: document.getElementById("job_type").value,
    tags: document.getElementById("tags").value,
  };

  const method = editingJobId ? "PUT" : "POST";
  const url = editingJobId ? `${API_URL}/${editingJobId}` : API_URL;

  await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(jobData),
  });

  editingJobId = null;
  jobForm.reset();
  jobForm.querySelector("button[type='submit']").textContent = "Add Job";
  fetchJobs();
});

applyBtn.addEventListener("click", fetchJobs);

clearBtn.addEventListener("click", () => {
  filterJobType.value = "";
  filterLocation.value = "";
  filterTag.value = "";
  sortSelect.value = "posting_date_desc";
  fetchJobs();
});

toggleLayoutBtn.addEventListener("click", () => {
  jobsContainer.classList.toggle("mobile-view");
  toggleLayoutBtn.textContent = jobsContainer.classList.contains("mobile-view")
    ? "🖥️ Toggle Desktop View"
    : "📱 Toggle Mobile View";
});

fetchJobs();
