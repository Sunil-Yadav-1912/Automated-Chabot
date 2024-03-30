# Python_chabot
Personally created chatbot for ease of information and faster access  to important data. for the internal users of creditfair as well as their customers and merchants. 

Major Modules

1. Authorization  Module: This module is responsible for handling the authorization of users to access different functionalities and resources within authguard also called as middleware which uses JWT auth system.

2. Logging  Module: This module is responsible for logging all the activities of the chabot in a log file as well as on AWS Cloudwatch too which keeps all the logs safe and private. AWS integration is of our company's account hence you have to create your account for AWS logging if not needed comment out the module and just keep the file logger.

3. Environment Modules: Whole project depends on the environment module and it's variables defined in the env file but due to privacy policy I have cleared the env values you need to put your database credentials and keys for proper running of the project.

4. Docker file: This file is used to build a docker image of the chabot application. It contains all the necessary commands and configurations needed for running the project and to use it as a microservice in any other project.

5. Encryption and Decryption Module: This module is responsible for encrypting and decrypting the values that are stored in the database privately. 

6. AWS S3 Module: This module is used to interact with the Amazon Web Services (AWS) Simple Storage Service (S3). It provides methods for uploading files or getting the files through amazon cloud storage.

7. Whatsapp APIs: Integrated this to access the chatbot information through whatsapp messaging platform. The API is made seperately to interact with whatsapp 

8. Backend (Python): Handles all the logic behind the scene.

9. Frontend (html, css, js): Displays what users see and interact with. Also integrated with document and voice modules.

