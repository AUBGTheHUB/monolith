FROM rust:latest

WORKDIR /usr/src/app

COPY . .

RUN cargo build --release

RUN ls -l ./target/release/

EXPOSE 8001

CMD ["./target/release/url_shortener"]
