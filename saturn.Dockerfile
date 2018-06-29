FROM maven:alpine

# Set working directory
WORKDIR /saturn

# Copy current host directory to container working directory
ADD . .

RUN apk add --update nodejs-npm
RUN npm install

CMD ["mvn", "spring-boot:run"]
