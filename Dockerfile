# oscad

FROM alpine:latest

LABEL maintainer="dev@starck.fi"

COPY wrapper.sh /usr/local/bin/openstack-wrapper.sh

RUN set -x \
  && chmod -c 755 /usr/local/bin/openstack-wrapper.sh \
  && apk add --no-cache --update build-base git linux-headers py-pip python-dev \
  && pip install git+https://github.com/openstack/python-openstackclient.git

VOLUME /opt

ENTRYPOINT ["/usr/local/bin/openstack-wrapper.sh"]
