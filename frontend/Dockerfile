FROM node:23-alpine AS build

WORKDIR /app

RUN npm cache clean --force

COPY package.json package-lock.json ./

RUN npm install -g npm@latest

RUN npm install

COPY . .

RUN npm run build

FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
