import kagglehub
from kagglehub import KaggleDatasetAdapter

def load_cdc():
    return kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        "abdelazizsami/cdc-diabetes-health-indicators",
        "diabetes_binary_health_indicators_BRFSS2015.csv"
    )
