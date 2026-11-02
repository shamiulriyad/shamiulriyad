# Glossary (Artifact 10)

| Term | Definition |
| --- | --- |
| Ablation study | An experiment that removes one component to measure how much that component contributes. |
| Affine transform | A geometric mapping that combines rotation, scaling, shear and translation; straight lines stay straight. |
| Anomaly | Anything that differs from the learned notion of 'normal'. Not every anomaly is a defect (it may be noise or a harmless variation). |
| Anomaly detection | Finding samples or regions that do not look like normal data, usually trained with normal data only. |
| Anomaly map | An image in which each pixel's value is that location's anomaly score; also called a heatmap. |
| Anomaly score | A number that says how abnormal a sample (image score) or location (pixel score) is. Higher means more suspicious. |
| AUPRC | Area under the precision–recall curve. More informative than AUROC when defects are rare. |
| AUPRO / PRO | Per-region overlap: a localisation metric that gives every defect region equal weight, regardless of its size, integrated up to a false-positive rate of 30%. |
| AUROC | Area under the ROC curve: the probability that a random anomalous sample gets a higher score than a random normal one. 0.5 = chance, 1.0 = perfect. |
| Backbone / encoder | The pretrained neural network that converts an image into feature maps. |
| Bounding box | A rectangle around a defect, given by its position, width and height. |
| Calibration | Making scores behave like probabilities, so a 'confidence of 0.9' is correct about 90% of the time. |
| Catastrophic forgetting | When a model updated on new data loses performance on what it had learned before. |
| Continual learning | Learning from a stream of new data or tasks over time without forgetting earlier knowledge. |
| Coreset subsampling | Selecting a small, representative subset of memory features that covers the whole feature space. |
| Cross-die inspection | Inspecting dies that were not used as references, with references enrolled from other dies. |
| Cross-type inspection | Inspecting a different die design (product) from the one the references came from. |
| Cross-wafer inspection | Inspecting dies from a wafer different from the reference wafer. |
| Defect | A physical imperfection on the die (particle, scratch, bridge, open, residue, ...) that may affect yield or reliability. |
| Defect preservation ratio (DPR) | Proposed in this dossier: anomaly score of an injected defect after a processing step divided by its score without that step. Values below 1 mean the step weakens the defect. |
| Defect localisation | Saying where a defect is: a heatmap, box or pixel mask. |
| Die | One rectangular chip on a wafer; after dicing it becomes an individual integrated circuit. |
| Die-to-die inspection | Classical method that compares a die with neighbouring dies of the same design; differences are defect candidates. |
| Dice / IoU | Overlap measures between predicted and true masks. IoU = intersection/union; Dice = 2·intersection/(sum of areas). |
| DINOv2 | A self-supervised Vision Transformer whose patch features transfer well to many tasks without fine-tuning. |
| Domain shift | Change in data distribution between training and use, such as a different tool, layer, product or illumination. |
| ECC alignment | Enhanced Correlation Coefficient: an iterative, brightness-insensitive method for refining an image alignment. |
| Enrolment | Adding the features of reference dies to the memory. No network weights change. |
| Feature map | A grid of feature vectors, one per image location, produced by the encoder. |
| Feature vector | A list of numbers that describes a patch or an image in a way that makes similar things close together. |
| Few-shot learning | Learning or adapting from a handful (for example 1–10) of examples. |
| Fourier–Mellin registration | Estimating rotation and scale with Fourier transforms and log-polar resampling, followed by translation. |
| Ground truth | The reference annotation (label, box or mask) used to evaluate predictions. |
| Human-in-the-loop | A workflow in which people verify or correct the model's outputs and their decisions are fed back to the system. |
| Illumination correction | Removing slow brightness variations caused by the imaging system, not by the sample. |
| Image registration | Finding the geometric transform that maps one image onto another so that corresponding structures overlap. |
| Inference | Using a trained or enrolled model on new data. |
| k-nearest neighbours (kNN) | Finding the k stored items closest to a query; the distance to them is used as a score. |
| Known-defect memory | A small store of features or prototypes of verified, named defect classes. |
| Leakage | When information from the test set influences training or tuning, inflating results. |
| Mahalanobis distance | A distance that accounts for the spread and correlation of the normal data. |
| Memory bank / reference memory | The stored set of normal (and optionally defect) features that new dies are compared with. |
| Novelty gate | A rule that only admits new memory items if they are sufficiently different from what is already stored. |
| Open-set recognition | Classification that can answer 'none of the known classes' instead of forcing a known label. |
| Optical inspection | Wafer inspection with light microscopy; fast, but with lower resolution than SEM. |
| Patch | A small square region of an image (or one cell of a feature map). |
| Pixel-level mask | A binary image in which defect pixels are 1 and normal pixels are 0. |
| Precision / Recall / F1 | Precision = share of alarms that are real defects; recall = share of real defects found; F1 = their harmonic mean. |
| Prototype | The average feature of a class; used for nearest-prototype classification. |
| Prototypical network | A few-shot classifier that compares a query with class prototypes. |
| Quarantine buffer | Temporary store for feedback-derived memory items that are not used until verified. |
| Reference die | A die image accepted as normal and used for comparison. |
| Rotation robustness | Giving the same correct decision whatever the die's orientation. |
| SEM | Scanning Electron Microscope: images surfaces at nanometre resolution with an electron beam; used for defect review. |
| Siamese network | Two weight-sharing networks that embed two inputs so that their similarity can be compared. |
| Spatial Transformer Network (STN) | A differentiable network module that learns to warp its input to a canonical pose. |
| Test-time adaptation (TTA) | Adapting a model on unlabelled test data during inference (for example, updating normalisation statistics). |
| Threshold (τ) | The score above which a die or pixel is called anomalous. |
| Unknown anomaly | An anomalous region that does not match any known defect class; it is sent for engineer investigation. |
| Vision Transformer (ViT) | A network that splits an image into patches and processes them with self-attention. |
| Wafer | A thin disc of semiconductor material (usually silicon) on which many identical dies are fabricated. |
| Wafer map | A grid showing each die's position and result (pass/fail or bin code); shows spatial patterns across the wafer. |
| Yield | Fraction of dies on a wafer that work correctly. |
