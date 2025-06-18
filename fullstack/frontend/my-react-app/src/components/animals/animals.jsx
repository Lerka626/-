import './animals.css';
import { useEffect, useState } from 'react';

const API_URL = import.meta.env.VITE_API_BASE_URL;

export default function Animals() {
    const [openAddModal, setOpenAddModal] = useState(false);
    const [passports, setPassports] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [file, setFile] = useState(null);

    // States for the info modal window
    const [showInfoModal, setShowInfoModal] = useState(false);
    const [currentPassportInfo, setCurrentPassportInfo] = useState(null);
    const [cordsHistory, setCordsHistory] = useState([]);
    const [isInfoLoading, setIsInfoLoading] = useState(false);

    // States for the photo gallery inside the modal
    const [galleryPhotos, setGalleryPhotos] = useState([]);
    const [currentPhotoIndex, setCurrentPhotoIndex] = useState(0);

    const [inputs, setInputs] = useState({
        age: '', gender: '', cords_sd: '00.00', cords_vd: '00.00', name: ''
    });

    const fetchPassports = async () => {
        setLoading(true);
        try {
            const response = await fetch(`${API_URL}/all_passports`);
            if (!response.ok) throw new Error('Сетевая ошибка при загрузке паспортов.');
            const data = await response.json();
            setPassports(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchPassports();
    }, []);

    const handleShowPassportModal = async (passportId) => {
        if (!passportId) return;

        // Reset states before opening
        setCurrentPassportInfo(null);
        setCordsHistory([]);
        setGalleryPhotos([]);
        setCurrentPhotoIndex(0);
        setIsInfoLoading(true);
        setShowInfoModal(true);

        try {
            // Fetch all data for the modal concurrently
            const [passportResponse, historyResponse, photosResponse] = await Promise.all([
                fetch(`${API_URL}/get_passport/${passportId}`),
                fetch(`${API_URL}/passport/${passportId}/history`),
                fetch(`${API_URL}/passport/${passportId}/photos`)
            ]);

            // Check passport data
            if (!passportResponse.ok) throw new Error('Паспорт не найден');
            const passportData = await passportResponse.json();
            setCurrentPassportInfo(passportData);

            // Check history data
            if (historyResponse.ok) {
                const historyData = await historyResponse.json();
                setCordsHistory(historyData);
            }

            // Check photos data - 'photosResponse' is correctly defined here
            if (photosResponse.ok) {
                const photoData = await photosResponse.json();
                // Create the gallery list: main photo first, then the rest
                const allPhotos = [
                    passportData.image_preview,
                    ...photoData.filter(p => p !== passportData.image_preview)
                ];
                setGalleryPhotos(allPhotos);
            }

        } catch (error) {
            console.error("Ошибка при получении данных паспорта:", error);
            alert(error.message);
            setShowInfoModal(false);
        } finally {
            setIsInfoLoading(false);
        }
    };

    const handleCloseInfoModal = () => {
        setShowInfoModal(false);
    };

    const handlePhotoChange = (direction) => {
        if (galleryPhotos.length <= 1) return;
        if (direction === 'next') {
            setCurrentPhotoIndex((prevIndex) => (prevIndex + 1) % galleryPhotos.length);
        } else if (direction === 'prev') {
            setCurrentPhotoIndex((prevIndex) => (prevIndex - 1 + galleryPhotos.length) % galleryPhotos.length);
        }
    };

    const handleInputChange = (e) => setInputs({ ...inputs, [e.target.name]: e.target.value });
    const handleFileChange = (e) => setFile(e.target.files[0]);

    const handleAddPassportSubmit = async (e) => {
        e.preventDefault();
        if (!file) {
            alert("Пожалуйста, выберите фото для паспорта.");
            return;
        }

        const formData = new FormData();
        Object.entries(inputs).forEach(([key, value]) => formData.append(key, value));
        formData.append('image_preview', file);

        try {
            const response = await fetch(`${API_URL}/upload_passport/`, {
                method: 'POST', body: formData,
            });
            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Не удалось создать паспорт.');
            }
            setOpenAddModal(false);
            fetchPassports();
            setFile(null);
        } catch (error) {
            console.error('Ошибка при создании паспорта:', error);
            alert(`Ошибка: ${error.message}`);
        }
    };

    if (loading) return <div className="loading-message">Загрузка...</div>;
    if (error) return <div className="error-message">Ошибка: {error}</div>;

    return (
        <>
            <div className="name-of-str">Паспорта редких животных</div>
            <div className="animals-container-wrapper">
                <div className="header-of-animals">
                    <div className="add-passport-btn" onClick={() => setOpenAddModal(true)}>
                        Добавить паспорт
                    </div>
                </div>
                <div className="passports">
                    {passports.map((passport) => (
                        <div className="passport" key={passport.id}>
                            <div className="animal-img">
                                {passport.image_preview ?
                                    <img src={`${API_URL}/image/passport/${passport.image_preview}`} alt={passport.name} />
                                    : <div>Нет фото</div>}
                            </div>
                            <div className="text-info-animal">
                                <div className="irb-name">{passport.name || 'Неизвестно'}</div>
                                <div className="sex"><label>Вид:</label> {passport.type}</div>
                                <div className="sex"><label>Пол:</label> {passport.gender || 'Неизвестен'}</div>
                                <div className="age">{passport.age ? `${passport.age} лет` : 'Возраст не указан'}</div>
                                <div className="more-info" onClick={() => handleShowPassportModal(passport.id)}>
                                    Больше информации
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            <div className={`modal-add-passport ${openAddModal ? 'visible' : 'hidden'}`}>
                 <div className="add-passport-container">
                    <div className="close" onClick={() => setOpenAddModal(false)}>&times;</div>
                    <h4 className="modal-title">Введите данные животного</h4>
                    <form className="inputs_passport" onSubmit={handleAddPassportSubmit}>
                        <div className="add_name"><label>Имя</label><input type="text" name="name" value={inputs.name} onChange={handleInputChange} required /></div>
                        <div className="add_name"><label>Возраст</label><input type="number" name="age" value={inputs.age} onChange={handleInputChange} required /></div>
                        <div className="add_name"><label>Пол</label><input type="text" name="gender" value={inputs.gender} onChange={handleInputChange} required /></div>
                        <div className="add_name"><label>Широта:</label><input type="text" name="cords_sd" value={inputs.cords_sd} onChange={handleInputChange} required /></div>
                        <div className="add_name"><label>Долгота:</label><input type="text" name="cords_vd" value={inputs.cords_vd} onChange={handleInputChange} required /></div>
                        <div className="add-photo">
                            <label className="input-file">
                                <input onChange={handleFileChange} type="file" name="file" accept="image/png, image/jpeg" required/>
                                <span>Выберите фото</span>
                            </label>
                            {file && <span>Выбран файл: {file.name}</span>}
                        </div>
                        <button type="submit">Создать паспорт</button>
                    </form>
                </div>
            </div>

            <div className={`show_animal_passport ${showInfoModal ? 'visible' : 'hidden'}`}>
                <div className="animal-passport-wrapper">
                    <div className="close" onClick={handleCloseInfoModal}>&times;</div>

                    {isInfoLoading ? (
                        <div className="loading-message">Загрузка данных...</div>
                    ) : currentPassportInfo ? (
                        <>
                            <div className="passport-modal-name">
                                {currentPassportInfo.name || 'Паспорт животного'}
                            </div>

                            <div className="photo-gallery">
                                <div className="gallery-image">
                                    {galleryPhotos.length > 0 && (
                                        <img
                                          src={`${API_URL}/image/passport/${galleryPhotos[currentPhotoIndex]}`}
                                          alt={`${currentPassportInfo.name} - фото ${currentPhotoIndex + 1}`}
                                        />
                                    )}
                                </div>
                                {galleryPhotos.length > 1 && (
                                    <div className="gallery-controls">
                                        <button onClick={() => handlePhotoChange('prev')} className="gallery-arrow">‹</button>
                                        <span className="gallery-counter">{currentPhotoIndex + 1} / {galleryPhotos.length}</span>
                                        <button onClick={() => handlePhotoChange('next')} className="gallery-arrow">›</button>
                                    </div>
                                )}
                            </div>

                            <div className="passport-modal-items">
                                <div className="passport-item"><label>Имя:</label> {currentPassportInfo.name}</div>
                                <div className="passport-item"><label>Вид:</label> {currentPassportInfo.type}</div>
                                <div className="passport-item"><label>ID:</label> {currentPassportInfo.id}</div>
                                <div className="passport-item"><label>Пол:</label> {currentPassportInfo.gender}</div>
                                <div className="passport-item"><label>Возраст:</label> {currentPassportInfo.age}</div>
                            </div>

                            <div className="passport-history">
                                <h4>История перемещений:</h4>
                                {cordsHistory.length > 0 ? (
                                    <ul>
                                        {cordsHistory.map((record, index) => (
                                            <li key={index}>
                                                {new Date(record.date).toLocaleDateString()}: {record.coordinates}
                                            </li>
                                        ))}
                                    </ul>
                                ) : (
                                    <p>История перемещений отсутствует.</p>
                                )}
                            </div>
                        </>
                    ) : (
                         <div className="error-message">Не удалось загрузить данные.</div>
                    )}
                </div>
            </div>
        </>
    );
}

