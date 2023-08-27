import { OverlayTrigger, Popover, Button } from 'react-bootstrap';

const popover = (
    <Popover id="popover-basic">
        <Popover.Header as="h3">Want to update or remove?</Popover.Header>
        <Popover.Body>
            <Button variant="danger">Remove</Button>
        </Popover.Body>
    </Popover>
);

const UrlRow = ({ endpoint, url, selected, setSelected }) => {
    const isShown = endpoint === selected;

    return (
        <>
            <OverlayTrigger show={isShown} placement="bottom" overlay={popover}>
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
