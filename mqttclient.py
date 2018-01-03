import paho.mqtt.client as mqttw

class MqttClient :

    def __init__( self , address = "localhost", port = 1883 , id_ = "" ,  subscribe = ""  , message = None ) :
        self.address = address
        self.port = port
        self.subscribe = subscribe
        self.message = message

        self.client = mqttw.Client( client_id = id_ )
        self.client.connect( self.address , self.port )

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.loop_start()

    def on_connect( self , client , userdata , flags , rc ) :
        for subscribe in self.subscribe :
            self.client.subscribe( subscribe )

    def on_message( self , client , userdata , msg ) :
        if self.message is None :
            return

        self.message( client , userdata , msg )

    def publish( self , topic, payload=None, qos=0, retain=False ) :
        self.client.publish( topic  , payload , qos , retain )

