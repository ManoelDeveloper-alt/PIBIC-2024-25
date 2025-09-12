class RobotControl:
	def __init__(self):
		# estabelece uma conexão com o stm32 solicitando ao arquivo "serialcommunication"
		pass
	def motor( self, vel1, vel2, vel3, vel4):
		# aplica as velocidade passadas nos motores
		pass

	def getVelocidade(self):
		# retorna um vetor com as velocidades das 4 rodas
		return []

	def getPos(self):
		# retorna um vetor com a posicao e orientacao
		return []

	def getUltrasonicSensor(self):
		# retorna uma matiz 2 colunas por 8 linhas
		# para cada linha - is_detected - valor
		return [ [], []]

	def getLineSensor(self):
		# retorna o valor dos sensores de linha
		return []

	def setLightBottom( self, valor):
		# mudar a intensidade da luz de chão
		pass
