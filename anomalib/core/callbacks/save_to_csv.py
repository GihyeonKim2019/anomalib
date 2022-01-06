"""Callback to save metrics to CSV."""
from pathlib import Path

import numpy as np
import pandas as pd
from pytorch_lightning import Callback, Trainer

from anomalib.core.model import AnomalibModule


class SaveToCSVCallback(Callback):
    """Callback that saves the inference results of a model.

    The callback generates a csv file that saves different performance
    metrics and results.
    """

    def __init__(self):
        """Callback to save metrics to CSV."""

    def on_test_epoch_end(self, trainer: Trainer, pl_module: AnomalibModule) -> None:
        """Save Results at the end of training.

        Args:
            trainer (Trainer): Pytorch lightning trainer object (unused)
            pl_module (LightningModule): Lightning modules derived from BaseAnomalyLightning object.
        """
        results = pl_module.results
        data_frame = pd.DataFrame(
            {
                "name": results.filenames,
                "true_label": results.true_labels,
                "pred_label": results.pred_labels.astype(int),
                "wrong_prediction": np.logical_xor(results.true_labels, results.pred_labels).astype(int),
            }
        )

        if trainer.log_dir is not None:
            data_frame.to_csv(Path(trainer.log_dir) / "results.csv")
        else:
            raise ValueError("trainer.log_dir does not exist to save the results.")