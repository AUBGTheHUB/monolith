import asyncio

from service.mail_service.resend_service import ResendMailService

async def main():
    resend = ResendMailService()

    return await resend.send_participant_verification_email(
        "klevi1255@gmail.com",
        "SUBJECT",
    "Klevi",
        "Team 1",
        "https://google.com"
    )

if __name__ == '__main__':
    print(asyncio.run(main()))
