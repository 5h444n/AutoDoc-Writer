
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Converter from './pages/converter'; 

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/converter" element={<Converter />} />
      </Routes>
    </Router>
  );
}

export default App;