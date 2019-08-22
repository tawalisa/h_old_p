FROM openjdk:8-jdk-alpine
ENV JAVA_HOME=/usr/lib/jvm/default-jvm/jre
RUN mkdir /jar
RUN mkdir /code
RUN mkdir /cert 

ADD ./cert/ca.cert.pem /ca.cert.pem

RUN /usr/lib/jvm/default-jvm/jre/bin/keytool -import -file /ca.cert.pem -keystore /tmp/truststore.jks -alias rootca -storepass 123456 -noprompt -trustcacerts

ENV CLASSPATH=/jar/unboundid-ldapsdk-4.0.8.jar:/code

WORKDIR  /code

CMD ["java Test"]
