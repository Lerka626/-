import Filters from './Filters/Filters'
import Result from './Result/Result'
import './ProcessPhoto.css'
import { useState } from 'react'

export default function ProcessPhoto() {
    const [params, setParams] = useState({"results": 0})
   
    if (params.results === 0) {
        return <Filters setParams={setParams} />
    } else if (params.results === 'load') {
        return <div className='loadText'>Подождите, идет загрузка и обработка...</div>
    } else {
        // Передаем setParams, чтобы из Result можно было вернуться назад
        return <Result params={params} setParams={setParams} />
    }
}
