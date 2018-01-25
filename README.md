# Project Overview

## Objectives

[SD]RSiX project aims, firstly, to automate Layer 2 deployments in an Internet Exchange Point (IXP). In Brazilian IXPs, the connected Autonomous Systems (ASes) exchange traffic multilaterally using two VLANs, one for IPv4 and the other for IPv6, and bilaterally using VLANs defined by the IXP to connect two or more ASes.

Bilateral VLANs creation and MAC filter updates represent about 40% of the total of the tickets open [1]. Add to that connecting or removing an AS requires configuring VLANs (two or more), filters, and the management system. All these operations may be automated reducing manual e repetitive work, and consequently turning the workflow more reliable.

The SDN approach of the Layer 2 enables an SDN approach for the management, integrating OpenFlow counters with traditional monitoring protocols gathered in a fully automated system.
_____________________________________________

[1] Statistics got from the Brazilian IXP tickets system ([my.ix.br](https://my.ix.br)) database.

## Technical Details

It consists of [Ryu SDN framework](https://osrg.github.io/ryu/) application and files that enable it to run on a Docker container.

This project has been developed together with [\[SD\]RSiX Lab](https://bitbucket.org/sd-rsix/sd-rsix-lab) project, which is a testbed environment that simulates the [RSiX Internet Exchange Point infrastructure](http://ix.br/trafego/pix/rs) on a small scale. Although, can be run independently of the Lab by running the application in the _src_ folder using _ryu-manager_.

The _docker-compose.yml_ file creates the container to run the application with the __10.10.10.254__ IP address attached to the _sd_rsix_ Docker network. If you want to run this application using Docker, without the [\[SD\]RSiX Lab](https://bitbucket.org/sd-rsix/sd-rsix-lab), you must change network parameters in _docker-compose.yml_ file.

## Team

This project has been maintained/developed by RSiX team and researchers from the [Informatics Institute](http://www.inf.ufrgs.br/site/) of the [Federal University of Rio Grande do Sul](http://www.ufrgs.br/english/home).


# Building and Running

## Requirements

You only need installed on your machine the following:

 * [Docker](https://www.docker.com/)
 * [Docker Compose](https://docs.docker.com/compose/)

## Creating the Docker network

If you already configured the [SD]RSiX Lab, jump to the next section. If not, run the following and jump this step when you configure de Lab:

```
docker network create --subnet=10.10.10.0/24 --gateway=10.10.10.1 sd_rsix
```

## Running

Run the following command from inside the project's root folder:

```
docker-compose up
```

Every time you change the code in _src_ folder you need to deploy de container again. You can do that running the command below:

```
## Rebuilds the image and starts the controller container
docker-compose up --build
```

If you want to remove everything created by the _docker-compose_ script, run:

```
# Remove container, network and the image locally generated:
docker-compose down --rmi local
```
