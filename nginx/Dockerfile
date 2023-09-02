# Use the official Nginx base image
FROM nginx:latest

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
EXPOSE 443
EXPOSE 3000
EXPOSE 3001
EXPOSE 6969
EXPOSE 8000

CMD ["nginx", "-g", "daemon off;"]
