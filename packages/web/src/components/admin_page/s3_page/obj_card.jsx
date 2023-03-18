import { Button } from 'react-bootstrap';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Popover from 'react-bootstrap/Popover';
// import axios from 'axios';

export const ObjectCard = ({ url }) => {
    const filename = url.slice(url.lastIndexOf('/') + 1);

    const saveToClipboard = () => {
        navigator.clipboard.writeText(url);
    };

    /* const deleteImage = () => {
        axios({
            method: 'delete'
            url: url + '/api/hackathon/teams/' + team_data['id'] + '/',
            headers: { 'BEARER-TOKEN': localStorage.getItem('auth_token') }
        })
            // eslint-disable-next-line no-unused-vars
            .then((res) => {
                console.log('Image was deleted');
                history(-2);
            })
            .catch((err) => {
                console.log(err);
            });
    }; */

    const CopyUrlPopover = (
        <Popover id="popover-basic">
            <Popover.Header as="h2">Copied image url!</Popover.Header>
        </Popover>
    );

    const DeleteImagePopover = (
        <Popover id="popover-basic">
            <Popover.Header as="h2">Image deleted successfully!</Popover.Header>
        </Popover>
    );

    const CopyUrl = () => (
        <OverlayTrigger
            trigger="click"
            placement="right"
            overlay={CopyUrlPopover}
        >
            <Button variant="primary" onClick={saveToClipboard}>
                Get image url
            </Button>
        </OverlayTrigger>
    );

    const DeleteImage = () => (
        <OverlayTrigger
            trigger="click"
            placement="right"
            overlay={DeleteImagePopover}
        >
            <Button variant="primary" onClick={saveToClipboard}>
                Delete image
            </Button>
        </OverlayTrigger>
    );

    return (
        <div className="s3-object-card">
            <h3>{filename}</h3>
            <img src={url} />
            <CopyUrl />
            <DeleteImage />
            {/* <Button variant="primary" onClick={saveToClipboard}>
                Get image url
            </Button> */}
            {/* <Button variant="primary" onClick={deleteImage} >
                Delete image
            </Button> */}
        </div>
    );
};
