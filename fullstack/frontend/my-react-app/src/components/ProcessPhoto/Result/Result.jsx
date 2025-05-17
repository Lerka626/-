import { useState } from 'react'
import { PieChart, Pie, Cell, Tooltip } from 'recharts';
import './result.css'

export default function Result(params) {
    const [showResult, setShowResult] = useState('none')
    const [photoInformation, setPhotoInformation] = useState('')
    const [showPassport, setShowPassport] = useState(false)
    const [passInfo, setPassInfo] = useState({})
    const [cordsInfo, setCordsInfo] = useState({})
    const class_list = {
        'Irbis': 'Ирбис',
        'Bear': 'Медведь', 
        'Fox': 'Лиса',
        'Goat': 'Коза',
        'Lynx': 'Рысь',
        'Marmot': 'Сурок',
        'Wapiti': 'Вапити',
        'Wolf': 'Волк',
        'Wolverine': 'Россомаха',
        'Hare': 'Заяц',
    }
    
    const COLORS_pie = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

    const showModal = (item) => {
        setShowResult('show')
        setPhotoInformation(item.IMG)
    }

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

    if (params.params === undefined) {
        return null
    } else {
        const data_pie = Object.entries(params.params.params.diagram).map(([key, value]) => {
            return {
                name: class_list[key],
                value: value
            };
        }
    );
    return(
    <>
        <div className="name_of_block">
            Результат обработки данных
        </div>
        <div className="work_answer">
            <div className="diagram">
                <div className="pie-chart-name">
                    Соотношение видов животных
                </div>
                <PieChart width={350} height={350}>
                    <Pie
                        data={data_pie}
                        cx={175}
                        cy={205}
                        labelLine={false}
                        label={entry => entry.name}
                        outerRadius={60}
                        fill="#8884d8"
                        dataKey="value"
                    >
                        {data_pie.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS_pie[index % COLORS_pie.length]} />
                        ))}
                    </Pie>
                    <Tooltip />
                </PieChart>
            </div>
            <div className="table">
                <div className='pie-chart-name'>
                    Отчет о всех найденных животных
                </div>
                <table className="results-table">
                    <thead>
                        <tr>
                            <th>Дата обработки</th>
                            <th>Животные на снимке</th>
                            <th>Уверенность</th>
                            <th>Размер животных</th>
                            <th>Пасспорт</th>
                            <th>Фото</th>
                        </tr>
                    </thead>
                    <tbody>
                        {params.params.params.pred.map((item, index) => {
                            if (item == null) {
                                return null
                            }

                            return (
                            <tr key={index}>
                                <th>{item.date}</th>
                                <th>{class_list[item.type]}</th>
                                <th>{parseFloat(item.confidence).toFixed(2)}</th>
                                <th>{item.size}px</th>
                                <th className='underline' onClick={item.passport ? () => handlePassprotModal(item.passport) : () => ''}>{item.passport ? 'Открыть' : 'Отсутствует'}</th>
                                <th className='underline' onClick={() => showModal(item)}>Открыть  </th>
                            </tr>)
                        })}
                    </tbody>
                </table>
                <div className="go_away" onClick={() => window.location.reload()}>
                    Назад
                </div>
            </div>
        </div>
      

        <div onClick={() => setShowResult('none')} className={"result-container" + " " + showResult}>
            <div className="results">
                <div className="close" onClick={() => setShowResult('none')}>
                    Закрыть
                </div>
                <div className="photo-result-container">
                    <img src={'http://92.255.107.199:8000/image/' + photoInformation} alt=""/>
                </div>
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
    </>
    )}
}

