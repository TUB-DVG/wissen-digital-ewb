Getting started
---------------
In this document a short summary of the project goal is given. Afterwards it is described how the setup in a development and production environment can be done.

WenDE – Wissensplattform
========================
The shift from a traditional supply infrastructure to a regenerative, decentralized energy system introduces increased complexity and necessitates the integration of previously independent sectors. The efficient operation of these systems relies on modern IT communication and control technologies. This transition poses significant changes and new challenges for all stakeholders, alongside a substantial need for research.
Research, development, and innovation projects in the field of Energiewende construction, as well as real-world energy transition laboratories, focus on various aspects of this multifaceted topic. They conduct in-depth analyses of the economic, political, and user-specific requirements and challenges.
A key objective of the WeNDE project is to simplify and disseminate the findings from these projects. The EWB knowledge platform is being developed as a central element of this initiative. It serves as a repository where knowledge is aggregated and tailored for different user groups. The platform emphasizes the visual presentation of data, examines the impacts of varying conditions, and facilitates the application of technological advancements. It also involves the verification of digital tools and supports the testing and development of new methodologies.
web interface with data base system of project infromation of the "Begleitforschung Energiewendebauen 2020" (focus modul digitalization).

Main concept
============
The Web-Application consists of 3 services, which are containerized, each of them living in a seperate container. In the backend the python based Django-Framework is used. Data is stored in a relational-database, whereby as a DBMS PostgreSQL is chosen. A nginx-instance is used as reverse-proxy to redirect HTTP-requests to the Django-Backend, using the uwsgi-protocol. Static-content is directly served by nginx, since it has access to a Docker-Volume, which is shared with the Django-application.

To start the project either in development-mode or in production-mode `docker <https://www.docker.com/>`_  together with `docker compose <https://github.com/docker/compose>`_ are needed on your local system. Depending on your operating system (OS), the installation may differ. Please consult the guide provided by `docker <https://docs.docker.com/engine/install/>`_ for your OS.

After that please clone the repo to a local location of your choice. 
The application can be executed by doing the following steps:
1. Create a .env-file from the the .env.example file.
`
  cp .env.example .env
`
2. Start the setup process by calling the run script with the argument `up_initial` and providing a database dump file.
`
  ./run up_initial dev postgres/databaseDump.sql
`
For simplicity it was asumed that a database dump is located in the postgres/ folder inside the root-folder of the webcentral-repository. That command will populate the database with the data present in the database dump and will start the web-application in development mode afterwards. It can the be visited on a browser of choice by going to the link `http://127.0.0.1:8000`.
