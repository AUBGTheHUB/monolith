import { Button } from 'react-bootstrap';
import axios from 'axios';

export const ObjectCard = ({ url }) => {
    const filename = url.slice(url.lastIndexOf('/') + 1);

    const saveToClipboard = () => {
        navigator.clipboard.writeText(url);
    };

    const deleteImage = () => {
        axios({
            method: 'delete'
            // url: url + '/api/hackathon/teams/' + team_data['id'] + '/',
            // headers: { 'BEARER-TOKEN': localStorage.getItem('auth_token') }
        })
            // eslint-disable-next-line no-unused-vars
            .then((res) => {
                console.log('Image was deleted');
                history(-2);
            })
            .catch((err) => {
                console.log(err);
            });
    };

    return (
        <div className="s3-object-card">
            <h3>{filename}</h3>
            <img src={url} />
            <Button variant="primary" onClick={saveToClipboard}>
                {' '}
                Get image url
            </Button>
            <Button variant="primary" onClick={deleteImage}>
                Delete image
            </Button>
        </div>
    );
};
