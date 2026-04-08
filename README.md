# Project Overview 

This project aims to design and prototype a cloud-based architecture for collecting, storing, and analyzing telemetry data from domestic photovoltaic (PV) systems. The proposed architecture retrieves operational metrics through an embedded edge device connected to the PV inverter and transmits the data to a cloud infrastructure where it is processed, stored, and visualized. 

The primary objective of the project is to validate an end-to-end IoT telemetry pipeline capable of supporting data collection for a range of domestic PV inverters. The system provides a visualization dashboard that allows users to inspect energy production trends and monitor the operational status of their PV installation. 

At the current implementation stage, the prototype includes a basic alerting mechanism for common PV plant malfunctions, such as the absence of energy production during daylight hours. 

As future work, the system could incorporate a machine learning pipeline deployed on Amazon SageMaker to analyze historical telemetry data and detect abnormal behavior in the PV plant, enabling anomaly detection and predictive maintenance capabilities. 


# Architecture Overview 

The system architecture follows a layered design composed of an edge layer dedicated to data acquisition, a cloud ingestion layer, a processing layer, and a storage and visualization layer. 

Telemetry data is collected from the PV inverter by an edge device and transmitted to the AWS cloud through a secure MQTT connection. Once ingested, an AWS IoT rule is used to route incoming telemetry messages to a serverless component responsible for data cleanup and transformation, while also acting as a decoupling layer between the ingestion pipeline and the specific inverter model and data format. The processed data is then stored in a time-series database and made available to users through a visualization dashboard and alert notifications. 

The following picture illustrates the high-level architecture of the system and the main data flow between the elements.

High-level architecture of the system.
Check out the full char here:
https://lucid.app/lucidchart/b4d95e6d-c69d-4dd8-a091-7daea9b741a3/edit?invitationId=inv_2c067017-d6be-4e8d-81aa-418cfdb05da7 

## Data Pipeline 

### Edge Layer 

The edge layer is responsible for acquiring live data from the PV inverter directly. 

### Local Data Collection 

Edge device (Raspberry Pi) acquires inverter data via wired Modbus connection 

A Mosquitto MQTT broker runs on the edge device 

Collected data is published locally as MQTT messages 

### Secure Cloud Entry Point 

The MQTT broker bridges messages to AWS IoT Core 

Communication occurs over MQTT over TLS 

Edge device authenticates to AWS IoT Core using a X.509 certificate 

## Cloud Ingestion Layer 

The cloud ingestion layer is responsible for securely receiving data from edge devices and routing messages downstream to the processing components. 

### AWS IoT Core 

Acts as the cloud entry point for MQTT messages transmitted by edge devices 

Provides a managed MQTT broker for device connectivity 

Handles secure communication and authentication via TLS and X.509 certificates 

### IoT Rule Engine 

Incoming messages are evaluated by an AWS IoT Rule 

The rule filters messages based on topic and triggers downstream processing 

## Processing Layer 

The processing layer is implemented using AWS Lambda, which provides decoupling from the specific PV inverter model and integrates the pipeline with the downstream storage and visualization services. 

### Serverless Data Processing 

An AWS Lambda function is triggered when a new telemetry message is received 

Messages are received from IoT Core as JSON payloads 

The payload is converted to InfluxDB Line Protocol, as required by the storage layer 

### Integration and Decoupling 

AWS IoT Core does not provide a native rule action for writing to a self-managed InfluxDB instance 

The Lambda function acts as an integration layer between the ingestion pipeline and the database backend 

This offers decoupling from vendor-specific inverter data formats, enabling support for multiple inverter models 

## Storage, Visualization, and Alerting Layer 

The storage and visualization layer is responsible for persisting telemetry data and providing users with tools to inspect and monitor the performance of their PV installation. 

### Data Storage 

Telemetry data is stored in InfluxDB, a time-series database optimized for high-frequency data 

InfluxDB runs on an Amazon EC2 instance deployed within the project’s Virtual Private Cloud (VPC) 

### Data Visualization 

Grafana is used to visualize telemetry data and build a dashboard for monitoring PV system performance and electrical billing costs 

Grafana queries InfluxDB to display time-series metrics such as energy production and system status 

### Anomaly Detection and Alerting 

Grafana evaluates alert rules on incoming telemetry data to detect common malfunction conditions (e.g., grid voltage outside safe range, inverter overheating, absence of energy production during daylight hours). 

When a condition is triggered, Grafana publishes a notification to Amazon SNS, which alerts the user via email or SMS. 

(As future work) the Lambda function could call a Machine Learning model deployed on Amazon SageMaker to detect subtle deviations from normal operating conditions before writing data to InfluxDB. 

### Prototype Deployment and Extension 

For the purposes of this prototype, InfluxDB and Grafana are hosted on the same EC2 instance 

This simplified deployment prevents autoscaling and high-availability configurations typical of a production-graded application 

In a production environment, the storage and visualization layer could be deployed across multiple availability zones to improve scalability and reliability 

## Project Status and Future Work 

The proposed architecture successfully demonstrates a prototype implementation of an end-to-end telemetry pipeline for domestic photovoltaic systems. The system integrates edge data acquisition, secure cloud ingestion, serverless processing, and time-series storage, while providing users with a dashboard for monitoring PV system performance and receiving basic malfunction alerts. 

The current prototype validates the feasibility of the selected technologies and establishes a flexible architecture that can be extended to support additional inverter models and advanced analytics. 
