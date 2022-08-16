import React from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "react-bootstrap";

const InvalidClient = () => {
    const history = useNavigate();
    return (
        <div className="client-not-validated">
        <div>
            <h3>Client is not validated</h3>
            <Button onClick={() => {
            history("/admin/");
            }
            }>Return to login page</Button>
        </div>
        </div>
    );
}

export default InvalidClient;