import { Table } from 'react-bootstrap';
import axios from 'axios';
import { useEffect, useState } from 'react';
import { parseToNewAPI, urlShortenerURL } from '../../../Global';
import UrlRow from './row';

const UrlsTable = () => {
    const [shortenedUrls, setShortenedUrls] = useState([]);
    const [selected, setSelected] = useState('');
    const [trigger, setTrigger] = useState(0);

    const triggerFetch = () => {
        setTrigger(prev => prev + 1);
    };

    useEffect(() => {
        axios(parseToNewAPI(urlShortenerURL), {
            headers: {
                'BEARER-TOKEN': localStorage.getItem('auth_token'),
            },
        }).then(res => {
            setShortenedUrls(res.data.urls);
        });
    }, [trigger]);

    return (
        <Table style={{ color: 'white' }}>
            <thead>
                <tr>
                    <th>entry</th>
                    <th>url</th>
                </tr>
            </thead>
            <tbody>
                {shortenedUrls.map(item => (
                    <UrlRow
                        endpoint={item.endpoint}
                        url={item.url}
                        key={item.endpoint}
                        selected={selected}
                        setSelected={setSelected}
                        triggerFetch={triggerFetch}
                    />
                ))}
            </tbody>
        </Table>
    );
};

export default UrlsTable;
