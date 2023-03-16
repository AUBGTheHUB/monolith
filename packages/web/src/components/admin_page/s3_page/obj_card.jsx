import { Button } from 'react-bootstrap';

export const ObjectCard = ({ url }) => {
    const filename = url.slice(url.lastIndexOf('/') + 1);

    const saveToClipboard = () => {
        navigator.clipboard.writeText(url);
    };

    return (
        <div className="s3-object-card">
            <h3>{filename}</h3>
            <img src={url} />
            <Button variant="primary" onClick={saveToClipboard}>
                {' '}
                Get image url
            </Button>
            <Button variant="primary">Delete image</Button>
        </div>
    );
};
