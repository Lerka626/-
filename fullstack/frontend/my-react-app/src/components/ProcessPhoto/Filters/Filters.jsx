import { useState } from 'react'
import './filters.css'
import PropTypes from 'prop-types';

export default function Filters({ setParams }) {
    const [maxObjects, setMaxObjects] = useState(1);
    const [minSize, setMinSize] = useState(1);
    const [west, setWest] = useState(1)
    const [north, setNorth] = useState(1)
    const [openModal, setOpenModal] = useState(false)
    const [animals, setAnimals] = useState(
        {
            'sheep': false,
            'cattle': false,
            'seal': false,
            'camelus': false,
            'kiang': false,
            'zebra': false,
            'horse': false
        })
    
    const processCheckbox = (e) => {
        const animalId = e.target.id; 
    
        if (animalId in animals) {
            setAnimals((prevAnimals) => ({
                ...prevAnimals, 
                [animalId]: !prevAnimals[animalId] 
            }));
        }
    }

    const sendData = async (e) => {
        setParams({'results': 'load'})
        setOpenModal(false)

        const input = e.target
        const file = input.files[0]; 
        const formData = new FormData(); 
  
        formData.append('files', file, file.name);

        async function fetchData() {
            try {
                const response = await fetch(`http://92.255.107.199:8000/upload/?cords_sd=${west}&cords_vd=${north}`, {
                    method: 'POST',
                    body: formData,
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const res = await response.json();
                return res;
            } catch (error) {
                console.error('Fetching data failed:', error);
                return null;
            }
        }

        let res = null;
        let i = 0
        while (res === null && i < 10) {
            res = await fetchData();
            setParams({"results": 0})
            i ++
        }
        if (res !== null) {
            setParams({'results': 1, 'params': res})
        }
    }   

    return (
    <>
        <div className="filters-container">
            <div className="big_add_button" onClick={() => setOpenModal(true)}>
                ЗАГРУЗИТЬ ФАЙЛ
            </div>
        </div>

        <div className={`modal-upload ${openModal ? 'visible' : 'hidden'}`}>
            <div className="params-container">
                <div className="close" onClick={() => setOpenModal(false)}>
                    Закрыть
                </div>
                Выберите параметры для обработки
                <div className="params">
                    <div className="param">
                        <div className="input-for">Максимальное количество объектов</div>
                        <div className="input-data">
                            <input type="range" value={maxObjects} min="1" max="100" onInput={(e) => setMaxObjects(e.target.value)}/>
                            <output id="rangevalue">{maxObjects}</output>
                        </div>
                    </div>
                    <div className="param">
                        <div className="input-for">Минимальный размер объекта в пикселях</div>
                        <div className="input-data">
                            <input type="range" value={minSize} min="0" max="300" onInput={(e) => setMinSize(e.target.value)}/>
                            <output id="rangevalue">{minSize} px</output>
                        </div>
                    </div>

                    <div className="param scrollable">
                        <div className="input-for">Виды животных</div>
                        <div className="animals-select">
                            <div className="animal-select-item">
                                <label htmlFor="baran">Козёл</label>
                                <input onInput={(e) => (processCheckbox(e))} type="checkbox" name="sheep" id="sheep" />
                            </div>
                            <div className="animal-select-item">
                                <label htmlFor="horse">Медведь</label>
                                <input onInput={(e) => (processCheckbox(e))} type="checkbox" name="cattle" id="cattle"/>
                            </div>
                            <div className="animal-select-item">
                                <label htmlFor="baran">Волк</label>
                                <input onInput={(e) => (processCheckbox(e))} type="checkbox" name="seal" id="seal"/>
                            </div>
                            <div className="animal-select-item">
                                <label htmlFor="seacat">Заяц</label>
                                <input onInput={(e) => (processCheckbox(e))} type="checkbox" name="camelus" id="camelus"/>
                            </div>
                            <div className="animal-select-item">
                                <label htmlFor="cow">Ирбис </label>
                                <input onInput={(e) => (processCheckbox(e))} type="checkbox" name="kiang" id="kiang"/>
                            </div>
                            <div className="animal-select-item">
                                <label htmlFor="pig">Лиса</label>
                                <input onInput={(e) => (processCheckbox(e))} type="checkbox" name="zebra" id="zebra"/>
                            </div>
                            <div className="animal-select-item">
                                <label htmlFor="pig">Манул</label>
                                <input onInput={(e) => (processCheckbox(e))} type="checkbox" name="horse" id="horse"/>
                            </div>
                            <div className="animal-select-item">
                                <label htmlFor="pig">Олень</label>
                                <input onInput={(e) => (processCheckbox(e))} type="checkbox" name="horse" id="horse"/>
                            </div>
                            <div className="animal-select-item">
                                <label htmlFor="pig">Рысь</label>
                                <input onInput={(e) => (processCheckbox(e))} type="checkbox" name="horse" id="horse"/>
                            </div>
                            <div className="animal-select-item">
                                <label htmlFor="pig">Сурок</label>
                                <input onInput={(e) => (processCheckbox(e))} type="checkbox" name="horse" id="horse"/>
                            </div>
                            <div className="animal-select-item">
                                <label htmlFor="pig">Росомаха</label>
                                <input onInput={(e) => (processCheckbox(e))} type="checkbox" name="horse" id="horse"/>
                            </div>
                        </div>
                    </div>
                    <div className="param">
                        <div className="input-for">Широта и долгота измерений</div>
                        <div className="input-data">
                            <label>Широта</label>
                            <input type="text" value={west} onInput={(e) => setWest(e.target.value)}/>
                        </div>
                        <div className="input-data">
                            <label>Долгота</label>
                            <input type="text" value={north} onInput={(e) => setNorth(e.target.value)}/>
                        </div>
                    </div>
                </div>
                <div className="add-photo">
                    <label className="input-file">
                        <input onInput={(e) => sendData(e)} type="file" name="file" className="input_file"/>                        
                        <span>Выберите файл</span>
                    </label>                    
                    <div className="instructions">
                        <p>Загрузите снимок (.jpeg, .png, .jpg) или серию снимков в формате (.zip)</p>
                    </div>
                </div>
            </div>
        </div>

        <div className="animals-info-container">
            <div className="name-of-str">
                Сводка по заповеднику
            </div>
            <div className="animals-info">
                <div className="animals">
                    <div className="animal">
                        <div>Количество Ирбисов: 87</div>
                        <a href="">Больше информации</a>
                    </div>
                    <div className="animal">
                        <div>Количество Тигров: 150</div>
                        <a href="">Больше информации</a>
                    </div>
                    <div className="animal">
                        <div>Количество Леопардов: 128</div>
                        <a href="">Больше информации</a>
                    </div>
                    <div className="animal">
                        <div>Количество Афалинов: 91</div>
                        <a href="">Больше информации</a>
                    </div>
                </div>
                <div className="map">
                    <iframe className='animals-map' src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2260.8714869077967!2d39.71881357356276!3d43.58470006695607!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x40f5cbd3baafc893%3A0x378b92333ee70da2!2z0KHQmNCg0JjQo9Ch!5e0!3m2!1sru!2sru!4v1737203400150!5m2!1sru!2sru"></iframe>  
                </div>
            </div>
        </div>
    </>
    )
}

Filters.propTypes = {
    setParams: PropTypes.func.isRequired,
};