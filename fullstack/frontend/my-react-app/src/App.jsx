import Navigation from './components/navigation/Navigation'
import ProcessPhoto from './components/ProcessPhoto/ProcessPhoto';
import Footer from './components/footer/Footer'
import Zips from './components/zips/Zips';
import Animals from './components/animals/animals';
import "./style.css";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

export default function App() {
  return (
    <>
      <Router>
          <Routes>
              <Route path="/" element={
                <>
                  <Navigation/>
                  <ProcessPhoto/>
                  <Footer/>
                </>} />
              <Route path="/zips" element={
                <>
                  <Navigation/>
                  <Zips/>
                  <Footer/>
                </>
              } />
              <Route path="/animals" element={
                <>
                  <Navigation/>
                  <Animals/>
                  <Footer/>
                </>
              } />
          </Routes>
      </Router>
    </>
  )
}