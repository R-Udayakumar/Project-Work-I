// import React, { useState } from 'react';
// import axios from 'axios';
// import './App.css';

// function App() {
//   const [step, setStep] = useState('create-profile');
//   const [studentId, setStudentId] = useState(null);
//   const [dashboardData, setDashboardData] = useState(null);
  
//   // Form State
//   const [name, setName] = useState('');
//   const [targetRole, setTargetRole] = useState('Software Engineer');
//   const [skillsInput, setSkillsInput] = useState('');

//   const handleCreateProfile = async (e) => {
//     e.preventDefault();
//     const skills = skillsInput.split(',').map(s => s.trim()).filter(s => s);
//     try {
//       const response = await axios.post('http://localhost:5000/api/profile', {
//         name,
//         target_role: targetRole,
//         skills
//       });
//       setStudentId(response.data.student_id);
//       // Automatically fetch dashboard after creating profile
//       fetchDashboard(response.data.student_id);
//     } catch (error) {
//       console.error("Error creating profile:", error);
//       alert("Failed to create profile. Is the backend running?");
//     }
//   };

//   const fetchDashboard = async (id) => {
//     try {
//       const response = await axios.get(`http://localhost:5000/api/dashboard/${id}`);
//       setDashboardData(response.data);
//       setStep('dashboard');
//     } catch (error) {
//       console.error("Error fetching dashboard:", error);
//     }
//   };

//   return (
//     <div className="App">
//       <header className="App-header">
//         <h1>Nexus AI Prototype</h1>
//       </header>
//       <main>
//         {step === 'create-profile' && (
//           <div className="card">
//             <h2>Create Your Student Profile</h2>
//             <form onSubmit={handleCreateProfile}>
//               <div className="form-group">
//                 <label>Full Name:</label>
//                 <input type="text" value={name} onChange={e => setName(e.target.value)} required />
//               </div>
//               <div className="form-group">
//                 <label>Target Role:</label>
//                 <select value={targetRole} onChange={e => setTargetRole(e.target.value)}>
//                   <option value="Software Engineer">Software Engineer</option>
//                   <option value="Data Scientist">Data Scientist</option>
//                 </select>
//               </div>
//               <div className="form-group">
//                 <label>Your Skills (comma-separated):</label>
//                 <input type="text" value={skillsInput} onChange={e => setSkillsInput(e.target.value)} placeholder="e.g., Python, Java, SQL" />
//               </div>
//               <button type="submit" className="btn">Initialize Digital Twin</button>
//             </form>
//           </div>
//         )}

//         {step === 'dashboard' && dashboardData && (
//           <div className="dashboard">
//             <h2>Welcome, {dashboardData.student_name}</h2>
//             <div className="dashboard-grid">
//               <div className="card">
//                 <h3>🎯 Your Focus: {dashboardData.target_role}</h3>
//                 <p><strong>Identified Skill Gaps:</strong></p>
//                 {dashboardData.skill_gaps.length > 0 ? (
//                   <ul>{dashboardData.skill_gaps.map(skill => <li key={skill}>{skill}</li>)}</ul>
//                 ) : (<p>No major gaps found! Keep it up.</p>)}
//               </div>
//               <div className="card highlight">
//                 <h3>💡 Daily Industry Insight</h3>
//                 <p>{dashboardData.daily_insight}</p>
//               </div>
//               <div className="card">
//                 <h3>⚡ Today's Micro-Challenge</h3>
//                 <p>{dashboardData.todays_challenge}</p>
//                 <button className="btn-small">Mark as Complete</button>
//               </div>
//               <div className="card">
//                 <h3>📚 Recommended Learning Path</h3>
//                 <ul>
//                   {dashboardData.recommended_learning_path.map((course, idx) => <li key={idx}>{course}</li>)}
//                 </ul>
//               </div>
//             </div>
//             <button className="btn btn-secondary" onClick={() => setStep('create-profile')}>Start Over</button>
//           </div>
//         )}
//       </main>
//     </div>
//   );
// }

// export default App;

import React, { useState , useEffect } from 'react';
import { motion } from 'framer-motion';
import './App.css';
import ChatBot from './ChatBot';
import { 
  BookOpen, 
  Code, 
  Cpu, 
  Target, 
  Zap, 
  ChevronRight, 
  Terminal 
} from 'lucide-react';

// function App() {
//   const [step, setStep] = useState(1);
//   const [loading, setLoading] = useState(false);
//   const [formData, setFormData] = useState({
//     name: '',
//     target_role: '',
//     skills: ''
//   });
//   const [dashboardData, setDashboardData] = useState(null);

//   const handleInputChange = (e) => {
//     setFormData({ ...formData, [e.target.name]: e.target.value });
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setLoading(true);

//     try {
//       // 1. Send data to the NEW Backend Endpoint
//       const res = await fetch('http://127.0.0.1:5000/api/init_twin', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({
//           name: formData.name,
//           target_role: formData.target_role,
//           skills: formData.skills.split(',').map(s => s.trim()) // Convert string to array
//         }),
//       });

//       if (!res.ok) throw new Error("Backend connection failed");

//       const data = await res.json();
      
//       // 2. If successful, fetch the Dashboard immediately using the new ID
//       fetchDashboard(data.student_id);

//     } catch (error) {
//       console.error("Error:", error);
//       alert("Failed to connect to Nexus AI Backend. Make sure 'python app.py' is running!");
//       setLoading(false);
//     }
//   };

//   const fetchDashboard = async (id) => {
//     try {
//       const res = await fetch(`http://127.0.0.1:5000/api/dashboard/${id}`);
//       const data = await res.json();
//       setDashboardData(data);
//       setStep(2); // Move to dashboard view
//     } catch (error) {
//       console.error("Dashboard Error:", error);
//     } finally {
//       setLoading(false);
//     }
//   };

function App() {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({ name: '', target_role: '', skills: '' });
  const [dashboardData, setDashboardData] = useState(null);

  // --- NEW: AUTO-LOGIN ON REFRESH ---
  useEffect(() => {
    // 1. Check if we have a saved ID in the browser
    const savedId = localStorage.getItem("nexus_id");
    
    if (savedId) {
      // 2. If yes, go straight to fetching data (Skip the form!)
      fetchDashboard(savedId);
    }
  }, []);

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await fetch('http://127.0.0.1:5000/api/init_twin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: formData.name,
          target_role: formData.target_role,
          skills: formData.skills.split(',').map(s => s.trim())
        }),
      });

      if (!res.ok) throw new Error("Backend connection failed");

      const data = await res.json();
      
      // --- NEW: SAVE ID TO BROWSER ---
      localStorage.setItem("nexus_id", data.student_id); 
      
      fetchDashboard(data.student_id);

    } catch (error) {
      console.error("Error:", error);
      alert("Failed to connect to Backend.");
      setLoading(false);
    }
  };

  // --- NEW: LOGOUT FUNCTION ---
  // You need this so you can actually create a NEW user if you want to!
  const handleReset = () => {
    localStorage.removeItem("nexus_id"); // Clear memory
    setStep(1); // Go back to form
    setDashboardData(null); // Clear data
    setFormData({ name: '', target_role: '', skills: '' }); // Clear inputs
  };

  const fetchDashboard = async (id) => {
    try {
      const res = await fetch(`http://127.0.0.1:5000/api/dashboard/${id}`);
      if (!res.ok) throw new Error("Failed to load dashboard");
      
      const data = await res.json();
      setDashboardData(data);
      setStep(2); 
    } catch (error) {
      console.error("Dashboard Error:", error);
      // If the ID is invalid (e.g. server restarted and DB is empty), reset
      handleReset(); 
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="logo">
          <Cpu className="icon-logo" /> NEXUS AI
        </div>
        {step === 2 && (
          <button onClick={handleReset} className="reset-btn">
            New Profile
          </button>
        )}
      </header>

      <main>
        {step === 1 ? (
          <motion.div 
            className="hero-section"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1>Build Your Digital Twin</h1>
            <p className="subtitle">The AI Architect for your professional evolution.</p>
            
            <form onSubmit={handleSubmit} className="glass-form">
              <div className="input-group">
                <label>Identity Name</label>
                <input 
                  type="text" 
                  name="name" 
                  placeholder="e.g. Alex Chen" 
                  value={formData.name} 
                  onChange={handleInputChange} 
                  required 
                />
              </div>

              <div className="input-group">
                <label>Target Protocol (Role)</label>
                <input 
                  type="text" 
                  name="target_role" 
                  placeholder="e.g. DevOps Engineer" 
                  value={formData.target_role} 
                  onChange={handleInputChange} 
                  required 
                />
              </div>

              <div className="input-group">
                <label>Current Modules (Skills)</label>
                <input 
                  type="text" 
                  name="skills" 
                  placeholder="e.g. Docker, Python, Linux" 
                  value={formData.skills} 
                  onChange={handleInputChange} 
                  required 
                />
              </div>

              <button type="submit" className="cta-button" disabled={loading}>
                {loading ? (
                  <span className="loading-text">Analyzing Neural Pathways...</span>
                ) : (
                  <>Initialize System <ChevronRight size={20}/></>
                )}
              </button>
            </form>
          </motion.div>
        ) : (
          <>
          <motion.div 
            className="dashboard-grid"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, staggerChildren: 0.1 }}
          >
            {/* 1. Profile Card */}
            <motion.div className="card profile-card" whileHover={{ scale: 1.02 }}>
              <div className="card-header">
                <Terminal size={18} className="text-accent"/>
                <h3>Identity Matrix</h3>
              </div>
              <div className="profile-info">
                <h2>{dashboardData?.student_name}</h2>
                <div className="badge">{dashboardData?.target_role}</div>
              </div>
            </motion.div>

            {/* 2. Insight Card */}
            <motion.div className="card insight-card" whileHover={{ scale: 1.02 }}>
              <div className="card-header">
                <Zap size={18} className="text-yellow"/>
                <h3>Market Pulse</h3>
              </div>
              <p className="insight-text">"{dashboardData?.daily_insight}"</p>
            </motion.div>

            {/* 3. Skill Gaps */}
            <motion.div className="card gaps-card" whileHover={{ scale: 1.01 }}>
              <div className="card-header">
                <Target size={18} className="text-red"/>
                <h3>Critical Missing Skills</h3>
              </div>
              <ul className="gap-list">
                {dashboardData?.skill_gaps.map((gap, i) => (
                  <li key={i} className="gap-item">
                     {gap}
                  </li>
                ))}
              </ul>
            </motion.div>

            {/* 4. Challenge Card */}
            <motion.div className="card challenge-card" whileHover={{ scale: 1.01 }}>
              <div className="card-header">
                <Code size={18} className="text-green"/>
                <h3>Active Protocol</h3>
              </div>
              <div className="code-block">
                {dashboardData?.todays_challenge}
              </div>
            </motion.div>

            {/* 5. Learning Path */}
            <motion.div className="card path-card" whileHover={{ scale: 1.01 }}>
              <div className="card-header">
                <BookOpen size={18} className="text-blue"/>
                <h3>Upload Sequence</h3>
              </div>
              <div className="resource-list">
                {dashboardData?.recommended_learning_path.map((res, i) => (
                  <div key={i} className="resource-item" onClick={() => window.open(res, '_blank')}>
                    <span className="step-num">0{i+1}</span>
                    <span style={{flex:1}}>{res}</span>
                    <ChevronRight size={16} color="#94a3b8"/>
                  </div>
                ))}
              </div>
            </motion.div>
          </motion.div>
          <ChatBot studentId={dashboardData?.student_id} studentName={dashboardData?.student_name} />
          </>
        )}
      </main>
    </div>
  );
}

export default App;