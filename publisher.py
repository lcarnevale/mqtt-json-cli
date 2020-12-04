# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""MQTT Publisher Script

.. _Google Python Style Guide
    https://github.com/google/styleguide/blob/gh-pages/pyguide.md
"""

__copyright__ = 'Copyright 2019-2020, Lorenzo Carnevale'
__author__ = 'Lorenzo Carnevale <lorenzocarnevale@gmail.com>'
__credits__ = ''
__description__ = 'MQTT Publisher Script'

# standard libraries
import time
import socket
import argparse
# third parties libraries
import paho.mqtt.client as mqtt


def main():
	description = ('%s\n%s' % (__author__, __description__))
	epilog = ('%s\n%s' % (__credits__, __copyright__))
	parser = argparse.ArgumentParser(
		description = description,
		epilog = epilog
	)

	parser.add_argument('-H', '--host',
						dest='host',
                        help='Define the hostname',
                        type=str,
						required=True)

	parser.add_argument('-p', '--port',
						dest='port',
                        help='Define the port',
                        type=int, default=1883)

	parser.add_argument('-u', '--username',
						dest='username',
                        help='Define the username',
                        type=str, default='admin')

	parser.add_argument('-P', '--password',
						dest='password',
                        help='Define the password',
                        type=str, default='admin')

	parser.add_argument('-d', '--data',
						dest='data',
                        help='Define data',
                        type=str, default='{"example": "This is an example"}')

	parser.add_argument('-t', '--topic',
						dest='topic',
                        help='Define the topic',
                        type=str,
						required=True)

	options = parser.parse_args()

	# initializing metadata
	mqtt.Client.connected_flag = False
	client_name = '%s-pub' % (socket.gethostname())

	# implementing callbacks
	def on_connect(client, _, __, rc):
		"""Connection's callback

		The callback for when the client receives a CONNACK response from the server.
		It subscribes to all the topics specified in the topics list.
		Moreover, subscribing in on_connect() means that if we lose the connection
		and reconnect then subscriptions will be renewed.

		Connection Return Codes:
			0: Connection successful
			1: Connection refused – incorrect protocol version
			2: Connection refused – invalid client identifier
			3: Connection refused – server unavailable
			4: Connection refused – bad username or password
			5: Connection refused – not authorised
			6-255: Currently unused.

		Args:
			client(obj:'paho.mqtt.client.Client'): the client instance for this callback;
			rc(int): is used for checking that the connection was established.
		"""
		return_code = {
	        0: "Connection successful",
	        1: "Connection refused – incorrect protocol version",
	        2: "Connection refused – invalid client identifier",
	        3: "Connection refused – server unavailable",
	        4: "Connection refused – bad username or password",
	        5: "Connection refused – not authorised",
	    }
		print(return_code.get(rc, "Currently unused."))
		client.connected_flag = True

	def on_disconnect(client, _, rc):
		"""
		Args:
			client(obj:'paho.mqtt.client.Client'): the client instance for this callback;
			rc(int): is used for checking that the disconnection was done.
		"""
		print('Disconnection successful %s' % (rc))

	def on_publish(client, _, result):
		"""Publish's callback

		The callback for when a PUBLISH message is sent to the server

		Args:
			client(obj:'paho.mqtt.client.Client'): the client instance for this callback;
			result():.
		"""
		print('Data published')

	# defining the client and callbacks
	client = mqtt.Client(client_name)
	client.on_connect = on_connect
	client.on_disconnect = on_disconnect
	client.on_publish = on_publish

	# authenticating and connecting to the broker
	client.loop_start()
	client.username_pw_set(username=options.username,password=options.password)
	client.connect(options.host, options.port)

	print("Wait for connection ...")
	while not client.connected_flag:
	    time.sleep(1)

	# publishing a message
	client.publish(
		options.topic,
		options.data
	)

	# disconneting the client
	client.loop_stop()    #Stop loop
	client.disconnect()

if __name__ == '__main__':
	main()
