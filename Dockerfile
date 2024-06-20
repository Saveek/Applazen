# Builder stage
FROM node:18 as builder
WORKDIR /usr/src/app
COPY package*.json ./
RUN yarn install --quiet
COPY . ./
RUN yarn build  # Make sure this step is included

# Production stage
FROM nginx:stable-alpine as production-stage
WORKDIR /usr/share/nginx/html
COPY --from=builder /usr/src/app/build .
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
