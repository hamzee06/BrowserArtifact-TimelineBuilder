import React, { useState } from 'react';
import { fetchCookies } from '../services/api';

const Cookies = () => {
  const [cookies, setCookies] = useState([]);
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleFileUpload = () => {
    if (file) {
      fetchCookies(file).then(data => setCookies(data));
    }
  };

  // ---------- STYLES ----------
  const containerStyle = {
    maxWidth: '900px',
    margin: '40px auto',
    padding: '20px',
    backgroundColor: '#ffffff',
    borderRadius: '12px',
    boxShadow: '0px 4px 10px rgba(0,0,0,0.08)',
  };

  const headingStyle = {
    textAlign: 'center',
    fontSize: '22px',
    fontWeight: '700',
    color: '#2c3e50',
    marginBottom: '20px',
  };

  const controlRowStyle = {
    display: 'flex',
    gap: '10px',
    marginBottom: '20px',
    alignItems: 'center',
  };

  const inputStyle = {
    flex: 1,
    padding: '10px 14px',
    borderRadius: '8px',
    border: '1px solid #dcdcdc',
    fontSize: '14px',
  };

  const buttonStyle = {
    padding: '10px 18px',
    borderRadius: '8px',
    border: 'none',
    backgroundColor: '#3498db',
    color: '#fff',
    fontWeight: '600',
    fontSize: '14px',
    cursor: 'pointer',
    transition: 'background 0.2s ease',
  };

  const tableWrapperStyle = {
    overflowX: 'auto',
    marginTop: '20px',
  };

  const tableStyle = {
    width: '100%',
    borderCollapse: 'collapse',
    border: '1px solid #e0e0e0',
    borderRadius: '8px',
    overflow: 'hidden',
  };

  const thStyle = {
    backgroundColor: '#f7f9fc',
    color: '#34495e',
    padding: '12px',
    fontWeight: '600',
    borderBottom: '2px solid #e0e0e0',
    textAlign: 'left',
    maxWidth: '250px',
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  };

  const tdStyle = {
    padding: '12px',
    borderBottom: '1px solid #f0f0f0',
    fontSize: '14px',
    color: '#333',
    maxWidth: '250px',
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  };

  const zebraStyle = (index) => ({
    backgroundColor: index % 2 === 0 ? '#ffffff' : '#f9fbfd',
  });

  // Shorten text helper
  const shortenText = (text, maxLength = 50) => {
    if (!text) return '';
    return text.length > maxLength
      ? text.slice(0, 30) + '...' + text.slice(-15)
      : text;
  };

  // ---------- COMPONENT ----------
  return (
    <div style={containerStyle}>
      <h2 style={headingStyle}>Browser Cookies</h2>

      <div style={controlRowStyle}>
        <input type="file" onChange={handleFileChange} style={inputStyle} />
        <button
          onClick={handleFileUpload}
          style={buttonStyle}
          onMouseOver={(e) => (e.target.style.backgroundColor = '#2980b9')}
          onMouseOut={(e) => (e.target.style.backgroundColor = '#3498db')}
        >
          Upload
        </button>
      </div>

      <div style={tableWrapperStyle}>
        <table style={tableStyle}>
          <thead>
            <tr>
              <th style={thStyle}>Host</th>
              <th style={thStyle}>Name</th>
              <th style={thStyle}>Value</th>
              <th style={thStyle}>Path</th>
              <th style={thStyle}>Expiry</th>
            </tr>
          </thead>
          <tbody>
            {cookies.map((cookie, index) => (
              <tr key={index} style={zebraStyle(index)}>
                <td style={tdStyle} title={cookie.host}>{shortenText(cookie.host)}</td>
                <td style={tdStyle} title={cookie.name}>{shortenText(cookie.name, 40)}</td>
                <td style={tdStyle} title={cookie.value}>{shortenText(cookie.value, 40)}</td>
                <td style={tdStyle} title={cookie.path}>{shortenText(cookie.path, 30)}</td>
                <td style={tdStyle}>{cookie.expiry}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Cookies;
