import { useNavigate } from 'react-router-dom';
import { Button } from 'react-bootstrap';
const BackBtn = () => {
    const history = useNavigate();
    const btnStyle = {
        variant: 'primary',
        width: '3em',
        height: '3em',
        fontSize: '2vh',
        borderRadius: '50%',
        position: 'absolute',
        top: '3vw',
        left: '1vw',
        backcolor: 'red',
        zIndex: '1',
    };
    return (
        <Button style={btnStyle} variant="primary" onClick={() => history(-1)}>
            &#8249;
        </Button>
    );
};
export default BackBtn;
