import { Body, Container, Head, Hr, Html, Img, Link, Preview, Section, Text, Button } from '@react-email/components';
import * as React from 'react';

export const VerificationEmail = () => (
    <Html>
        <Head />
        <Preview>Secure your spot at HackAUBG 7.0</Preview>
        <Body style={main}>
            <Container style={container}>
                <Section style={box}>
                    <Section style={{ backgroundColor: '#365ED4', padding: '20px 48px' }}>
                        <Img
                            src="https://hubarskibucket.s3.eu-central-1.amazonaws.com/thehub-logo-white.png"
                            width="136"
                            height="40"
                            alt="The Hub Logo"
                        />
                    </Section>
                    <Hr style={hr} />
                    <Text style={title}>
                        Welcome to HackAUBG 7.0, <br />
                        {`{participant_greeting}`}!<br />
                    </Text>
                    <Text style={paragraph}>
                        Thank you for registering for our seventh <Link style={anchor}>annual hackathon!</Link>
                    </Text>
                    <Text style={paragraph}>
                        We are extremely excited to have you on board and can&apos;t wait to see what{' '}
                        <Link style={anchor}>you&apos;ll create!</Link>
                    </Text>
                    <Text style={paragraph}>Before your adventure at the hackathon starts, you&apos;ll have to:</Text>
                    <br />
                    <Button href={`{verification_link}`} style={button}>
                        Verify
                    </Button>
                    <br />
                    <Hr style={hr} />
                    <Text style={footer}>
                        <Link style={anchor} href="https://thehub-aubg.com/hackathon">
                            HackAUBG 7.0
                        </Link>
                    </Text>
                </Section>
            </Container>
        </Body>
    </Html>
);

export default VerificationEmail;

const main = {
    backgroundColor: '#f6f9fc',
    fontFamily: '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Ubuntu,sans-serif',
};

const container = {
    backgroundColor: '#ffffff',
    margin: '0 auto',
    padding: '20px 0 48px',
    marginBottom: '64px',
    maxWidth: '600px',
};

const box = {
    padding: '0 48px',
};

const hr = {
    borderColor: '#e6ebf1',
    margin: '20px 0',
};

const paragraph = {
    color: '#525f7f',
    fontSize: '16px',
    lineHeight: '24px',
    textAlign: 'left' as const,
};

const anchor = {
    color: '#365ED4',
};

const button = {
    backgroundColor: '#365ED4',
    borderRadius: '5px',
    color: '#fff',
    fontSize: '16px',
    fontWeight: 'bold',
    textDecoration: 'none',
    textAlign: 'center' as const,
    display: 'block',
    width: '70%',
    padding: '10px',
    margin: '0 auto',
};

const footer = {
    color: '#8898aa',
    fontSize: '12px',
    lineHeight: '16px',
};

const title = {
    color: '#000000',
    fontSize: '27px',
    lineHeight: '1.5em',
    textAlign: 'center' as const,
    marginBottom: '30px',
};
