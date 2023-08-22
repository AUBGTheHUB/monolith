import { Card, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

export const LandingCard = ({ title, text, url, description }) => {
    const history = useNavigate();
    return (
        <Card className="card-dash-landing">
            <Card.Body>
                <Card.Title>{title}</Card.Title>
                <Card.Text>{text}</Card.Text>
                <Button
                    variant="primary"
                    onClick={() => {
                        history(url);
                    }}
                >
                    {description}
                </Button>
            </Card.Body>
        </Card>
    );
};
