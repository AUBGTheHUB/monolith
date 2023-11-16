import { useNavigate } from 'react-router-dom';
import { Button } from 'react-bootstrap';
import './back_button.css';

const BackBtn = ({ positionButtonOnTop = false }) => {
    const history = useNavigate();
    const className = positionButtonOnTop ? 'top' : 'middle';
    return (
        <Button className={className} variant="primary" onClick={() => history(-1)}>
            &#8249;
        </Button>
    );
};

export default BackBtn;
