.. webcentral documentation master file, created by
   sphinx-quickstart on Tue May 30 14:28:04 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to EWB Wissensplattform documentation!
======================================

Introduction
------------
The shift from a traditional supply infrastructure to a regenerative, decentralized energy system increased complexity and necessitates the integration of previously independent sectors. The efficient operation of these systems relies on modern IT communication and control technologies. This transition poses significant changes and new challenges for all stakeholders, alongside a substantial need for research.
Research, development, and innovation projects in the field of `Energiewendebauen <https://www.energiewendebauen.de/>`_, as well as real-world energy transition laboratories, focus on various aspects of this multifaceted topic. They conduct in-depth analyses of the economic, political, and user-specific requirements and challenges.
A key objective of the EWB Wissensplattform is to simplify and disseminate the findings from these projects.  It serves as a repository where knowledge is aggregated and tailored for different user groups. The platform emphasizes the visual presentation of data, examines the impacts of varying conditions, and facilitates the application of technological advancements. It also involves the verification of digital tools and supports the testing and development of new methodologies.
web interface with data base system of project infromation of the "Begleitforschung Energiewendebauen 2020" (focus modul digitalization).

Structure of the documentation
------------------------------
The documentation is structured into two parts. The first part is intended for the end-user of the plattform. It explains topics, which are relvant to the end-user. Everything is explained from a high level view.

The second part holds holds the developer guide where everthing is explained in more detail. 

End user guide
==============

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   general/getting_started
   general/basic_structure
   general/interacting_with_the_app
   general/configuration_env_file
   general/structure_project_repo
   general/data_model
   general/data_import
   general/migrations
   general/production

Developer guide
===============

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   dev/template_structure
   dev/style_guide
   dev/static_code_analysis
   dev/pyproject_toml
   dev/testing
   dev/load_profiles
   dev/plotly_apps
   dev/csp
   dev/use_cases
   dev/save_page_views
   dev/data_import
   dev/data_export

HowTo Guides
============
.. toctree::
   :maxdepth: 2
   :caption: HowTo:
   
   HowTo/create_dump_for_repo
   HowTo/rollback_tool


Old to be refactored
====================
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installtion_basics
   dataImportDjango
   insertLinksInDatabase
   templateStructure
   translation
   listing_pages
   testing


   

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
