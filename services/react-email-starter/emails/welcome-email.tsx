import { Body, Container, Head, Hr, Html, Img, Link, Preview, Section, Text } from '@react-email/components';
import * as React from 'react';

export const WelcomeEmail = () => (
    <Html>
        <Head />
        <Preview>You&apos;re now verified for HackAUBG 7.0</Preview>
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
                        Before the hackathon starts, there are a few <Link style={anchor}>important things:</Link>
                    </Text>
                    <Section style={invite_link}>
                        <Text style={invite_link}>{`{invite_link_statement}`}</Text>
                    </Section>
                    <Text style={paragraph}>
                        To ensure you stay in the loop, we will invite you to join the Official HackAUBG 7.0 Facebook
                        group. That is where we&apos;ll share all the latest updates and instructions about the event.
                    </Text>
                    <Text style={paragraph}>
                        What&apos;s more, each team will have their very own <Link style={anchor}>facilitator</Link>{' '}
                        from The Hub to guide you through the hackathon. They&apos;ll be your point of contact for any
                        questions or concerns you may have and will even help you find new teammates if needed.
                    </Text>
                    <Text style={paragraph}>
                        Make sure to follow our social media accounts for updates about the event and exciting upcoming
                        surpises -{' '}
                        <Link style={anchor} href="https://www.facebook.com/TheHubAUBG">
                            Facebook
                        </Link>
                        ,{' '}
                        <Link style={anchor} href="https://www.instagram.com/thehubaubg/">
                            Instagram
                        </Link>
                        {', and '}
                        <Link style={anchor} href="https://www.linkedin.com/company/the-hub-aubg/mycompany/">
                            Linkedin.
                        </Link>
                    </Text>
                    <Text style={paragraph}>
                        We&apos;re thrilled to have you on board and can&apos;t wait to meet you!
                    </Text>
                    <Text style={paragraph}>See you soon!</Text>
                    <Text style={paragraph}>&mdash; The Hub AUBG</Text>
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

export default WelcomeEmail;

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

const invite_link = {
    color: '#525f7f',
    fontSize: '16px',
    lineHeight: '24px',
    maxWidth: '600px',
    textAlign: 'left' as const,
    wordBreak: 'break-all' as const,
    overflowWrap: 'break-word' as const,
    whiteSpace: 'normal' as const,
};

const anchor = {
    color: '#365ED4',
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
