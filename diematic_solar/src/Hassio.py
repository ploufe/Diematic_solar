#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging,json

#This class allow to interface with Home Assistant through the MQTT Discovery Protocol
class Hassio:

	def __init__(self,mqttClient,topicRoot,clientId,discovery_prefix,availability_enabled=True):
		
		#logger
		self.logger = logging.getLogger(__name__);
		#attribute init
		self.availabilityTopic=None;
		#mqttClient instance ref saving
		self.mqtt=mqttClient;
		self.topicRoot=topicRoot;
		self.clientId=clientId;
		self.discovery_prefix=discovery_prefix;
		self.availability_enabled=availability_enabled;
		self.device = {
			"identifiers": [""],
			"manufacturer": "",
			"name": ""
		}
		
	def setDevice(self,manufacturer,name,id):
		self.device = {
			"identifiers": id,
			"manufacturer": manufacturer,
			"name": name
		}
	
	def availabilityInfo(self,shortTopic,payload_available,payload_not_available):
		#availability info saving
		
		if self.availability_enabled:
			self.availabilityTopic=self.topicRoot+'/'+shortTopic;
			self.payload_available=payload_available;
			self.payload_not_available=payload_not_available;

	def addAvailability(self,payload):
		if self.availability_enabled:
			payload["availability_topic"]=self.availabilityTopic;
			payload["payload_available"]=self.payload_available;
			payload["payload_not_available"]=self.payload_not_available;

	def removeEntity(self,component,object_id):
		discoveryTopic=self.discovery_prefix+'/'+component+'/'+self.clientId+'/'+object_id+'/config';
		self.mqtt.publish(discoveryTopic,'',1,True);
	
	def addSensor(self,object_id,name,deviceClass,shortStateTopic,valueTemplate,unit_of_measurement):
		#build discovery topic
		discoveryTopic=self.discovery_prefix+'/sensor/'+self.clientId+'/'+object_id+'/config';
		#build discovery message payload
		payload={"name":name};
		payload["default_entity_id"]='sensor.'+object_id;
		payload["unique_id"]=self.clientId+'.'+object_id;
		if (deviceClass is not None):
			payload["device_class"]=deviceClass;
		payload["state_topic"]=self.topicRoot+'/'+shortStateTopic;
		if (valueTemplate is not None):
			payload["value_template"]=valueTemplate;
		self.addAvailability(payload);
		if (unit_of_measurement is not None):
			payload["unit_of_measurement"]=unit_of_measurement;
		payload['device'] = self.device
		#send discovery message
		self.mqtt.publish(discoveryTopic,json.dumps(payload),1,False);

	def addBinarySensor(self,object_id,name,deviceClass,shortStateTopic,payload_on,payload_off):
		#build discovery topic
		discoveryTopic=self.discovery_prefix+'/binary_sensor/'+self.clientId+'/'+object_id+'/config';
		#build discovery message payload
		payload={"name":name};
		payload["default_entity_id"]='binary_sensor.'+object_id;
		payload["unique_id"]=self.clientId+'.'+object_id;
		if (deviceClass is not None):
			payload["device_class"]=deviceClass;
		payload["state_topic"]=self.topicRoot+'/'+shortStateTopic;
		payload["payload_on"]=payload_on;
		payload["payload_off"]=payload_off;
		self.addAvailability(payload);
		payload["enabled_by_default"]=False;
		payload['device'] = self.device
		#send discovery message
		self.mqtt.publish(discoveryTopic,json.dumps(payload),1,False);
	
	def addNumber(self,object_id,name,shortStateTopic,shortCommandTopic,min,max,step,unit_of_measurement):
		#build discovery topic
		discoveryTopic=self.discovery_prefix+'/number/'+self.clientId+'/'+object_id+'/config';
		#build discovery message payload
		payload={"name":name};
		payload["default_entity_id"]='number.'+object_id;
		payload["unique_id"]=self.clientId+'.'+object_id;
		payload["state_topic"]=self.topicRoot+'/'+shortStateTopic;
		payload["command_topic"]=self.topicRoot+'/'+shortCommandTopic;
		self.addAvailability(payload);
		payload["qos"]=2;
		payload["min"]=min;
		payload["max"]=max;
		payload["step"]=step;
		if (unit_of_measurement is not None):
			payload["unit_of_measurement"]=unit_of_measurement;
		payload['device'] = self.device
		#send discovery message
		self.mqtt.publish(discoveryTopic,json.dumps(payload),1,False);
		
	def addSelect(self,object_id,name,shortStateTopic,shortCommandTopic,options):
		#build discovery topic
		discoveryTopic=self.discovery_prefix+'/select/'+self.clientId+'/'+object_id+'/config';
		#build discovery message payload
		payload={"name":name};
		payload["default_entity_id"]='select.'+object_id;
		payload["unique_id"]=self.clientId+'.'+object_id;
		payload["state_topic"]=self.topicRoot+'/'+shortStateTopic;
		payload["command_topic"]=self.topicRoot+'/'+shortCommandTopic;
		self.addAvailability(payload);
		payload["qos"]=2;
		payload["options"]=options;
		payload['device'] = self.device
		#send discovery message
		self.mqtt.publish(discoveryTopic,json.dumps(payload),1,False);	

	def addSwitch(self,object_id,name,shortStateTopic,shortCommandTopic,payload_off,payload_on):
		#build discovery topic
		discoveryTopic=self.discovery_prefix+'/switch/'+self.clientId+'/'+object_id+'/config';
		#build discovery message payload
		payload={"name":name};
		payload["default_entity_id"]='switch.'+object_id;
		payload["unique_id"]=self.clientId+'.'+object_id;
		if (shortStateTopic is not None):
			payload["state_topic"]=self.topicRoot+'/'+shortStateTopic;
		payload["command_topic"]=self.topicRoot+'/'+shortCommandTopic;
		self.addAvailability(payload);
		payload["payload_off"]=payload_off;
		payload["payload_on"]=payload_on;		
		payload["qos"]=2;
		payload['device'] = self.device
		#send discovery message
		self.mqtt.publish(discoveryTopic,json.dumps(payload),1,False);		

