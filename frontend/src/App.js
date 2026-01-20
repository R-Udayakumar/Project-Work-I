import React, { useState, useEffect } from 'react';
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

function App() {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({ name: '', target_role: '', skills: '' });
  const [dashboardData, setDashboardData] = useState(null);

  // --- AUTO-LOGIN ON REFRESH ---
  useEffect(() => {
    const savedId = localStorage.getItem("nexus_id");
    if (savedId) {
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
      
      localStorage.setItem("nexus_id", data.student_id); 
      fetchDashboard(data.student_id);

    } catch (error) {
      console.error("Error:", error);
      alert("Failed to connect to Backend.");
      setLoading(false);
    }
  };

  const handleReset = () => {
    localStorage.removeItem("nexus_id"); 
    setStep(1); 
    setDashboardData(null); 
    setFormData({ name: '', target_role: '', skills: '' }); 
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
            <p className="subtitle">The AI Mentor for your professional evolution.</p>
            
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

            {/* 5. Learning Path - FIX APPLIED HERE */}
            <motion.div className="card path-card" whileHover={{ scale: 1.01 }}>
              <div className="card-header">
                <BookOpen size={18} className="text-blue"/>
                <h3>Resource Sequence</h3>
              </div>
              <div className="resource-list">
                {dashboardData?.recommended_learning_path && dashboardData.recommended_learning_path.map((res, i) => (
                  <div 
                    key={i} 
                    className="resource-item" 
                    onClick={() => window.open(res.link, '_blank')}
                    style={{cursor: 'pointer'}}
                  >
                    <span className="step-num">0{i+1}</span>
                    {/* Access res.title instead of res object */}
                    <span style={{flex:1}}>{res.title}</span> 
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