import axios from 'axios';
import { OverlayTrigger, Popover, Button } from 'react-bootstrap';
import { parseToNewAPI, urlShortenerURL } from '../../../Global';

const popover = onDelete => {
    return (
        <Popover id="popover-basic">
            <Popover.Header as="h3">Want to update or remove?</Popover.Header>
            <Popover.Body>
                <Button variant="danger" onClick={onDelete}>
                    Remove
                </Button>
            </Popover.Body>
        </Popover>
    );
};

const UrlRow = ({ endpoint, url, selected, setSelected, triggerFetch }) => {
    const isShown = endpoint === selected;

    const onDelete = () => {
        axios(parseToNewAPI(urlShortenerURL + `/${endpoint}`), {
            headers: {
                'BEARER-TOKEN': localStorage.getItem('auth_token'),
            },
            method: 'delete',
        }).then(() => {
            triggerFetch();
        });
    };

    return (
        <>
            <OverlayTrigger show={isShown} placement="bottom" overlay={popover(onDelete)}>
                <tr
                    onClick={() => {
                        if (selected === '' || endpoint !== selected) {
                            setSelected(endpoint);
                        } else {
                            setSelected('');
                        }
                    }}>
                    <td>https://thehub-aubg.com/s/{endpoint}</td>
                    <td>{url}</td>
                </tr>
            </OverlayTrigger>
        </>
    );
};

export default UrlRow;
