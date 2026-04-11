FROM eclipse-temurin:17-jdk-alpine AS build
WORKDIR /app
COPY backend/ ./backend/
COPY gradle/ ./gradle/
COPY build.gradle.kts settings.gradle.kts gradle.properties gradlew ./
RUN chmod +x gradlew
RUN ./gradlew :backend:buildFatJar --no-daemon

FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=build /app/backend/build/libs/notex-api.jar ./notex-api.jar
EXPOSE 8080
ENV PORT=8080
CMD ["java", "-jar", "notex-api.jar"]
