import React, { useState } from "react";
import "./App.css";

function App() {
  const [started, setStarted] = useState(false);
  const [jobDescription, setJobDescription] = useState(null);
  const [resumes, setResumes] = useState([]);

  const handleStart = () => {
    setStarted(true);
  };

  const handleJobDescriptionChange = (event) => {
    setJobDescription(event.target.files[0]);
  };

  const handleResumesChange = (event) => {
    setResumes(Array.from(event.target.files));
  };

  const handleProcess = () => {
    if (!jobDescription) {
      alert("Please upload a Job Description (PDF) first.");
      return;
    }
    if (resumes.length === 0) {
      alert("Please upload at least one Resume (PDF).");
      return;
    }

    alert(`Processing ${resumes.length} resume(s) for the job: ${jobDescription.name}`);
  };

  return (
    <div className="App">
      {!started ? (
        <header className="App-header">
          <h1>Welcome to Resume Screening App</h1>
          <button className="App-button" onClick={handleStart}>
            Get Started
          </button>
        </header>
      ) : (
        <div className="upload-container">
          <h1>📄 Resume Screening App</h1>

          <div className="upload-section">
            <label>
              📄 Upload Job Description (PDF)
              <input type="file" accept=".pdf" onChange={handleJobDescriptionChange} />
            </label>
          </div>

          <div className="upload-section">
            <label>
              📂 Upload Resumes (PDF)
              <input type="file" accept=".pdf" multiple onChange={handleResumesChange} />
            </label>
          </div>

          <button className="App-button" onClick={handleProcess}>
            🚀 Process Resumes
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
