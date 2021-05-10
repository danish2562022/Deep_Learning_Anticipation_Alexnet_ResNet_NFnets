# Uncertainty-aware Anticipation of Sparse Surgical Instrument Usage

PyTorch implementation of uncertainty-aware anticipation of sparse surgical instrument usage.
We define the novel task of anticipating the usage of instruments in surgical videos. We propose a Bayesian CNN-LSTM network and evaluate its ability to quantify uncertainties relevant to the task. Details can be found in our [paper](https://arxiv.org/pdf/2007.00548.pdf).

## Code

### Requirements

Check if you have all required Python packages installed. Our code depends on
> torch torchvision numpy scipy matplotlib

Experiments were run using Python 3.8, [PyTorch 1.6.0](https://pytorch.org), Cuda 10.2 and Torchvision 0.7.0. The code was also tested for PyTorch 1.5.0 and Torchvision 0.6.0.

### Data preparation

Experiments were performed on the [Cholec80 dataset](https://arxiv.org/pdf/1602.03012.pdf) containing 80 complete videos of cholcystectomies. Access to the dataset can be requested [here](http://camma.u-strasbg.fr/datasets).

Assume the Cholec80 dataset was downloaded to `<DOWNLOAD_DIR>`. Copy the frame extraction script `frame_extractor_cholec80.py` into `/<DOWNLOAD_DIR>/cholec80/videos/` and run the script here. This should create 4 folders `1/`, `2/`, `3/` and `4/` containing the frames of 20 operations each. For our experiments we used fold `4/` for testing and the rest for training.

Finally, move frame folders `1/`, `2/`, `3/` and `4/` into `data/images/` of this repository and move the annotation folder `tool_annotations/` into `data/annotations/`. The structure of the `data/` directory should now look as follows:

```
<REPO>
	data
		images
			1                                   # fold number 1
				02                              	# operation number 02
					00000000.png
					00000001.png
					00000002.png
					...
				04                              	# operation number 04
					00000000.png
					00000001.png
					00000002.png
					...
				...
			2                                   # fold number 2
				...
			3                                   # fold number 3
				...
			4                                   # fold number 4
				...
		annotations
			tool_annotations
				video01-tool.txt
				video02-tool.txt
				...
				video80-tool.txt
```

### Training

To train a model, use the following command:

```bash
cd train_test_scripts
python3 train.py --horizon <HORIZON> --output_folder <OUTPUT_FOLDER>
```

The parameter `<HORIZON>` refers to the number of minutes instruments should be anticipated before appearance. Learned weights, sampled predictions and training stats are written to `output/experiments/` by default. Please check default parameter settings in `train_test_scripts/options.py`.

### Testing

To sample predictions from a trained probailistic model on the test fold `4/`, use:

```bash
cd train_test_scripts
python3 test.py --horizon <HORIZON> --num_samples <NUM_SAMPLES> --model_folder <MODEL_DIR> --model_epoch <EPOCH>
```

The number of samples `<NUM_SAMPLES>` to be drawn from the approximate posterior as well as the horizon `<HORIZON>` on which the model was trained on have to be specified. `<MODEL_DIR>` refers to the directory in which the desired model file is located and `<EPOCH>` specifies from which epoch to load wieghts. Model files generated by the training script `train.py` have the form `model<EPOCH>.pkl`. By default, the sampled predictions are written to `outputs/test/` as numpy arrays (`.npy`).

### Evaluation

The following commands reproduce the graphs presented in the paper. These scripts require that prediction samples have already been saved as `.npy` files by either the `train.py` or `test.py` script. Alternatively, pretrained models containing weights and sampled test predictions for horizons of 3 and 5 min. can be downloaded [here](https://caruscloud.uniklinikum-dresden.de/index.php/s/FfrzHiAFseNw5tm).

In the following, `<SAMPLE_PATH>` refers to the directory in which prediction samples are located and `<EPOCH>` specifies from which epoch to load predictions.

To print test scores according to the metrics `wMAE` and `pMAE` from the paper (like Table 1 & 2 in the paper), use:

```bash
cd evaluation_scripts
python3 test_scores.py --horizon <HORIZON> --sample_path <SAMPLE_PATH> --epoch <EPOCH> 
```

To view predictions and uncertainty estimates on test operations (like Suppl. Fig. 3 in the paper), use:

```bash
cd evaluation_scripts
python3 plot_test_samples.py --horizon <HORIZON> --sample_path <SAMPLE_PATH> --epoch <EPOCH> --uncertainty_type <UNCERT>
```

`<UNCERT>` specifies which uncertainty measure to use and can be "epistemic_reg", "epistemic_cls", "aleatoric_cls" or "entropy_cls".

To view plots related to uncertainty analysis in the regression case (like Fig. 2 & 3 in the paper), use:

```bash
cd evaluation_scripts
python3 plot_uncertainties_reg.py --horizon <HORIZON> --sample_path <SAMPLE_PATH> --epoch <EPOCH>
```

To view plots related to uncertainty analysis in the classification case (like Fig. 2 & 3 in the paper), use:

```bash
cd evaluation_scripts
python3 plot_uncertainties_cls.py --horizon <HORIZON> --sample_path <SAMPLE_PATH> --epoch <EPOCH> --uncertainty_type <UNCERT_CLS>
```

`<UNCERT_CLS>` specifies which uncertainty measure to use and can be "epistemic_cls", "aleatoric_cls" or "entropy_cls".

### Baselines

To reproduce the results of the histogram baselines `MeanHist` and `OracleHist`, run:

```bash
cd baselines
python3 histogram_baselines.py --horizon <HORIZON> --baseline <BASELINE_TYPE> --mode <MODE>
```

where `<BASELINE_TYPE>` can be "oracle" or "mean" and `<MODE>` can be "train" or "test". In training mode, the best threshold on the training set is determined for each instrument. Then the wMAE and pMAE scores on the test set are computed. This can take several minutes. In test mode, the previously learned thresholds (which are hard-coded in the script) are directly used to compute the test scores.

## How to cite

The paper has been published at the 23rd International Conference on Medical Image Computing and Computer-Assisted Interventions ([MICCAI 2020](http://miccai2020.org/)).

```
@inproceedings{rivoir2020rethinking,
  title={Rethinking Anticipation Tasks: Uncertainty-Aware Anticipation of Sparse Surgical Instrument Usage for Context-Aware Assistance},
  author={Rivoir, Dominik and Bodenstedt, Sebastian and Funke, Isabel and von Bechtolsheim, Felix and Distler, Marius and Weitz, J{\"u}rgen and Speidel, Stefanie},
  booktitle={International Conference on Medical Image Computing and Computer-Assisted Intervention},
  pages={752--762},
  year={2020},
  organization={Springer}
}
```

This work was carried out at the National Center for Tumor Diseases (NCT) Dresden, [Department of Translational Surgical Oncology](https://www.nct-dresden.de/tso.html).