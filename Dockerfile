# oscad

FROM alpine:latest

LABEL maintainer="dev@starck.fi"

COPY unannoy.patch /tmp/unannoy.patch
COPY wrapper.sh /usr/local/bin/openstack-wrapper.sh

RUN set -x \
  && mkdir /vol \
  && chmod -c 755 /usr/local/bin/openstack-wrapper.sh \
  && apk add --no-cache --update build-base git linux-headers py-pip python-dev

RUN set -x \
  && pip install git+https://github.com/openstack/python-openstackclient.git

RUN set -x \
  && pip install git+https://github.com/openstack/python-heatclient.git \
  && pip install git+https://github.com/openstack/python-novaclient.git \
  && pip install git+https://github.com/openstack/python-swiftclient.git

RUN set -x \
  && patch -p0 < /tmp/unannoy.patch

VOLUME /vol

ENTRYPOINT ["/usr/local/bin/openstack-wrapper.sh"]
