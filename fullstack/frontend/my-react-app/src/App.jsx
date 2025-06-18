import Navigation from './components/navigation/Navigation'
import ProcessPhoto from './components/ProcessPhoto/ProcessPhoto';
// import Footer from './components/footer/Footer' // Убрали импорт футера
import Zips from './components/zips/Zips';
import Animals from './components/animals/animals';
import "./style.css";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

export default function App() {
  return (
    <>
      <Router>
          {/* Навигация теперь находится вне Routes и будет отображаться на всех страницах */}
          <Navigation/>

          {/* Основной контент страницы будет меняться внутри этого блока */}
          <main className="main-content-area">
            <Routes>
                <Route path="/" element={<ProcessPhoto />} />
                <Route path="/zips" element={<Zips />} />
                <Route path="/animals" element={<Animals />} />
            </Routes>
          </main>
      </Router>
    </>
  )
}