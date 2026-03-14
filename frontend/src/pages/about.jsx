  const About = () => {
    return (
      <div style={{ maxWidth: 700, margin: '40px auto', padding: 30, background: '#f8f9fa', borderRadius: 10, boxShadow: '0 2px 8px rgba(0,0,0,0.07)' }}>
        <h1 style={{ color: '#2c3e50', textAlign: 'center', marginBottom: 20 }}>About This App</h1>
        <p style={{ fontSize: '1.1em', color: '#444', marginBottom: 16 }}>
          This project is designed to show browser data like history, cookies, and login info using a React frontend and FastAPI backend.
        </p>
        <p style={{ fontWeight: 'bold', color: '#555', textAlign: 'center' }}>
          Created by: [Hamza Rafi]
        </p>
      </div>
    );
  };
  export default About;