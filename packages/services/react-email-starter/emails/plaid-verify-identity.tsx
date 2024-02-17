import { Body, Container, Head, Heading, Html, Img, Link, Section, Text } from '@react-email/components';
import * as React from 'react';

interface PlaidVerifyIdentityEmailProps {
    validationCode?: string;
}

const baseUrl = process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : '';

export const PlaidVerifyIdentityEmail = ({ validationCode }: PlaidVerifyIdentityEmailProps) => (
    <Html>
        <Head />
        <Body style={main}>
            <Container style={container}>
                <Link href="{verifyLink}" style={link}>
                    Click here
                </Link>
            </Container>
        </Body>
    </Html>
);

PlaidVerifyIdentityEmail.PreviewProps = {
    validationCode: '144833',
} as PlaidVerifyIdentityEmailProps;

export default PlaidVerifyIdentityEmail;

const main = {
    backgroundColor: '#ffffff',
    fontFamily: 'HelveticaNeue,Helvetica,Arial,sans-serif',
};

const container = {
    backgroundColor: '#ffffff',
    border: '1px solid #eee',
    borderRadius: '5px',
    boxShadow: '0 5px 10px rgba(20,50,70,.2)',
    marginTop: '20px',
    maxWidth: '360px',
    margin: '0 auto',
    padding: '68px 0 130px',
};

const link = {
    color: '#444',
    textDecoration: 'underline',
};
