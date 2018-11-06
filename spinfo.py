import os 
import sys 

def sep():
	print('\u001b[33;1m-\u001b[0m'*70)

file_lines = 0
d = {}
dfile = {}
dsize = {}
dir_sum = 0 
file_sum = 0
ignored_dirs = 0 
ignored_files = 0 
git_init = False

# extension dictionary
lang_dic = {
	"md" : "Markdown",
	"sh" : "Shell script",
	"hs" : "Haskell",
	"cpp" : "C++",
	"cc": "C++",
	"ts":"TypeScript",
	"js":"JavaScript",
	"py":"Python",
	"cs":"C#",
	"rb":"ruby",
	"pl":"Perl",
	"rs":"Rust",
	"kt":"Kotlin",
	"kts":"Kotlin script",
	"clj":"Clojure"
}

if len(sys.argv) < 2  :
	path = os.getcwd()
else:
	path = sys.argv[1]
	if(os.path.exists(path)):
		pass 
	else:
		print('Sorry Path does not exist') 
		sys.exit(1)

# walk directory and subdirectroy walk
for dirpath , dirnames , filenames in os.walk(path):	

	for directory in dirnames:
		if directory == '.git':
			git_init = True
		if not directory.startswith('.'):
			dir_sum += 1
		else:
			ignored_dirs+=1 
	for file in filenames:
		if not file.startswith('.'):
			file_sum+=1
		else:
			ignored_files+=1  

	for file in filenames:
		fullpath = os.path.join(dirpath,file)
		try:
			if file.endswith('pyc') or file == '.DStore' or file.startswith('.'):
				pass
			else:
				try:
					ex = file.split('.')[1]
				except IndexError:
					pass 
				if ex in lang_dic.keys():
					ex = lang_dic[ex].capitalize() 

				if ex in d.keys():
					d[ex]+= sum(1 for line in open(fullpath))
					dsize[ex]+= os.path.getsize(fullpath)
					dfile[ex] += 1
				else:
					d[ex] = sum(1 for line in open(fullpath))
					dsize[ex] = os.path.getsize(fullpath)
					dfile[ex] = 1 
		except Exception:
			pass		
print(f'Directories : \u001b[33m{dir_sum}\u001b[0m'.ljust(50),
	f'Files : \u001b[33m{file_sum}\u001b[0m',
	f'\nBinaries/Ignored:\u001b[33m {ignored_dirs} dir(s) , {ignored_files} file(s)\u001b[0m',
	f'\nGit : { "(YES)" if git_init else "NO "}'
)	
	

# display 
sep()
print('\u001b[33;1mLanguage'.ljust(27),
	'Files'.ljust(20),
	'Lines'.ljust(20),
	'Size\u001b[0m'.ljust(20))
sep()
total_size = sum(dsize.values()) // 1024
total_size = str(total_size) + 'KB' 
for i in d:
	if (dsize[i] / 1024 ) > 1:
		dsize[i] = dsize[i] // 1024
		b = 'KB'
	elif (dsize[i] / (1024*1024)) > 1 :
		dsize[i] = dsize[i] // (1024*1024)
		b = 'MB'
	else:
		b = 'B'

	print(f'{i}'.ljust(20),
		f'{dfile[i]}'.ljust(20),
		f'{ d[i] if d[i] != 0 else "empty" }'.ljust(20),
		f'{dsize[i]} {b}\u001b[0m'.ljust(20)) 

total_lines = sum(d.values())
sep()

print(f'Total'.ljust(20),
	f'{sum(dfile.values())}'.ljust(20),
	f'{total_lines}'.ljust(20),
	f'{total_size}'.ljust(20))
sep()