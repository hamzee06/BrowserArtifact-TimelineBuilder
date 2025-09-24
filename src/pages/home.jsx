import React, { useState } from 'react';
import HistoryTable from '../components/historytable';
import CookieList from '../components/cookielist';
import LoginData from '../components/logindata';
import About from '../pages/about';
import  RealtimeData  from '../components/realtime'; // Ensure this matches your file structure

// Responsive styles using CSS-in-JS
const sectionStyle = {
  background: '#fff',
  borderRadius: 16,
  boxShadow: '0 4px 24px rgba(44,62,80,0.08)',
  margin: '32px auto',
  padding: '32px 5vw',
  maxWidth: 900,
  width: '98vw',
  boxSizing: 'border-box',
  transition: 'box-shadow 0.2s',
};

const buttonGroupStyle = {
  display: 'flex',
  justifyContent: 'center',
  gap: '24px',
  margin: '32px 0 0 0',
  flexWrap: 'wrap'
};

const buttonStyle = (active) => ({
  padding: '12px 32px',
  fontSize: '1.1em',
  borderRadius: 8,
  border: 'none',
  background: active ? '#1976d2' : '#e3f2fd',
  color: active ? '#fff' : '#1976d2',
  fontWeight: 600,
  boxShadow: active ? '0 2px 8px rgba(25,118,210,0.12)' : 'none',
  cursor: 'pointer',
  transition: 'all 0.2s',
  marginBottom: '12px',
  minWidth: 120
});

const fileSectionStyle = {
  marginTop: 24,
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  width: '100%'
};

const textareaStyle = {
  width: '100%',
  minHeight: 80,
  marginBottom: 16,
  padding: 10,
  borderRadius: 6,
  border: '1px solid #cfd8dc',
  fontSize: '1em',
  resize: 'vertical',
  boxSizing: 'border-box'
};

const responsiveContainer = {
  background: 'linear-gradient(135deg, #e3f2fd 0%, #f8fafc 100%)',
  minHeight: '100vh',
  paddingBottom: 40,
  width: '100vw',
  boxSizing: 'border-box'
};

const headerStyle = {
  padding: '48px 0 20px 0',
  textAlign: 'center',
  background: 'rgba(255,255,255,0.7)',
  boxShadow: '0 2px 12px rgba(44,62,80,0.04)',
  marginBottom: 10,
  width: '100vw',
  boxSizing: 'border-box'
};

const h1Style = {
  color: '#1976d2',
  fontSize: '2.2em',
  marginBottom: 12,
  letterSpacing: 2,
  fontWeight: 700,
  fontFamily: 'Segoe UI, Arial, sans-serif'
};

const pStyle = {
  color: '#444',
  fontSize: '1.05em',
  marginBottom: 0,
  fontWeight: 500,
  letterSpacing: 0.5
};

const footerStyle = {
  textAlign: 'center',
  padding: '18px 0 8px 0',
  color: '#888',
  fontSize: '1em',
  letterSpacing: 0.5,
  width: '100vw',
  boxSizing: 'border-box'
};

const Home = () => {
  const [activeTab, setActiveTab] = useState('');
  const [fileContent, setFileContent] = useState('');
  const [fileName, setFileName] = useState('');

  // Handle file input and read content
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setFileName(file ? file.name : '');
    if (file) {
      const reader = new FileReader();
      reader.onload = (evt) => {
        setFileContent(evt.target.result);
      };
      reader.readAsText(file);
    } else {
      setFileContent('');
    }
  };

  // Render selected data component
  const renderDataSection = () => {
    switch (activeTab) {
      case 'history':
        return <HistoryTable />;
      case 'cookies':
        return <CookieList />;
      case 'logindata':
        return <LoginData />;
        case 'realtime':
        return <RealtimeData />;
      default:
        return null;
    }
  };

  return (
    <div style={responsiveContainer}>
      <header style={headerStyle}>
        <h1 style={h1Style}>
          Browser Data Viewer
        </h1>
        <p style={pStyle}>
          View your browser history, cookies, and login info in one place.
        </p>
      </header>

      <div style={buttonGroupStyle}>
        <button
          style={buttonStyle(activeTab === 'history')}
          onClick={() => setActiveTab('history')}
        >
          History
        </button>
        <button
          style={buttonStyle(activeTab === 'cookies')}
          onClick={() => setActiveTab('cookies')}
        >
          Cookies
        </button>
        <button
          style={buttonStyle(activeTab === 'logindata')}
          onClick={() => setActiveTab('logindata')}
        >
          Login Data
        </button>

        <button
          style={buttonStyle(activeTab === 'realtime')}
          onClick={() => setActiveTab('realtime')}  > Real Time</button> 
      </div>

      <main>
        <section style={sectionStyle}>
          {renderDataSection()}
          <div style={fileSectionStyle}>
          </div>
        </section>
        <section style={sectionStyle}>
          <About />
        </section>
      </main>
      <footer style={footerStyle}>
        &copy; {new Date().getFullYear()} Browser Data Viewer. All rights reserved.
      </footer>
    </div>
  );  
};

export default Home;