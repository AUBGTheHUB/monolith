import { Body, Container, Head, Html, Img, Section, Text, Link } from '@react-email/components';
import * as React from 'react';

export const ParticipantWelcomeEmail = () => (
    <Html>
        <Head>
            <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet" />
            <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&display=swap" rel="stylesheet" />
        </Head>
        <Body style={main}>
            <Container style={container}>
                <Section>
                    <Text style={title}>
                        Welcome to HackAUBG 5.0, <br /> <br /> {`{participantName}`}
                    </Text>
                    <br /> <br />
                    <Text style={paragraph as React.CSSProperties}>
                        Before the hackathon starts, there are a few <span style={highlight}>important things:</span>
                    </Text>
                    <Text style={paragraph as React.CSSProperties}>
                        You can view your payments and a variety of other information about your account right from your
                        dashboard.
                    </Text>
                    <Text style={paragraph as React.CSSProperties}>
                        To ensure you stay in the loop, we will invite you to join the Official HackAUBG 5.0 Facebook
                        group. That is where we'll share all the latest updates and instructions about the event.
                    </Text>
                    <Text style={paragraph as React.CSSProperties}>
                        What's more, each team will have their very own <span style={highlight}>facilitator</span> from
                        The Hub to guide you through the hackathon. They'll be your point of contact for any questions
                        or concerns you may have and will even help you find new teammates if needed.
                    </Text>
                    <Text style={paragraph as React.CSSProperties}>
                        Make sure to follow our social media accounts for updates about the event and exciting upcoming
                        surpises -{' '}
                        <Link href="https://www.facebook.com/TheHubAUBG" style={highlight}>
                            Facebook
                        </Link>
                        ,{' '}
                        <Link href="https://www.instagram.com/thehubaubg/" style={highlight}>
                            Instagram
                        </Link>{' '}
                        and{' '}
                        <Link href="https://www.linkedin.com/company/the-hub-aubg/mycompany/" style={highlight}>
                            Linkedin
                        </Link>
                    </Text>
                    <Text style={paragraph as React.CSSProperties}>
                        We're thrilled to have you on board and can't wait to meet you!
                    </Text>
                    <Text style={paragraph as React.CSSProperties}>
                        <span style={highlight}>See you soon! - The Hub AUBG</span>
                    </Text>
                </Section>
            </Container>
            <Img src={'../static/moon-email.png'} width="100%" height="100%" />
        </Body>
    </Html>
);

export default ParticipantWelcomeEmail;

const main = {
    fontFamily: "'IBM Plex Mono', monospace",
    backgroundImage: `url(../static/moon-particles-5.png)`,
    margin: '0',
};

const title = {
    fontFamily: "'Press Start 2P'",
    color: '#FFFFFF',
    textAlign: 'center' as 'center',
    fontSize: '25px',
};

const container = {
    margin: '0 auto',
    padding: '20px 0 48px',
    color: '#FFFFFF',
    backgroundColor: 'rgba(0, 0, 0, 1.5)',
};

const paragraph = {
    fontSize: '16px',
    color: '#FFFFFF',
    lineHeight: '24px',
    textAlign: 'center',
    textShadow: '0px 0px 8px rgba(0, 0, 0, 0.8)',
};

const highlight = {
    color: '#C298F3',
};
