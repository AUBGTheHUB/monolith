import Validate, { gcpToken, objUploaderURL } from '../../../Global';
import axios from 'axios';
import { useState } from 'react';
import { useEffect } from 'react';
import InvalidClient from '../invalid_client';
import { ObjectCard } from './obj_card';

export const RenderStorageObjects = () => {
    const [objects, setObjects] = useState();

    const getObjects = () => {
        axios({
            method: 'post',
            headers: {
                Authorization: gcpToken
            },
            url: objUploaderURL + '?show=true'
        })
            .then((res) => {
                console.log(res);
                setObjects(res.data.message);
            })
            // eslint-disable-next-line
            .catch((err) => {
                // do nothing
            });
    };

    useEffect(getObjects, []);
    if (Validate()) {
        if (objects) {
            return (
                <div className="s3-space-around">
                    {objects.map((url, index) => (
                        <ObjectCard url={url} key={index} />
                    ))}
                </div>
            );
        } else {
            return <p>No Objects</p>;
        }
    }

    return <InvalidClient />;
};
