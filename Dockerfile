# k5utils

FROM alpine:latest

LABEL maintainer="dev@starck.fi"

RUN set -x \
  && apk add --no-cache --update bash build-base curl git jq linux-headers py-pip python-dev \
  && pip install git+https://github.com/openstack/python-openstackclient.git

RUN set -x \
  && pip install git+https://github.com/openstack/python-heatclient.git \
  && pip install git+https://github.com/openstack/python-novaclient.git \
  && pip install git+https://github.com/openstack/python-swiftclient.git

COPY initrc /root/.bashrc
COPY unannoy.patch /tmp/unannoy.patch
COPY k5-image-import /usr/local/bin/k5-image-import

RUN set -x \
  && mkdir /vol \
  && patch -p0 < /tmp/unannoy.patch \
  && chmod -c 755 /usr/local/bin/k5-image-import

VOLUME /vol

ENTRYPOINT ["/bin/bash"]
