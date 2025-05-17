import './navigation.css'
import { useState } from 'react'
import { Link } from 'react-router-dom';

export default function Navigation() {
    const [showMenu, setShowMenu] = useState('none')

    return (
    <>
            <div className="navigation-container">
                <div className="brand-name">
                    IRIS
                </div>
                <div className="nav-items">
                    <Link to="/" className="nav-item">Главная</Link>
                    <a href="https://ups2025.tilda.ws/18_irbis" className="nav-item">Контакты</a>
                    <Link to="/zips" className="nav-item">Архив измерений</Link>
                    <Link to="/animals" className="nav-item">Животные</Link>
                    <div className="burger" onClick={() => setShowMenu('flex')}>
                        <div className="burger-item"></div>
                        <div className="burger-item"></div>
                        <div className="burger-item"></div>
                    </div>
                </div>
            </div>

            <div className={'mobile-nav-items' + ' ' + showMenu} onClick={() => setShowMenu('none')}>
                <Link to="/" className="mobile-nav-item">Главная</Link>
                <a href="https://ups2025.tilda.ws/18_irbis" className="mobile-nav-item">Контакты</a>
                <Link to="/zips" className="mobile-nav-item">Архив измерений</Link>
                <Link to="/animals" className="mobile-nav-item">Животные</Link>
            </div>
    </>
    )
}