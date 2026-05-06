import React, { useState } from "react";
import "./App.css";

function App() {
  const API = "http://127.0.0.1:5000";

  const [page, setPage] = useState("login");
  const [user, setUser] = useState(null);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [jobs, setJobs] = useState([]);
  const [applications, setApplications] = useState([]);
  const [search, setSearch] = useState("");

  // LOGIN
  const login = async () => {
    const res = await fetch(`${API}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (data.user_id) {
      setUser(data);
      setPage("jobs");
      getJobs();
    } else {
      alert(data.message);
    }
  };

  // REGISTER
  const register = async () => {
    const res = await fetch(`${API}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name,
        email,
        password,
        role: "user",
      }),
    });

    const data = await res.json();
    alert(data.message);
    setPage("login");
  };

  // GET JOBS
  const getJobs = async () => {
    const res = await fetch(`${API}/jobs`);
    const data = await res.json();
    setJobs(data);
  };

  // APPLY JOB
  const applyJob = async (job_id) => {
    const res = await fetch(`${API}/apply`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: user.user_id,
        job_id,
      }),
    });

    const data = await res.json();
    alert(data.message);
  };

  // APPLICATIONS
  const getApplications = async () => {
    const res = await fetch(`${API}/applications/${user.user_id}`);
    const data = await res.json();
    setApplications(data);
    setPage("applications");
  };

  // FILTER
  const filteredJobs = jobs.filter(
    (job) =>
      job.title.toLowerCase().includes(search.toLowerCase()) ||
      job.company.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="app">

      <h1 className="title">Job Portal</h1>

      {/* LOGIN */}
      {page === "login" && (
        <div className="box">
          <h2>Login</h2>

          <input placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
          <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />

          <button onClick={login}>Login</button>

          <p onClick={() => setPage("register")}>Create account</p>
        </div>
      )}

      {/* REGISTER */}
      {page === "register" && (
        <div className="box">
          <h2>Register</h2>

          <input placeholder="Name" onChange={(e) => setName(e.target.value)} />
          <input placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
          <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />

          <button onClick={register}>Register</button>

          <p onClick={() => setPage("login")}>Already have account?</p>
        </div>
      )}

      {/* JOBS */}
      {page === "jobs" && (
        <div className="container">

          <div className="topbar">
            <h2>Available Jobs</h2>

            <div>
              <button onClick={getApplications}>Applied Jobs</button>
              <button onClick={() => setPage("login")}>Logout</button>
            </div>
          </div>

          <input
            className="search"
            placeholder="Search jobs..."
            onChange={(e) => setSearch(e.target.value)}
          />

          <div className="jobs-grid">
            {filteredJobs.map((job) => (
              <div className="card" key={job.id}>
                <h3>{job.title}</h3>
                <p>{job.company}</p>
                <p>{job.salary}</p>
                <p>{job.description}</p>

                <button onClick={() => applyJob(job.id)}>
                  Apply
                </button>
              </div>
            ))}
          </div>

        </div>
      )}

      {/* APPLICATIONS */}
      {page === "applications" && (
        <div className="container">

          <div className="topbar">
            <h2>My Applications</h2>
            <button onClick={() => setPage("jobs")}>Back</button>
          </div>

          <div className="jobs-grid">
            {applications.map((job, i) => (
              <div className="card small" key={i}>
                <h3>{job.title}</h3>
                <p>{job.company}</p>
              </div>
            ))}
          </div>

        </div>
      )}

    </div>
  );
}

export default App;