import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/home';
import RealTimeLog from './components/realtime';
import LoginData from './components/logindata';
import HistoryTable from './components/historytable';


function App() {
  return (
    <>
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/realtime" element={<RealTimeLog />} />
        <Route path="/logins" element={<LoginData />} />
        <Route path="/history" element={<HistoryTable />} />
       

      </Routes>
    </Router>
    </>
  );
  
}

export default App;

