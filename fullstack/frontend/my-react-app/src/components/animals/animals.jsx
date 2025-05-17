import './animals.css'
import { useEffect, useState } from 'react';

export default function Animals() {
    const [openModal, setOpenModal] = useState(false)
    const [passports, setPassports] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [file, setFile] = useState(null);
    const [showPassport, setShowPassport] = useState(false)
    const [passInfo, setPassInfo] = useState({})
    const [cordsInfo, setCordsInfo] = useState({})
    const [inputs, setInputs] = useState({
        'age': '',
        'gender': '',
        'cords_sd': '',
        'cords_vd': '',
        'name': ''
    });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setInputs({
            ...inputs,
            [name]: value,
        });
    };

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
        }
    };

    const handlePassprotModal = async (e) => {
        const selected_passport = e
        setShowPassport(true)
        console.log(selected_passport)
        const resp_pass = await fetch(`http://92.255.107.199:8000/get_passport/${selected_passport}`)
        const res_pass = await resp_pass.json()
        setPassInfo(res_pass[0])

        const resp = await fetch(`http://92.255.107.199:8000/get_coordinates/${res_pass[0].cords_id}`)
        const res = await resp.json()
        setCordsInfo(res[0])
    }

    const handleSubmit = async (e) => {
        e.preventDefault();

        setOpenModal(false)
        
        const formData = new FormData();

        if (file) {
            formData.append('image_preview', file);
        }

        try {
            await fetch(`http://92.255.107.199:8000/upload_passport/?age=${inputs['age']}&gender=${inputs['gender']}&cords_sd=${inputs['cords_sd']}&cords_vd=${inputs['cords_vd']}&name=${inputs['name']}`, {
                method: 'POST',
                body: formData
            });

        } catch (error) {
            console.error('Network error:', error);
        }
        const new_pass = {age: inputs['age'], gender: inputs['gender'], cords_sd: inputs['cords_sd'], cords_vd: inputs['cords_vd'], name: inputs['name']}
        setPassports([...passports, new_pass])
    };

    useEffect(() => {
        const fetchPassports = async () => {
            try {
                const response = await fetch('http://92.255.107.199:8000/all_passports'); // Замените на ваш реальный API
                if (!response.ok) {
                    throw new Error('Сетевая ошибка, не удалось получить данные о паспортах.');
                }
                const data = await response.json();
                setPassports(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchPassports();
    }, []);

    if (loading) {
        return <div>Загрузка...</div>;
    }

    if (error) {
        return <div>Ошибка: {error}</div>;
    } else {
        return (
    <>
        <div className="name-of-str">
            Паспорта животных
        </div>
        <div className="animals-container-wrapper">
            <div className="header-of-animals">
                <div className="add-passport-btn" onClick={() =>setOpenModal(true)}>
                    Добавить паспорт
                </div>
            </div>
            <div className="passports">
                {passports.map((passport, index) => (
                    <div className="passport" key={index}>
                        <div className="text-info-animal">
                            <div className="irb-name">{passport.name || 'Неизвестно'}</div>
                            <div className="sex"><label>Пол:</label> {passport.gender || 'Неизвестен'}</div>
                            <div className="age">{passport.age ? `${passport.age} лет` : 'Возраст неизвестен'}</div>
                            <div className="more-info" onClick={() => handlePassprotModal(passport.id)}>Больше информации</div>
                        </div>
                        <div className="animal-img">
                            {passport.image_preview ? <img src={'http://92.255.107.199:8000/pass_preview?image_name=' + passport.image_preview} alt={passport.name || 'Изображение'} /> : <div>Изображение не доступно</div>}
                        </div>
                    </div>
                ))}
            </div>
        </div>

        <div className={`modal-add-passport ${openModal ? 'visible' : 'hidden'}`}>
            <div className="add-passport-container">
                <div className="close" onClick={() => setOpenModal(false)}>
                    Закрыть
                </div>
                <form className="inputs_passport" onSubmit={handleSubmit}>
                    <div className="add_name">
                        <label>Имя</label>
                        <input type="text" name="name" value={inputs.name} onChange={handleInputChange} />
                    </div>
                    <div className="add_name">
                        <label>Возраст</label>
                        <input type="text" name="age" value={inputs.age} onChange={handleInputChange} />
                    </div>
                    <div className="add_name">
                        <label>Пол</label>
                        <input type="text" name="gender" value={inputs.gender} onChange={handleInputChange} />
                    </div>
                    <div className="add_name">
                        <label>Широта:</label>
                        <input type="text" name="cords_sd" value={inputs.cords_sd} onChange={handleInputChange} />
                    </div>
                    <div className="add_name">
                        <label>Долгота:</label>
                        <input type="text" name="cords_vd" value={inputs.cords_vd} onChange={handleInputChange} />
                    </div>
                    <div className="add-photo">
                        <label className="input-file">
                            <input onInput={handleFileChange} type="file" name="file" className="input_file"/>                        
                            <span>Выберите файл</span>
                        </label>                    
                        <div className="instructions">
                            <p>Загрузите снимок (.jpeg, .png, .jpg)</p>
                        </div>
                    </div>
                    <button type="submit">Отправить</button>
                </form>
            </div>
        </div>

        <div className={`show_animal_passport ${showPassport ? 'visible' : 'hidden'}`}>
            <div className="animal-passport-wrapper">
                <div className="close" onClick={() => setShowPassport(false)}>
                    Закрыть
                </div>
                <div className="passport-modal-name">
                    Паспорт животного
                </div>
                <div className="passport-modal-items">
                    <div className="passport-photo-modal">
                        <img src={'http://92.255.107.199:8000/pass_preview?image_name=' + passInfo.image_preview} alt=""/>
                    </div>
                    <div className="passport-item">
                        <label>Имя</label> {passInfo.name}
                    </div>
                    <div className="passport-item">
                        <label>Вид</label> {passInfo.type}
                    </div>
                    <div className="passport-item">
                        <label>ID</label> {passInfo.id}
                    </div>
                    <div className="passport-item">
                        <label>ПОЛ</label> {passInfo.gender}
                    </div>
                    <div className="passport-item">
                        <label>Возраст</label> {passInfo.age}
                    </div>
                    <div className="passport-item">
                        <label>Последние координаты</label> {cordsInfo.coordinates}
                    </div>
                    <div className="passport-item">
                        <label>Последняя дата обнаружения</label> {cordsInfo.date}
                    </div>
                    <div className="passport-item">
                        <label>Место обитания</label> Саяно-Шушенский заповедник
                    </div>
                </div>
            </div>
        </div>
    </>)}
}