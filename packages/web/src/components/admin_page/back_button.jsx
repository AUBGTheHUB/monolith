import { useNavigate } from 'react-router-dom';
import { Button } from 'react-bootstrap';
import './back_button.css';
const BackBtn = ({ style }) => {
    const history = useNavigate();
    return (
        <Button className={style} variant="primary" onClick={() => history(-1)}>
            &#8249;
        </Button>
    );
};
export default BackBtn;
