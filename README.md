NodeJS Builder image
===================

This repository has a Docker container with Crontab service and a UI from 
[https://github.com/alseambusher/crontab-ui](https://github.com/alseambusher/crontab-ui)
This source is based on [ryanj/origin-s2i-nodejs](https://github.com/ryanj/origin-s2i-nodejs/) and [windperson/docker-crontab](https://github.com/windperson/docker-crontab)

CentOS based builder images with Nodejs binaries from nodejs.org.
The resulting image can be run using [Docker](http://docker.io).

If you are interested in using SCL-based nodejs binaries, try [sti-nodejs](https://github.com/openshift/sti-nodejs)

Usage
---------------------
To build a simple [nodejs example app](https://github.com/brunoemer/crontab-ui/) application using standalone [STI](https://github.com/openshift/source-to-image):

```
$ docker build -t s2i-crontab-ui-base .
$ s2i build https://github.com/brunoemer/crontab-ui s2i-crontab-ui-base s2i-crontab-ui
```

Run the resulting image with [Docker](http://docker.io):

```
$ docker run -it --name s2i-crontab-ui -p 8099:8000 -e HOST='0.0.0.0' s2i-crontab-ui
```

Access the application:
```
$ curl 127.0.0.1:8000
```

Import local image to registry
```
$ oc get svc -n default | grep registry #get registry ip
$ docker tag s2i-crontab-ui docker-registry.default.svc:5000/teste/s2i-crontab-ui #tag a local image
$ oc login xxx
$ oc whoami -t # get token to login docker registry
$ docker login -u user -e email -p token docker-registry.default.svc:5000
$ docker push docker-registry.default.svc:5000/teste/s2i-crontab-ui # push a image
```

Default user and password:
#### User: admin
#### Password: admin

Repository organization
------------------------
* **`nodejs.org`**

    * **Dockerfile**

        CentOS based Dockerfile with 64bit nodejs binaries from nodejs.org.

    * **Dockerfile.sourcebuild**

        CentOS based Dockerfile, nodejs binaries built from source (downloaded from nodejs.org).

    * **`s2i/bin/`**

        This folder contains scripts that are run by [STI](https://github.com/openshift/source-to-image):

        *   **assemble**

            Used to install the sources into the location where the application
            will be run and prepare the application for deployment (eg. installing
            modules using npm, etc.)

        *   **run**

            This script is responsible for running the application, by using the
            application web server.

        *   **usage***

            This script prints the usage of this image.

    * **`contrib/`**

        This folder contains a file with commonly used modules.

    * **`test/`**

        This folder contains the [S2I](https://github.com/openshift/source-to-image)
        test framework with simple Node.JS echo server.

        * **`test-app/`**

            A simple Node.JS echo server used for testing purposes by the [S2I](https://github.com/openshift/source-to-image) test framework.

        * **run**

            This script runs the [S2I](https://github.com/openshift/source-to-image) test framework.

Environment variables
---------------------

Application developers can use the following environment variables to configure the runtime behavior of this image:

NAME        | Description
------------|-------------
NPM_RUN     | Select an alternate / custom runtime mode, defined in your `package.json` file's [`scripts`](https://docs.npmjs.com/misc/scripts) section (default: npm run "start")
NODE_ENV    | NodeJS runtime mode (default: "production")
HTTP_PROXY  | use an npm proxy during assembly
HTTPS_PROXY | use an npm proxy during assembly

One way to define a set of environment variables is to include them as key value pairs in your repo's `.s2i/environment` file.

Example: DATABASE_USER=sampleUser

#### NOTE: Define your own "`DEV_MODE`":

The following `package.json` example includes a `scripts.dev` entry.  You can define your own custom [`NPM_RUN`](https://docs.npmjs.com/cli/run-script) scripts in your application's `package.json` file.

### Using Docker's exec

To change your source code in a running container, use Docker's [exec](http://docker.io) command:
```
$ docker exec -it <CONTAINER_ID> /bin/bash
```

After you [Docker exec](http://docker.io) into the running container, your current directory is set to `/opt/app-root/src`, where the source code for your application is located.

### Using OpenShift's rsync

If you have deployed the container to OpenShift, you can use [oc rsync](https://docs.openshift.org/latest/dev_guide/copy_files_to_container.html) to copy local files to a remote container running in an OpenShift pod.
