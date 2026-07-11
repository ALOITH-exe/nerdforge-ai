import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Dashboard } from './pages/Dashboard';
import { GenerateAttack } from './pages/GenerateAttack';
import { AttacksList } from './pages/AttacksList';
import { AttackDetail } from './pages/AttackDetail';
import { AboutUs } from './pages/AboutUs';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/generate" element={<GenerateAttack />} />
        <Route path="/attacks" element={<AttacksList />} />
        <Route path="/attacks/:id" element={<AttackDetail />} />
        <Route path="/about" element={<AboutUs />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
