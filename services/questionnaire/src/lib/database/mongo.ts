import { MongoClient } from 'mongodb';
import { MONGOURI } from '$env/static/private';

const client = new MongoClient(MONGOURI);

export function start_mongo() {
    console.log('Starting mongo...');
    return client.connect();
}

const db = client.db('questionnaires');
export const questions = db.collection('questions');
export const answers = db.collection('answers');
