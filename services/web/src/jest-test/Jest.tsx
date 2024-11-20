import React, { useState } from 'react';

const STATUS = {
    HOVERED: 'hovered',
    NORMAL: 'normal',
} as const;

const Link: React.FC = () => {
    const [status, setStatus] = useState<(typeof STATUS)[keyof typeof STATUS]>(STATUS.NORMAL);

    const onMouseEnter = () => {
        setStatus(STATUS.HOVERED);
    };

    const onMouseLeave = () => {
        setStatus(STATUS.NORMAL);
    };

    return (
        <a className={status} href="#" onMouseEnter={onMouseEnter} onMouseLeave={onMouseLeave}>
            Link
        </a>
    );
};



export default Link;
