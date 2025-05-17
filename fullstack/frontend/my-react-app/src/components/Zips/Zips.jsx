import './zips.css';
import { useEffect, useState } from 'react';
import Result from '../ProcessPhoto/Result/Result';

export default function Zips() {
    const [data, setData] = useState([]);
    const [cIndex, setCIndex] = useState(null);
    const [params, setParams] = useState({"results": null}); 

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    };

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('http://92.255.107.199:8000/all_zips', {
                    method: 'GET',
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok: ' + response.statusText);
                }

                const jsonData = await response.json();
                setData(jsonData);
            } catch (error) {
                console.error('There was a problem with the fetch operation:', error);
            }
        };
        fetchData();
    }, []);

    useEffect(() => {
        const fetchParams = async () => {
            try {
                const response = await fetch(`http://92.255.107.199:8000/get_uploads/${cIndex}`, {
                    method: 'GET',
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok: ' + response.statusText);
                }

                const paramsData = await response.json();
                setParams({'results': 1, 'params': paramsData});
            } catch (error) {
                console.error('There was a problem with the fetch operation for uploads:', error);
            }
        };

        if (cIndex !== null) {
            fetchParams();
        }
    }, [cIndex]);

    if (params.results !== null) {
        return <Result params={params} setParams={setParams}/>;
    } else {
    return (
        <div className="zips-table">
            <div className="name-of-str">
                Архив измерений
            </div>
            <table className="results-table">
                <thead>
                    <tr>
                        <th>Дата обработки</th>
                        <th>Редкие животные</th>
                        <th>Широта, долгота</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((item, index) => (
                        <tr key={index} onClick={() => setCIndex(item.id)}> 
                            <th>{formatDate(item.upload_date)}</th>
                            <th>{item.rare_animals_count}</th>
                            <th>{item.coordinates}</th>
                        </tr>
                    ))}
                </tbody>
            </table>
            Нажмите на запись, чтоб увидеть полный отчет
        </div>
    )}
}


