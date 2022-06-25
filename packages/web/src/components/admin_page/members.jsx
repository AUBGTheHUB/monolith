import React from "react";
import axios from "axios";
import { useLocation, useNavigate } from "react-router-dom";
import { Button } from "react-bootstrap";
import RenderMembers from "./render_members";
import { useState } from "react";

const Members = () => {
  const history = useNavigate();
  const location = useLocation();
  let state_of_validated;
  const val = location.state;

  if (val === null) {
    state_of_validated = false;
  } else {
    state_of_validated = location.state.validated;
  }

  const [loading, setLoading] = useState(true);
  const [members, setMembers] = useState([{}])

  const getMembers = () => {
    axios({
      method: "get",
      url: "http://127.0.0.1:8000/api/members",
    })
      .then((res) => {
        setLoading(false);
        setMembers(res.data.data.data)
      })
      .catch((err) => {
        console.log(err);
      });
  };

  getMembers()


  if (state_of_validated) {
    if (loading) {
      return <h3>Awaiting data!</h3>;
    } else {
      return (
        <div className="members-div">
          {
            members[0].firstname
          }
          {/* <RenderMembers members={members} /> */}
        </div>
      );
    }
  } else {
    return (
      <div className="client-not-validated">
        <div>
          <h3>Client is not validated</h3>
          <Button
            onClick={() => {
              history("/admin/");
            }}
          >
            Return to login page
          </Button>
        </div>
      </div>
    );
  }
};

export default Members;
