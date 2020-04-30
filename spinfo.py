import os 
import sys 
import subprocess 
import time

print("Cheking ..")
 
sys.stdout.write('\x1b[1A')
sys.stdout.write('\x1b[2K') 
# os.system("printf '\033c'")
# bench 
start = time.time() 

# function that process the size of bytes and return a size enotation
def size_notation(input_char):
	if input_char > 1000000 :
		input_char = input_char // 1000000
		size_char = ' MB'
	elif input_char > 1000 :
		input_char = input_char // 1024
		size_char = ' KB'
	else:
		size_char = ' B'
	return f'{input_char}'.rjust(10) + f'{size_char}'

# horizontal line to separate section


def line_separtator():
	print("━"*70)	
def header_banner() :
	banner = ""
	full_line = "━"*70
	banner += "\033[0m┏"
	banner += full_line
	banner += '┓'
	banner += "\n┃"
	menu  = '\u001b[33mLanguage'.rjust(15)+ 'Files'.rjust(15) + 'Lines'.rjust(15) + 'Size\u001b[0m'.rjust(22)
	banner += menu + '┃'.rjust(13)
	banner += '\n┗'
	banner += full_line + '┛'
	print(banner)

def draw_information(d):

	info_string = '┏' + "━"*70 + '┓\n'
	for i in d:
		info_string += '┃' + f' . {i}'.capitalize().ljust(22) + f'{dfile[i]}'.ljust(14) + f'{ d[i] if d[i] != 0 else "empty" }'.ljust(10) + f'{size_notation(dsize[i])}\u001b[0m'.ljust(28) +'┃' + '\n'
	info_string += '┗' + "━"*70 + '┛'
	print(info_string)

def footer_banner(content):

	banner = ""
	full_line = "━"*70
	banner += "\033[0m┏"
	banner += full_line
	banner += '┓'
	banner += "\n┃  "
	menu  = content
	banner += menu 
	banner +=  '┃'
	banner += '\n┗'
	banner += full_line + '┛'
	print(banner)

file_lines = 0
d = {}
dfile = {}
dsize = {}
dir_sum = 0 
file_sum = 0
commits = 0
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
	"h":"C/C++ Header",
	"ts":"TypeScript",
	"js":"JavaScript",
	"py":"Python",
	"cs":"C#",
	"rb":"ruby",
	"pl":"Perl",
	"rs":"Rust",
	"kt":"Kotlin",
	"kts":"Kotlin script",
	"clj":"Clojure",
	"go":"Go",
	"php":"PHP",
	"vim":"VimScript",
	"jl" : "Julia",
}

if len(sys.argv) < 2  :
	path = os.getcwd()
else:
	path = sys.argv[1]
	if not os.path.exists(path): 
		print('Sorry Path does not exist') 
		sys.exit(1)

# walk directory and subdirectroy walk
for dirpath , dirnames , filenames in os.walk(path):	
	if '.git' in dirpath:
		git_init = True
		continue

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

if git_init:
	commits = subprocess.check_output('git rev-list --count HEAD',shell=True)
	commits = commits.decode("utf-8")

# header 
print(f'Directories : \u001b[33m{dir_sum}\u001b[0m'.ljust(50),
	f'Files : \u001b[33m{file_sum}\u001b[0m',
	f'\nBinaries/Ignored:\u001b[33m {ignored_dirs} dir(s) , {ignored_files} file(s)\u001b[0m',
	f'\nGit : { f"(YES) (commits : {commits.strip()})" if git_init else "NO"}'
)	
	
# display 
header_banner() 
# total size 
total_size_notation = size_notation(sum(dsize.values()))

# display information
draw_information(d)

total_lines = sum(d.values())

# display the total
footer_banner(f'Total'.ljust(20) + 
	f'{sum(dfile.values())}'.ljust(14) + 
	f'{total_lines}'.ljust(10) + 
	f'{total_size_notation}'.ljust(24)
)

print(f"[DONE in { (time.time() - start):.2f} second(s)]")