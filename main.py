"""
    Pipeline integrator
"""

from pipeline.config import ENDPOINT, REGION
from pipeline.bronze import make_connection, bronze_layer
from pipeline.silver import silver_layer
from pipeline.gold import gold_layer

def main()->None:
    client = make_connection(ENDPOINT, REGION)
    bronze_layer(client)
    silver_layer(client)
    gold_layer(client)


if __name__ == "__main__":
    main()