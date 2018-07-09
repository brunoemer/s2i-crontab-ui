FROM ryanj/centos7-s2i-nodejs:6.4.0

# This image provides a Node.JS environment you can use to run your Node.JS
# applications.

MAINTAINER Bruno Emer <emerbruno@gmail.com>

EXPOSE 8000

# This image will be initialized with "npm run $NPM_RUN"
# See https://docs.npmjs.com/misc/scripts, and your repo's package.json
# file for possible values of NPM_RUN
ENV NPM_RUN=start \
    NPM_CONFIG_LOGLEVEL=info \
    NPM_CONFIG_PREFIX=$HOME/.npm-global \
    PATH=$HOME/node_modules/.bin/:$HOME/.npm-global/bin/:$PATH \
    DEBUG_PORT=5858 \
    NODE_ENV=production \
    DEV_MODE=false

LABEL io.k8s.description="Platform for building and running Node.js applications" \
      io.k8s.display-name="Node.js v$NODE_VERSION" \
      io.openshift.expose-services="8000:http" \
      io.openshift.tags="builder,nodejs,nodejs$NODE_VERSION" \
      com.redhat.deployments-dir="/opt/app-root/src"

# Copy the S2I scripts from the specific language image to $STI_SCRIPTS_PATH
COPY ./s2i/bin/ $STI_SCRIPTS_PATH

# Each language image can have 'contrib' a directory with extra files needed to
# run and build the applications.
COPY ./contrib/ /opt/app-root

# Install crontab dependendecies
USER 0
RUN yum install -y supervisor
COPY supervisord.conf /etc/supervisord.conf
RUN usermod -u 1000130000 default
ENV HOST 0.0.0.0
ENV PORT 8000
ENV CRON_PATH /etc/crontabcustom
ENV CRON_IN_DOCKER true
RUN mkdir -p /etc/crontabcustom && chown -R 1000130000:0 /etc/crontabcustom && chmod -R g+w /etc/crontabcustom
RUN mkdir -p /var/log/crontab && chown -R 1000130000:0 /var/log/crontab && chmod -R g+w /var/log/crontab

ENV CIRCUS_LOG_LEVEL info
RUN yum install -y python2-pip python-devel
RUN pip install --no-cache-dir circus
COPY circus.ini /etc/circus/
COPY cron /opt/app-root/cron
RUN pip install --no-cache-dir -r /opt/app-root/cron/requirements.txt

RUN chmod -R g+rw /opt/app-root/
# Drop the root user and make the content of /opt/app-root owned by user 1001
RUN chown -R 1000130000:0 /opt/app-root
USER 1000130000

# Set the default CMD to print the usage of the language image
CMD $STI_SCRIPTS_PATH/usage
