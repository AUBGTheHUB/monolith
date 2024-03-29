import toast from 'react-hot-toast';

export const ObjectCard = ({ url }) => {
    const filename = url.slice(url.lastIndexOf('/') + 1);

    const saveToClipboard = () => {
        toast('Link is saved in clipboard');
        navigator.clipboard.writeText(url);
    };

    return (
        <div className="s3-object-card" onClick={saveToClipboard}>
            <h3>{filename}</h3>
            <img src={url} />
        </div>
    );
};
