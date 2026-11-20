FROM ubuntu:26.04
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    asterisk iproute2 python3 sip-tester sudo tcpdump tshark util-linux \
    && rm -rf /var/lib/apt/lists/*
RUN if id ubuntu >/dev/null 2>&1; then userdel ubuntu; fi
WORKDIR /opt/callpath
RUN module=$(dpkg-query -L asterisk-modules | sed -n '/\/chan_pjsip\.so$/p') \
    && test -f "$module" && ln -s "$(dirname "$module")" /opt/callpath/asterisk-modules
COPY callpath callpath
COPY network network
COPY asterisk asterisk
COPY scenarios scenarios
RUN cd scenarios && python3 ../network/tone.py
RUN printf '%s\n' 'Defaults:callpath !use_pty' 'callpath ALL=(root) NOPASSWD: /usr/bin/python3 -I /opt/callpath/network/helper.py *' \
      > /etc/sudoers.d/callpath \
    && chmod 0440 /etc/sudoers.d/callpath && visudo -cf /etc/sudoers.d/callpath
ENV PYTHONPATH=/opt/callpath PYTHONDONTWRITEBYTECODE=1 LC_ALL=C.UTF-8
ENTRYPOINT ["/opt/callpath/network/entrypoint"]
