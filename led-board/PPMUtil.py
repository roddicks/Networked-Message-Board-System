import string

def text_to_ppm(filename, text):
	text = text.upper()
	chars = []
	for c in text:
		chars.append(ppm_char_dict(c))
	
	#Write characters
	file = open(filename, 'w+b')
	write_ppm(file, chars)
	file.close()
	
	#Insert header at top
	file = open(filename, 'r')
	contents = file.readlines()
	file.close()
	contents.insert(0, 'P6\n')
	#9 columns per character plus one for space between characters
	contents.insert(1, str((len(text)*9) + len(text)) + ' 16\n')
	contents.insert(2, '255\n')
	
	file = open(filename, 'wb')
	file.writelines(contents)
	file.close()
	
def write_ppm(file, bytes):
	for i in range(1, 17):
		for bs in bytes:
			file.write(bs[9*3*i-9*3:9*3*i])
			file.write(b'\xFF\xFF\xFF')	#single space between letters
	
def ppm_char_dict(c):
	if c.isspace():
		result = open('font/space.ppm', 'rb')
	else:
		result = open('font/' + c + '.ppm', 'rb')
	#Just retrieve the pixel definition bytes, no headers
	return result.readlines()[3]
