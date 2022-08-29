import axios from 'axios';
import { useEffect, useState } from 'react';

const url = 'http://127.0.0.1:8000';

const Validate = () => {
  const [validated, setValidated] = useState(false);
  useEffect(() => {
    axios({
      method: 'post',
      url: url + '/api/validate',
      headers: { BEARER_TOKEN: localStorage.getItem('auth_token') }
    })
      // eslint-disable-next-line no-unused-vars
      .then((res) => { 
        setValidated(true);
      })
      // eslint-disable-next-line no-unused-vars
      .catch((err) => {
        setValidated(false);
      });
  }, []);

  return validated;
};
export { url };
export default Validate;

/*

    this is how you should handle the validation of the client

        if (Validate()) {
            something something
        } else {
            <InvalidClient/>
        }

*/
