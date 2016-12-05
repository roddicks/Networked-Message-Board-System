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
	chars = {
		'A': open('font/a.ppm', 'rb'),
		'B': open('font/b.ppm', 'rb'),
		'C': open('font/c.ppm', 'rb'),
		'D': open('font/d.ppm', 'rb'),
		'E': open('font/e.ppm', 'rb'),
		'F': open('font/f.ppm', 'rb'),
		'G': open('font/g.ppm', 'rb'),
		'H': open('font/h.ppm', 'rb'),
		'I': open('font/i.ppm', 'rb'),
		'J': open('font/j.ppm', 'rb'),
		'K': open('font/k.ppm', 'rb'),
		'L': open('font/l.ppm', 'rb'),
		'M': open('font/m.ppm', 'rb'),
		'N': open('font/n.ppm', 'rb'),
		'O': open('font/o.ppm', 'rb'),
		'P': open('font/p.ppm', 'rb'),
		'Q': open('font/q.ppm', 'rb'),
		'R': open('font/r.ppm', 'rb'),
		'S': open('font/s.ppm', 'rb'),
		'T': open('font/t.ppm', 'rb'),
		'U': open('font/u.ppm', 'rb'),
		'V': open('font/v.ppm', 'rb'),
		'W': open('font/w.ppm', 'rb'),
		'X': open('font/x.ppm', 'rb'),
		'Y': open('font/y.ppm', 'rb'),
		'Z': open('font/z.ppm', 'rb')
	}
	#Just retrieve the pixel definition bytes, no headers
	return chars.get(c).readlines()[3]
