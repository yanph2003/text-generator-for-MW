import re
 
file_template = open(file="_template_.txt",mode="r",encoding="utf-8")
template_text = file_template.read()
file_template.close()
tmp = template_text.split("###")
top_extra = tmp[0]
repeat_count = int(tmp[1])
template_text = tmp[2]
bottom_extra = tmp[3]
_replacement = template_text.split("@")
_replacement = [_replacement[x] for x in range(1,len(_replacement),2)]
replacement=[]
for i in range(len(_replacement)):
	if _replacement[i] not in _replacement[:i] : 
		replacement.append(_replacement[i])
text_array = [template_text for i in range(repeat_count)]

nico_flag = False
for x in replacement : 
	if x[:6] == "_NICO_" :
		nico_flag = True
		break 
if nico_flag : 
	html_file = open(file="_nico_source_.txt",mode="r",encoding="utf-8")
	line = html_file.read().split("v>")
	sm = []
	title = []
	leng = []
	date = []
	img = []
	for x in line :
		res = re.search(r'background-image: url\(&quot;https://nicovideo.cdn.nimg.jp/thumbnails/(.*)&quot;\);',x,re.M)
		if res :
			tmp = res.group(1)
			if tmp[-1] == 'M':
				tmp = tmp[:-1]+'L'
			img += ['https://nicovideo.cdn.nimg.jp/thumbnails/'+tmp]
		res = re.search(r'<h2 class="NC-MediaObjectTitle NC-VideoMediaObject-title NC-MediaObjectTitle_fixed2Line">(.*)</h2>',x,re.M)
		if res :
			title += [res.group(1)]
		res = re.search(r'<div class="NC-VideoLength">(.*)</d',x,re.M)
		if res :
			leng += [res.group(1)]
		res = re.search(r'<span class="NC-VideoRegisteredAtText-text">(.*)</span></span>',x,re.M)
		if res :
			date += [res.group(1)]
		res = re.search(r'<a href="https://www.nicovideo.jp/watch/([a-zA-Z0-9]*).*" class="NC-Link NC-MediaObject-contents" rel="noopener">',x,re.M)
		if res :
			sm += [res.group(1)]
	html_file.close()


if len(sm) != repeat_count or len(title) != repeat_count or len(date) != repeat_count or len(leng) != repeat_count or len(img) != repeat_count :
	print("[WARNING] Unmatched _nico_source_ and repeat_count!")
		
for marker in replacement :
	if marker[:6] != "_NICO_" :
		file_tmp = open(file=marker+".txt",mode="r",encoding="utf-8")
		dict_tmp = file_tmp.read().split("\n")
		file_tmp.close()
		for i in range(repeat_count) :
			text_array[i] = text_array[i].replace("@"+marker+"@",dict_tmp[i if i<len(dict_tmp) else -1])
	else :
		if marker[:9] == "_NICO_SM_" :
			for i in range(repeat_count) :
				text_array[i] = text_array[i].replace("@"+marker+"@",sm[i if i<len(sm) else -1])
		elif marker[:12] == "_NICO_TITLE_" :
			for i in range(repeat_count) :
				text_array[i] = text_array[i].replace("@"+marker+"@",title[i if i<len(title) else -1])
		elif marker[:13] == "_NICO_LENGTH_" :
			for i in range(repeat_count) :
				tmp = leng[i if i<len(leng) else -1]
				if "CHN" in marker.split("_") or "C" in marker.split("_") : 
					tmp = tmp.split(":")
					if len(tmp) == 2:
						if tmp[0] != "0" :
							tmp = tmp[0]+"分"+tmp[1]+"秒"
						else :
							tmp = tmp[1]+"秒"
					elif len(tmp) == 3:
						tmp = tmp[0]+"小时"+tmp[1]+"分"+tmp[2]+"秒"
				text_array[i] = text_array[i].replace("@"+marker+"@",tmp)
		elif marker[:11] == "_NICO_DATE_" :
			for i in range(repeat_count) :
				tmp = date[i if i<len(date) else -1].split(" ")
				tmp[1] = " "+tmp[1] 
				if "CHN" in marker.split("_") or "C" in marker.split("_") : 
					ymd = tmp[0].split("/")
					tmp[0] = ymd[0]+"年"+ymd[1]+"月"+ymd[2]+"日"
					hm = tmp[1].split(":")
					tmp[1] = hm[0]+"时"+hm[1]+"分"
				if "MIN" in marker.split("_") or "M" in marker.split("_") :
						text_array[i] = text_array[i].replace("@"+marker+"@",tmp[0]+tmp[1])
				else :
						text_array[i] = text_array[i].replace("@"+marker+"@",tmp[0])	

		elif marker[:12] == "_NICO_IMAGE_" or marker[:10] == "_NICO_IMG_" :
			for i in range(repeat_count) :
				text_array[i] = text_array[i].replace("@"+marker+"@",img[i if i<len(img) else -1])
		else : 
			pass


result_file = open(file="result.txt",mode="w",encoding="utf-8")
final_text = top_extra
for x in text_array :
	final_text += x
final_text += bottom_extra
result_file.write(final_text)
result_file.close()

