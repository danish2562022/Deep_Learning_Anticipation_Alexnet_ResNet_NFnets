import os.path

def extractor(video, folderNumber):
	videoNumber = video[5:7]
	os.chdir('./' + folderNumber) 
	os.system('mkdir ' + videoNumber)
	os.chdir('..') 
	# -r 1 extracts one frame every second. First frame of every video is 00000000.png
	os.system('ffmpeg -hide_banner -i ' + video + ' -r 1 ' + '-start_number 0 ./' + folderNumber + '/' + videoNumber + '/%08d.png')

# execute script in <...>/cholec80/videos
os.system('mkdir 1 | mkdir 2 | mkdir 3 | mkdir 4')
video_files = sorted([f for f in os.listdir() if '.mp4' in f])

for file in video_files:

	videoNumber = file[5:7]
	
	if videoNumber in ['02','04','06','12','24','29','34','37','38','39','44','58','60','61','64','66','75','78','79','80']:
		extractor(file, '1')
	if videoNumber in ['01','03','05','09','13','16','18','21','22','25','31','36','45','46','48','50','62','71','72','73']:
		extractor(file, '2')
	if videoNumber in ['10','15','17','20','32','41','42','43','47','49','51','52','53','55','56','69','70','74','76','77']:
		extractor(file, '3')
	if videoNumber in ['07','08','11','14','19','23','26','27','28','30','33','35','40','54','57','59','63','65','67','68']:
		extractor(file, '4')