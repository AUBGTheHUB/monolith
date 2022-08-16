import React, { useEffect } from "react";
import axios from "axios";
import { useLocation, useNavigate } from "react-router-dom";
import { Button } from "react-bootstrap";
import RenderMembers from "./render_members";
import { useState } from "react";
import url from "../../../Global";

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
  const [members, setMembers] = useState([{}]);


  const getMembers = () => {
    axios({
      method: "get",
      url: url + "/api/members",
    })
      .then((res) => {
        setMembers(res.data.data.data);
        setLoading(false)
      })
      .catch((err) => {
        console.log(err);
      });
  };

  useEffect(()=>{
    getMembers()
  }, [])


  if (state_of_validated) {
    if(loading){
      return <h3>Fetching data!</h3>
    } else {
      return <RenderMembers members={members}/>
    }
  } else {
    return(
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
    </div>);
  }
};

export default Members;
