#!/usr/bin/with-contenv bashio
set -e

mqtt_broker=$(bashio::config 'mqtt_broker')
mqtt_port=$(bashio::config 'mqtt_port')
mqtt_user=$(bashio::config 'mqtt_user')
mqtt_password=$(bashio::config 'mqtt_password')
mqtt_topic_prefix=$(bashio::config 'mqtt_topic_prefix')
mqtt_client_id=$(bashio::config 'mqtt_client_id')
modbus_host=$(bashio::config 'modbus_host')
modbus_port=$(bashio::config 'modbus_port')
regulator_address=$(bashio::config 'regulator_address')
interface_address=$(bashio::config 'interface_address')
regulator_type=$(bashio::config 'regulator_type')
timezone=$(bashio::config 'timezone')
time_sync=$(bashio::config 'time_sync')
period=$(bashio::config 'period')
enable_circuit_a=$(bashio::config 'enable_circuit_a')
enable_circuit_b=$(bashio::config 'enable_circuit_b')
discovery_enable=$(bashio::config 'discovery_enable')
discovery_prefix=$(bashio::config 'discovery_prefix')
serial_device=$(bashio::config 'serial_device')
solar_enabled=$(bashio::config 'solar_enabled')

export MQTT_BROKER_HOST="$mqtt_broker"
export MQTT_BROKER_PORT="$mqtt_port"
export MQTT_BROKER_USER="$mqtt_user"
export MQTT_BROKER_PASSWORD="$mqtt_password"
export MODBUS_HOST="$modbus_host"
export MODBUS_PORT="$modbus_port"
export SERIAL_DEVICE="$serial_device"
export SOLAR_ENABLED="$solar_enabled"

printf '%s\n' \
  '[Modbus]' \
  "ip: $modbus_host" \
  "port: $modbus_port" \
  "regulatorAddress:$regulator_address" \
  "interfaceAddress:$interface_address" \
  '' \
  '[MQTT]' \
  "brokerHost: $mqtt_broker" \
  "brokerPort: $mqtt_port" \
  "brokerLogin: $mqtt_user" \
  "brokerPassword: $mqtt_password" \
  "topicPrefix: $mqtt_topic_prefix" \
  "clientId: $mqtt_client_id" \
  '' \
  '[Boiler]' \
  "regulatorType: $regulator_type" \
  "timezone: $timezone" \
  "timeSync: $time_sync" \
  "period: $period" \
  "enable_circuit_A: $enable_circuit_a" \
  "enable_circuit_B: $enable_circuit_b" \
  '' \
  '[Home Assistant]' \
  "MQTT_DiscoveryEnable: $discovery_enable" \
  "discovery_prefix: $discovery_prefix" \
  > /app/conf/Diematic32MQTT.conf

cd /app
exec python3 /app/Diematic32MQTT.py
