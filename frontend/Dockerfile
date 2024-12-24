FROM node:23-alpine AS build

COPY package.json package-lock.json

RUN npm install -g npm@latest

COPY . ./

RUN npm run build

FROM nginx:alpine

COPY --from=build /build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
