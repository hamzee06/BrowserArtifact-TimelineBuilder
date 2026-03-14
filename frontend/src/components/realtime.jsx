import React, { useState, useEffect, useRef } from 'react';
import { fetchRealTimeData } from '../services/api';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const tableStyle = {
  width: '100%',
  borderCollapse: 'collapse',
  marginTop: '20px',
  boxShadow: '0 2px 8px rgba(0,0,0,0.05)'
};

const thStyle = {
  background: '#f5f5f5',
  color: '#333',
  padding: '12px',
  borderBottom: '2px solid #ddd',
  textAlign: 'left'
};

const tdStyle = {
  padding: '10px',
  borderBottom: '1px solid #eee'
};

const zebraStyle = (index) => ({
  background: index % 2 === 0 ? '#fff' : '#f9f9f9'
});

const RealTimeLog = () => {
  const [log, setLog] = useState([]);
  const prevCount = useRef(0); // track previous length

  useEffect(() => {
    const fetchData = () => {
      fetchRealTimeData().then(data => {
        if (data.status === 'ok') {
          const newLog = data.data;

          // 🔔 detect new entries
          if (newLog.length > prevCount.current) {
            const newItems = newLog.slice(prevCount.current); // only new ones
            newItems.forEach(item => {
              toast.info(
                `🔔 ${item.title || 'New Activity'} \n${item.url || ''}`,
                { position: 'top-right', autoClose: 4000 }
              );
            });
          }

          prevCount.current = newLog.length;
          setLog(newLog);
        }
      });
    };

    fetchData();
    const intervalId = setInterval(fetchData, 2000); 

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div style={{ maxWidth: 800, margin: '40px auto', padding: 20, background: '#fafafa', borderRadius: 8 }}>
      <h2 style={{ textAlign: 'center', color: '#2c3e50', marginBottom: 24 }}>Real-Time Activity Log</h2>
      
      {/* 🔔 Toasts appear here */}
      <ToastContainer />

      <table style={tableStyle}>
        <thead>
          <tr>
            <th style={thStyle}>Timestamp</th>
            <th style={thStyle}>URL</th>
            <th style={thStyle}>Title</th>
          </tr>
        </thead>
        <tbody>
          {log.map((item, index) => (
            <tr key={index} style={zebraStyle(index)}>
              <td style={tdStyle}>{new Date(item.timestamp).toLocaleString()}</td>
              <td style={tdStyle}>
                <a
                  href={item.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    display: 'inline-block',
                    maxWidth: 180,
                    whiteSpace: 'nowrap',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    verticalAlign: 'bottom',
                    textDecoration: 'underline',
                    color: '#3498db'
                  }}
                  title={item.url}
                >
                  {item.url}
                </a>
              </td>
              <td style={tdStyle}>{item.title}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default RealTimeLog;
