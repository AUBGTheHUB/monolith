import { MongoClient } from 'mongodb';
import { MONGOURI } from '$env/static/private';

const client = new MongoClient(MONGOURI);

export function start_mongo() {
    console.log('Starting mongo...');
    return client.connect();
}

export const db = client.db();
export const questions = db.collection('questions');
