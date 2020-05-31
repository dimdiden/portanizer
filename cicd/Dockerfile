
ARG ALPINE=arm64v8/alpine:3.11
FROM ${ALPINE} AS alpine
ARG ARCH
ARG KUBERNETES_RELEASE=v1.17.0
ARG ARCH=arm64
WORKDIR /bin
RUN set -x \
    && apk --no-cache add curl \
    && curl -fsSLO https://storage.googleapis.com/kubernetes-release/release/${KUBERNETES_RELEASE}/bin/linux/${ARCH}/kubectl \
    && chmod +x kubectl

CMD ["cat"]