if __name__=='__main__':
	import torch
	from dataloader import prepare_dataset
	from model import AnticipationModel
	from options import parser
	import os

	opts = parser.parse_args()
	print("ss",opts)
	print("asda",opts.test_folder)
	if not os.path.exists(opts.test_folder):
		os.mkdir(opts.test_folder)

	model_file = os.path.join(opts.model_folder, 'model{:3d}.pkl'.format(opts.model_epoch))

	_, test_set = prepare_dataset(opts)
	model = AnticipationModel(opts,train=False,pretrain=model_file)

	with torch.no_grad():

		model.net.eval()
		model.net.set_mode('DETERMINISTIC')
		print(test_set)
		for ID,op in test_set:
			print(op)

			samples = model.sample_op_predictions(op,opts.num_samples)
			print(samples)
			model.save_samples(samples,ID=ID,epoch=opts.model_epoch,result_folder=opts.test_folder)
			print('saved samples for OP #' + ID)