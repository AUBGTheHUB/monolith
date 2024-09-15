// src/MockDataComponent.tsx

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchMockData, MockData } from './mockResponse';

const MockDataComponent: React.FC = () => {
    const { data, error, isLoading } = useQuery<MockData>({
        queryKey: ['mockData'],
        queryFn: fetchMockData,
        retry: 1,
    });

    return (
        <div>
            <h2>React Query Test</h2>
            {isLoading && <p>Loading...</p>}
            {error && <p>Error: {error.message}</p>}
            {data && <p>Data: {data.data}</p>}
        </div>
    );
};

export default MockDataComponent;
