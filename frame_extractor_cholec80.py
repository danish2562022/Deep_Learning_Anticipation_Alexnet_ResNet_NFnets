import os.path

def extractor(video, folderNumber):
	videoNumber = video[5:7]
	# print(os.getcwd())
	path=os.path.join('C:/Users/Public/Dataset_Cholec/ins_ant-master', str(folderNumber))
	# print(path)
	os.chdir(path)
	print(os.getcwd())
	os.system('mkdir ' + videoNumber)
	os.chdir('..')
	print(os.getcwd())
	path='Cholec80/videos'

	# -r 1 extracts one frame every second. First frame of every video is 00000000.png
	os.chdir(path)
	path=path+'/' + str(video)
	print(os.getcwd())
	path_output='C:/Users/Public/Dataset_Cholec/ins_ant-master/'
	os.system('ffmpeg -hide_banner -i ' + video + ' -r 1 ' + '-start_number 0 '+path_output + folderNumber + '/' + videoNumber + '/%08d.png')

# execute script in <...>/cholec80/videos
os.system('mkdir 1 | mkdir 2 | mkdir 3 | mkdir 4')
os.chdir("C:/Users/Public/Dataset_Cholec/ins_ant-master/Cholec80/videos")
print("Current Working Directory " , os.getcwd())
print(os.listdir())
video_files = sorted([f for f in os.listdir() if '.mp4' in f])
print(video_files)
for file in video_files:

	videoNumber = file[5:7]
	print(videoNumber)
	
	if videoNumber in ['02','04','06','12','24','29','34','37','38','39','44','58','60','61','64','66','75','78','79','80']:
		extractor(file, '1')
	if videoNumber in ['01','03','05','09','13','16','18','21','22','25','31','36','45','46','48','50','62','71','72','73']:
		extractor(file, '2')
	if videoNumber in ['10','15','17','20','32','41','42','43','47','49','51','52','53','55','56','69','70','74','76','77']:
		extractor(file, '3')
	if videoNumber in ['07','08','11','14','19','23','26','27','28','30','33','35','40','54','57','59','63','65','67','68']:
		extractor(file, '4')